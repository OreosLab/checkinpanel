#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import base64
import hashlib
import hmac
import os
import re
import threading
import time
import urllib.parse

import json5 as json
import requests

from utils_env import get_file_path

# 原先的 print 函数和主线程的锁
_print = print
mutex = threading.Lock()


# 定义新的 print 函数
def print(text, *args, **kw):
    '''
    使输出有序进行，不出现多线程同一时间输出导致错乱的问题。
    '''
    with mutex:
        _print(text, *args, **kw)


# 通知服务
push_config = {
    'HITOKOTO': False,                  # 启用一言（随机句子）

    'BARK': '',                         # bark 服务，自行搜索；此参数如果以 http 或者 https 开头则判定为自建 bark 服务

    'PUSH_KEY': '',                     # Server酱的 PUSH_KEY

    'TG_BOT_TOKEN': '',                 # tg 机器人的 TG_BOT_TOKEN；例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
    'TG_USER_ID': '',                   # tg 机器人的TG_USER_ID；例：1434078534
    'TG_API_HOST': '',                  # tg 代理 api
    'TG_PROXY_IP': '',                  # tg 机器人的 TG_PROXY_IP
    'TG_PROXY_PORT': '',                # tg 机器人的 TG_PROXY_PORT

    'DD_BOT_TOKEN': '',                 # 钉钉机器人的 DD_BOT_TOKEN
    'DD_BOT_SECRET': '',                # 钉钉机器人的 DD_BOT_SECRET

    'QMSG_TYPE': '',                    # qq 机器人的 QMSG_TYPE
    'QMSG_KEY': '',                     # qq 机器人的 QMSG_KEY

    'QYWX_AM': '',                      # 企业微信

    'PUSH_PLUS_TOKEN': '',              # 微信推送 Plus+

    'GOBOT_URL': '',                    # go-cqhttp
                                        # 推送到个人QQ: http://127.0.0.1/send_private_msg
                                        # 群：http://127.0.0.1/send_group_msg
    'GOBOT_TOKEN': '',                  # go-cqhttp 的 access_token, 可不填
    'GOBOT_QQ': '',                     # go-cqhttp 的推送群或者用户
                                        # GOBOT_URL 设置 /send_private_msg 填入 user_id=个人QQ
                                        #               /send_group_msg   填入 group_id=QQ群

    'FSKEY': '',                        # 飞书 的 FSKEY；https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx 的 xxxxxx 部分
}
notify_function = []

# 首先读取 面板变量 或者 github action 运行变量
for k in push_config:
    if v := os.getenv(k):
        push_config[k] = v

# 读取配置文件中的变量 (会覆盖环境变量)
CONFIG_PATH = os.getenv('NOTIFY_CONFIG_PATH') or get_file_path('notify.json5')
if os.path.exists(CONFIG_PATH):
    print(f'通知配置文件存在：{CONFIG_PATH}。')
    try:
        for k, v in dict(
            json.load(open(CONFIG_PATH, mode='r', encoding='utf-8'))
        ).items():
            if k in push_config:
                push_config[k] = v
    except ValueError:
        print(
            f'错误：配置文件 {CONFIG_PATH} 格式不对，请在 https://verytoolz.com/json5-validator.html 中检查格式'
        )
elif CONFIG_PATH:
    print(f'{CONFIG_PATH} 配置的通知文件不存在，请检查文件位置或删除对应环境变量！')


def bark(title: str, content: str) -> None:
    """
    使用 bark 推送消息。
    """
    if not push_config.get('BARK'):
        print('bark 服务的 bark_token 未设置!!\n取消推送')
        return
    print('bark 服务启动')

    if push_config.get('BARK').startswith('http'):
        url = f'{push_config.get("BARK")}/{title}/{content}'
    else:
        url = f'https://api.day.app/{push_config.get("BARK")}/{title}/{content}'
    response = requests.get(url).json()

    if response['code'] == 200:
        print('bark 推送成功！')
    else:
        print('bark 推送失败！')


def go_cqhttp(title: str, content: str) -> None:
    """
    使用 go_cqhttp 推送一条消息
    """
    if not push_config.get('GOBOT_URL') or not push_config.get('GOBOT_QQ'):
        print('go-cqhttp 服务的 GOBOT_URL 或 GOBOT_QQ 未设置!!\n取消推送')
        return
    print('go-cqhttp 服务启动')

    url = f'{push_config.get("GOBOT_URL")}?access_token={push_config.get("GOBOT_TOKEN")}&{push_config.get("GOBOT_QQ")}&message=标题:{title}\n内容:{content}'
    response = requests.get(url).json()

    if response['status'] == 'ok':
        print('go-cqhttp 推送成功！')
    else:
        print('go-cqhttp 推送失败！')


