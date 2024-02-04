import nonebot
import aiohttp
import re
import io
import os
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.params import CommandArg
from PIL import Image

# 设置代理地址
global_config = nonebot.get_driver().config
config = global_config.dict()
PROXY = config.get('aiohttp') if config.get('aiohttp') else ""
# 创建正则表达式命令处理器，匹配“来张”后跟任意文字的消息
setu = on_regex(r'#?来张(.+)', priority=10, block=True)

@setu.handle()
async def handle_receive(bot: Bot, event: MessageEvent):
    # 从事件中提取匹配的正则表达式分组
    match = re.match(r'#?来张(.+)', event.get_plaintext())
    if match:
        tag = match.group(1).strip()  # 获取匹配到的tag
        if not tag:
            # 如果没有提供参数，则给出提示
            await setu.finish('你想要来张什么呢？')
        else:
            # 构建API URL
            url = f'https://api.lolicon.app/setu/v2?tag={tag}'
            
            # 发送HTTP请求
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=PROXY) as response:
                    if response.status != 200:
                        # 如果HTTP请求失败
                        await setu.finish('获取图片失败了呢...')
                    data = await response.json()
            
            # 检查返回的数据
            if data['error'] or not data['data']:
                await setu.finish('找不到图片呢...')
            
            # 提取图片URL
            image_info = data['data'][0]
            image_url = image_info['urls']['original']
            # 提取图片文件名
            image_filename = image_url.split('/')[-1]

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, proxy=PROXY) as img_response:
                    if img_response.status != 200:
                        await setu.finish('下载图片失败了呢...')
                    # 读取图片数据
                    image_data = await img_response.read()
            # 获取当前脚本文件的目录
            script_dir = os.path.dirname(os.path.abspath(__file__))        
            # img文件夹的相对路径
            img_folder_path = os.path.join(script_dir, 'img')
            # 确保img文件夹存在
            if not os.path.exists(img_folder_path):
                os.makedirs(img_folder_path)
            # 图片保存路径
            image_path = os.path.join(img_folder_path, image_filename)    
            # 保存图片到本地
            with open(image_path, 'wb') as f:
                f.write(image_data)
            # 使用Pillow打开图片并压缩
            with Image.open(image_path) as img:
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                elif img.mode == 'LA' or (img.mode == 'P' and 'transparency' in img.info):
                    alpha = img.convert('RGBA').split()[-1]
                    bg = Image.new("RGBA", img.size, (255, 255, 255) + (255,))
                    bg.paste(img, mask=alpha)
                    img = bg.convert('RGB')
                elif img.mode == 'P':
                    img = img.convert('RGB')
                # 定义压缩图片的路径
                compressed_image_path = os.path.splitext(image_path)[0] + "_compressed.jpg"
                # 保存压缩后的图片，优化为较低的质量
                img.save(compressed_image_path, 'JPEG', quality=75, optimize=True)
            # 发送图片
            await setu.send(MessageSegment.image(f'file:///{compressed_image_path}'))