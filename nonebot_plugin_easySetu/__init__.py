import nonebot
import aiohttp
import re
import html
from datetime import datetime
from nonebot import on_command, on
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Event, GroupMessageEvent
from nonebot.params import CommandArg
from PIL import Image
from nonebot.exception import ActionFailed
from nonebot.permission import SUPERUSER
import json
import io
import os
global_config = nonebot.get_driver().config
config = global_config.dict()
PROXY = config.get('aiohttp') if config.get('aiohttp') else ""
on_message_sent = on("message_sent", block=False)
allowgroup = [123]

# 获取当前脚本文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 config.json 文件的绝对路径
CONFIG_FILE = os.path.join(current_dir, 'config.json')
mode_file = os.path.join(current_dir, 'mode.json')
def load_mode():
    try:
        with open(mode_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 1  # 默认值

# 保存 access 值到文件
def save_mode(mode_value):
    with open(mode_file, 'w') as f:
        json.dump(mode_value, f)

# 初始化 access 变量
mode = load_mode()
# 尝试从文件加载 access 值，如果文件不存在，则设置默认值为 1
def load_access():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 1  # 默认值

# 保存 access 值到文件
def save_access(access_value):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(access_value, f)

# 初始化 access 变量
access = load_access()

set_access = on_command("设置", priority=1, permission=SUPERUSER)
@set_access.handle()
async def handle_first_receive(bot: Bot, event: Event):
    global access  # 使用全局变量
    args = str(event.get_message()).strip()

    # 根据命令设置 access 的值
    if args == "设置仅我可用":
        access = 1
        response = "已设置：仅你可用"
    elif args == "设置仅管理可用":
        access = 2
        response = "已设置：仅管理可用"
    elif args == "设置所有人可用":
        access = 3
        response = "已设置：所有人可用"
    else:
        return

    # 保存修改后的 access 值到文件
    save_access(access)

    await set_access.finish(response)
setu = on_regex(r'#?来张(.+)', priority=10, block=True)

@setu.handle()
async def handle_receive(bot: Bot, event: MessageEvent):

    match = re.match(r'#?来张(.+)', event.get_plaintext())
    if match:
        tag = match.group(1).strip()  
        if isinstance(event, GroupMessageEvent) and access == 1:
            await setu.finish(f'只有主人可以用哦')
        elif isinstance(event, GroupMessageEvent) and access == 2 and event.sender.role not in ('owner', 'admin'):
            await setu.finish(f'臣服于权限喵，仅管理可用')
        else:
            # 构建API URL
            
            url = f'https://api.lolicon.app/setu/v2?tag={tag}'
            
            # 发送HTTP请求
            async with aiohttp.ClientSession() as session:
                async with session.get(url, ssl=False) as response:
                    if response.status != 200:
                        # 如果HTTP请求失败
                        await setu.send(MessageSegment.at(event.user_id) + f'API请求失败，错误码:{response.status}')
                        await setu.finish(MessageSegment.at(event.user_id) + f'\n获取图片失败,请重试')
                    data = await response.json()
            
            # 检查返回的数据
            if data['error'] or not data['data']:
                await setu.finish(MessageSegment.at(event.user_id) + f'\n暂无此tag图片\n查询的标签：{tag}')

            
            # 提取图片URL
            image_info = data['data'][0]
            image_url = image_info['urls']['original']
            pid = image_info['pid']
            title = image_info['title']
            drawuser = image_info['author'] 
            uid = image_info['uid']
            # 提取图片文件名
            image_filename = image_url.split('/')[-1]

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as img_response:
                    if img_response.status != 200:
                        await setu.finish(MessageSegment.at(event.user_id) + f'\n下载图片失败,错误码:{img_response.status}')
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

            
            try:
                await setu.send(MessageSegment.at(event.user_id) + MessageSegment.text(f"\n图来咯~\n查询的tag：{tag}\ntitle:{title}\nuid:{uid}\n画师:{drawuser}\npid:{pid}") + MessageSegment.image(f'file:///{image_path}'))
            except ActionFailed:
                await setu.send(MessageSegment.text(f"图片被拦截，可以使用链接查看~\n{image_url}"))
@on_message_sent.handle()
async def handle_message_sent(bot: Bot, event: Event):
    if isinstance(event, Event) and event.raw_message == "现在谁能用":
        if access == 1:
            await setu.finish(f'现在只有主人可以用哦')
        elif access ==2 :
            await setu.finish('现在只有管理可以用哦')
        elif access == 3:
            await setu.finish('现在所有人都可以用呢')

    match = re.match(r'#?来张(.+)', html.unescape(event.raw_message))
    if match:
        tag = match.group(1).strip()  # 获取匹配到的tag
        if  tag == "亚托莉":
            
            await setu.finish('false')

        else:
            # 构建API URL
            
            url = f'https://api.lolicon.app/setu/v2?tag={tag}'
            
            # 发送HTTP请求
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        # 如果HTTP请求失败
                        await setu.send(MessageSegment.at(event.user_id) + f'API请求失败，错误码:{response.status}')
                        await setu.finish(MessageSegment.at(event.user_id) + '获取图片失败,请重试')
                    data = await response.json()
            
            # 检查返回的数据
            if data['error'] or not data['data']:
                await setu.finish(MessageSegment.at(event.user_id) + f'暂无此tag图片，可尝试更换罗马字或片假名查询\n查询的标签：{tag}')

            
            # 提取图片URL
            image_info = data['data'][0]
            image_url = image_info['urls']['original']
            pid = image_info['pid']
            title = image_info['title']
            drawuser = image_info['author'] 
            uid = image_info['uid']
            # 提取图片文件名
            image_filename = image_url.split('/')[-1]

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as img_response:
                    if img_response.status != 200:
                        await setu.finish(MessageSegment.at(event.user_id) + f'\n下载图片失败,错误码:{img_response.status}')
                    # 读取图片数据
                    image_data = await img_response.read()
            # 获取当前脚本文件的目录
            script_dir = os.path.dirname(os.path.abspath(__file__))        
            # img文件夹的相对路径
            img_folder_path = os.path.join(script_dir, 'img++')
            # 确保img文件夹存在
            if not os.path.exists(img_folder_path):
                os.makedirs(img_folder_path)
            # 图片保存路径
            image_path = os.path.join(img_folder_path, image_filename)    
            # 保存图片到本地
            with open(image_path, 'wb') as f:
                f.write(image_data)

            # 发送图片
            message = MessageSegment.at(event.user_id) + MessageSegment.text(f"\n查询的tag：{tag}\ntitle:{title}\nuid:{uid}\n画师:{drawuser}\npid:{pid}") + MessageSegment.image(f'file:///{image_path}')
            message2 = MessageSegment.text(f"图片被拦截，可以使用链接查看~\n{image_url}")
            if event.message_type == "private":
                user_id = event.target_id
                try:
                    await bot.send_private_msg(user_id = user_id, message = message)
                except ActionFailed:
                    await bot.send_private_msg(user_id = user_id, message = message2)
            elif event.message_type == "group":
                group_id = event.target_id
                try:
                    await bot.send_group_msg(group_id = group_id, message = message)
                except ActionFailed:
                    await bot.send_group_msg(group_id = group_id, message = message2)
            else :
                return
@on_message_sent.handle()
async def handle_message_sent2(bot: Bot, event: Event):
    matches = re.match(r'#?设置(.+)', event.raw_message)
    global access
    global mode
    if matches:
        sett = matches.group(1).strip()
        if  sett == "仅我可用":
            access = 1
            response1 = "已设置仅我可用"
        elif sett == "仅管理可用":
            access = 2
            response1 = "已设置仅管理可用"
        elif sett == "所有人可用":
            access = 3
            response1 = "已设置所有人可用"
        elif sett == "正常模式":
            mode = 1
            response1 = "已设置为正常模式"
        elif sett == "涩图模式":
            mode = 2
            response1 = "已设置为涩图模式"
        else:
            return
        save_access(access)
        save_mode(mode)
        await set_access.finish(response1)