def serverJ(title: str, content: str) -> None:
    """
    通过 ServerJ 发送一条消息。
    """
    if not push_config.get('PUSH_KEY'):
        print('serverJ 服务的 PUSH_KEY 未设置!!\n取消推送')
        return
    print('serverJ 服务启动')

    data = {'text': title, 'desp': content.replace('\n', '\n\n')}
    if push_config.get('PUSH_KEY').index('SCT') != -1:
        url = f'https://sctapi.ftqq.com/{push_config.get("PUSH_KEY")}.send'
    else:
        url = f'https://sc.ftqq.com/${push_config.get("PUSH_KEY")}.send'
    response = requests.post(url, data=data).json()

    if response.get('errno') == 0 or response.get('code') == 0:
        print('serverJ 推送成功！')
    else:
        print(f'serverJ 推送失败！错误码：{response["message"]}')


def telegram_bot(title: str, content: str) -> None:
    """
    通过 telegram 发送一条通知。
    """
    if not push_config.get('TG_BOT_TOKEN') or not push_config.get('TG_USER_ID'):
        print("tg 服务的 bot_token 或者 user_id 未设置!!\n取消推送")
        return
    print("tg 服务启动")

    if push_config.get('TG_API_HOST'):
        url = f"https://{push_config.get('TG_API_HOST')}/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
    else:
        url = f"https://api.telegram.org/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'chat_id': str(push_config.get('TG_USER_ID')),
        'text': f'{title}\n\n{content}',
        'disable_web_page_preview': 'true'
    }
    proxies = None
    if push_config.get('TG_PROXY_IP') and push_config.get('TG_PROXY_PORT'):
        proxyStr = "http://{}:{}".format(
            push_config.get('TG_PROXY_IP'),
            push_config.get('TG_PROXY_PORT')
        )
        proxies = {"http": proxyStr, "https": proxyStr}
    response = requests.post(url=url,
                             headers=headers,
                             params=payload,
                             proxies=proxies).json()

    if response['ok']:
        print('tg 推送成功！')
    else:
        print('tg 推送失败！')


def dingding_bot(title: str, content: str) -> None:
    """
    使用 钉钉机器人 发送一条通知。
    """
    if not push_config.get('DD_BOT_SECRET') or not push_config.get(
            'DD_BOT_TOKEN'):
        print("钉钉机器人 服务的 DD_BOT_SECRET 或者 DD_BOT_TOKEN 未设置!!\n取消推送")
        return
    print("钉钉机器人 服务启动")

    timestamp = str(round(time.time() * 1000))
    secret_enc = push_config.get('DD_BOT_SECRET').encode('utf-8')
    string_to_sign = '{}\n{}'.format(
        timestamp,
        push_config.get('DD_BOT_SECRET')
    )
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc,
                         string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://oapi.dingtalk.com/robot/send?access_token={push_config.get("DD_BOT_TOKEN")}&timestamp={timestamp}&sign={sign}'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {'msgtype': 'text', 'text': {'content': f'{title}\n\n{content}'}}
    response = requests.post(url=url,
                             data=json.dumps(data, quote_keys=True),
                             headers=headers,
                             timeout=15).json()

    if not response['errcode']:
        print('钉钉机器人 推送成功！')
    else:
        print('钉钉机器人 推送失败！')


