<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-mypower

_✨ 一款从lolicon API获取指定tag图片的插件（适用于Onebot V11）✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/tianyisama/nonebot_plugin_easySetu" alt="license">
</a><img src="https://img.shields.io/badge/nonebot-2.0.0rc1+-red.svg" alt="NoneBot">
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

一款从lolicon API获取指定tag图片的插件（适用于Nonebot2 V11）

## 前言

其实是写给我自己偷偷找 ~~涩图~~ 美图用的，因此非常简陋

## 💿 安装

<details>
<summary>安装pillow(必须)</summary>


    pip install pillow
  若采用了虚拟环境，则需要在虚拟环境中执行
</details>

<details>
<summary>安装aiohttp(必须)</summary>


    pip install aiohttp
  若采用了虚拟环境，则需要在虚拟环境中执行
</details>
以下两种方式任选其一即可
<details>

<summary>使用nb-cli安装(推荐)</summary>


    nb plugin install nonebot-plugin-easySetu
    

</details>

<details>
<summary>使用PIP安装</summary>


    pip install nonebot-plugin-easySetu
    
安装完成后，请在你的`bot.py`文件中添加以下代码来导入插件：
 `nonebot.load_plugin("nonebot_plugin_easySetu")`
</details>

## 参数

需要在env中设置代理：
 `aiohttp=127.0.0.1:7890 #示例`
不想设置也没关系，将代码33行与50行`, proxy=PROXY`删除即可

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 |
|:-----:|:----:|:----:|:----:|
| 来张XX | 所有人 | 否 | 群聊与私聊 |

例如：来张萝莉

## ⚠ 注意

本插件会在<u>插件内</u>创建一个名为img的文件夹，然后每次获取都会将图片保存下来，同时对图片进行了压缩处理（也会保存），然后发送压缩后的图片，写出来的本意是适配qqbot的，腾讯的图片超时5000ms就发不出去了

本插件使用的API为[Lolicon API](https://api.lolicon.app/#/)，另外由于 ~~鄙人较懒~~ 我非常懒，参数只匹配了来张后面的文本，如果你不嫌麻烦的话，指令后可接各种参数
| 参数名 | 数据类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| r18 | int | 0 | 0为非 R18，1为 R18，2为混合 |
| num | int | 1 | 一次返回的结果数量，范围为1到20；在指定关键字或标签的情况下，结果数量可能会不足指定的数量 |
| uid | int[] |   | 返回指定uid作者的作品，最多20个 |
| keyword | string |   | 返回从标题、作者、标签中按指定关键字模糊匹配的结果，大小写不敏感，性能和准度较差且功能单一，建议使用tag代替 |
| tag | string[] |   | 返回匹配指定标签的作品 |
| size | string[] | ["original"] | 返回指定图片规格的地址 |
| proxy | string | i.pixiv.re | 	设置图片地址所使用的在线反代服务 |
| dateAfter | int |   | 返回在这个时间及以后上传的作品；时间戳，单位为毫秒 |
| dateBefore | int |   | 返回在这个时间及以前上传的作品；时间戳，单位为毫秒 |
| dsc | boolean | false | 用对某些缩写keyword和tag的自动转换 |
| excludeAI | boolean | false | 排除 AI 作品 |

例如：`https://api.lolicon.app/setu/v2?tag=萝莉&tag=贫乳&r18=1&excludeAI=true`就是返回tag为萝莉和贫乳且为r18且不是ai的作品
本插件（大概）只适配了tag，r18，keyword等这些只会返回一个url的参数，因为我只写了一个（），动手能力强的可以自己改改