def qmsg_bot(title: str, content: str) -> None:
    """
    使用 qmsg 发送一条消息。
    """
    if not push_config.get('QMSG_KEY') or not push_config.get('QMSG_TYPE'):
        print('qmsg 的 QMSG_KEY 或者 QMSG_TYPE 未设置!!\n取消推送')
        return
    print('qmsg 启动')

    url = f'https://qmsg.zendee.cn/{push_config.get("QMSG_TYPE")}/{push_config.get("QMSG_KEY")}'
    payload = {
        'msg': f'{title}\n\n{content.replace("----", "-")}'.encode('utf-8')
    }
    response = requests.post(url=url, params=payload).json()

    if response['code'] == 0:
        print('qmsg 推送成功！')
    else:
        print(f'qmsg 推送失败！{response["reason"]}')


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 发送一条推送。
    """
    if not push_config.get('PUSH_PLUS_TOKEN'):
        print('PUSHPLUS 服务的 token 未设置!!\n取消推送')
        return
    print('PUSHPLUS 服务启动')

    url = 'http://www.pushplus.plus/send'
    data = {
        'token': push_config.get('PUSH_PLUS_TOKEN'),
        'title': title,
        'content': content
    }
    body = json.dumps(data, quote_keys=True).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response['code'] == 200:
        print('PUSHPLUS 推送成功！')
    else:
        print('PUSHPLUS 推送失败！')


def wecom_app(title: str, content: str) -> None:
    """
    通过 企业微信 APP 发送推送。
    """
    if not push_config.get('QYWX_AM'):
        print('QYWX_AM 未设置！！\n取消推送')
        return
    QYWX_AM_AY = re.split(',', push_config.get('QYWX_AM'))
    if 4 < len(QYWX_AM_AY) > 5:
        print('QYWX_AM 设置错误！！\n取消推送')
        return

    corpid = QYWX_AM_AY[0]
    corpsecret = QYWX_AM_AY[1]
    touser = QYWX_AM_AY[2]
    agentid = QYWX_AM_AY[3]
    try:
        media_id = QYWX_AM_AY[4]
    except IndexError:
        media_id = ''
    wx = WeCom(corpid, corpsecret, agentid)
    # 如果没有配置 media_id 默认就以 text 方式发送
    if not media_id:
        message = title + '\n\n' + content
        response = wx.send_text(message, touser)
    else:
        response = wx.send_mpnews(title, content, media_id, touser)

    if response == 'ok':
        print('企业微信推送成功！')
    else:
        print('企业微信推送失败！错误信息如下：\n', response)


class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {
            'corpid': self.CORPID,
            'corpsecret': self.CORPSECRET,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data['access_token']

    def send_text(self, message, touser='@all'):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            'touser': touser,
            'msgtype': 'text',
            'agentid': self.AGENTID,
            'text': {
                'content': message
            },
            'safe': '0'
        }
        send_msges = (bytes(json.dumps(send_values, quote_keys=True), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone['errmsg']

    def send_mpnews(self, title, message, media_id, touser='@all'):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            'touser': touser,
            'msgtype': 'mpnews',
            'agentid': self.AGENTID,
            'mpnews': {
                'articles': [
                    {
                        'title': title,
                        'thumb_media_id': media_id,
                        'author': 'Author',
                        'content_source_url': '',
                        'content': message.replace('\n', '<br/>'),
                        'digest': message
                    }
                ]
            }
        }
        send_msges = (bytes(json.dumps(send_values, quote_keys=True), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone['errmsg']


def feishu(title: str, content: str) -> None:
    """
    通过 飞书 发送一条推送。
    """
    if not push_config.get('FSKEY'):
        print('飞书 服务的 FSKEY 未设置!!\n取消推送')
        return
    print('飞书 服务启动')

    url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{push_config.get("FSKEY")}'
    data = {'msg_type': 'text', 'content': {'text': f'{title}\n\n{content}'}}
    response = requests.post(url, data=json.dumps(data,
                                                  quote_keys=True)).json()

    if response.get('StatusCode') == 0:
        print('飞书 推送成功！')
    else:
        print('飞书 推送失败！错误信息如下：\n', response)


def one() -> str:
    """
    获取一条一言。
    :return:
    """
    url = 'https://v1.hitokoto.cn/'
    res = requests.get(url).json()
    return res['hitokoto'] + '    ----' + res['from']


if push_config.get('BARK'):
    notify_function.append(bark)
if push_config.get('GOBOT_URL') and push_config.get('GOBOT_QQ'):
    notify_function.append(go_cqhttp)
if push_config.get('PUSH_KEY'):
    notify_function.append(serverJ)
if push_config.get('TG_BOT_TOKEN') and push_config.get('TG_USER_ID'):
    notify_function.append(telegram_bot)
if push_config.get('DD_BOT_TOKEN') and push_config.get('DD_BOT_SECRET'):
    notify_function.append(dingding_bot)
if push_config.get('QMSG_KEY') and push_config.get('QMSG_TYPE'):
    notify_function.append(qmsg_bot)
if push_config.get('PUSH_PLUS_TOKEN'):
    notify_function.append(pushplus_bot)
if push_config.get('QYWX_AM'):
    notify_function.append(wecom_app)
if push_config.get('FSKEY'):
    notify_function.append(feishu)


def excepthook(args, /):
    if issubclass(args.exc_type, requests.exceptions.RequestException):
        print(
            f'网络异常，请检查你的网络连接、推送服务器和代理配置，该错误和账号配置无关。信息：{str(args.exc_type)}, {args.thread.name}'
        )
    else:
        global default_hook
        default_hook(args)


default_hook = threading.excepthook
threading.excepthook = excepthook


def send(title: str, content: str) -> None:
    hitokoto = push_config.get('HITOKOTO')

    text = one() if hitokoto else ''
    content += '\n\n' + text

    ts = [threading.Thread(target=mode,
                           args=(title, content),
                           name=mode.__name__) for mode in notify_function]
    [t.start() for t in ts]
    [t.join() for t in ts]


def main():
    send('title', 'content')


if __name__ == '__main__':
    main()
