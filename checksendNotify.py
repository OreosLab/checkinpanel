#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import os
import re
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

import base64
import hashlib
import hmac
import json5 as json
import requests
import time
import urllib.parse

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

    'QQ_MODE': '',                      # qq 机器人的 QQ_MODE
    'QQ_SKEY': '',                      # qq 机器人的 QQ_SKEY

    'QYWX_AM': '',                      # 企业微信

    'PUSH_PLUS_TOKEN': '',              # 微信推送 Plus+

    'GOBOT_URL': '',                    # go-cqhttp
                                        # 推送到个人QQ: http://127.0.0.1/send_private_msg
                                        # 群：http://127.0.0.1/send_group_msg
    'GOBOT_TOKEN': '',                  # go-cqhttp 的 access_token, 可不填
    'GOBOT_QQ': '',                     # go-cqhttp 的推送群或者用户
                                        # GOBOT_URL 设置 /send_private_msg 填入 user_id=个人QQ
                                        #               /send_group_msg   填入 group_id=QQ群
}
notify_function = []

# 读取配置文件中的变量
CONFIG_PATH = os.getenv("NOTIFY_CONFIG_PATH") or "/ql/config/notify_config.json5"
if os.path.exists(CONFIG_PATH):
    for k, v in dict(json.load(open(CONFIG_PATH, mode="r", encoding="utf-8"))).items():
        if k in push_config:
            push_config[k] = v

#  GitHub action 运行环境变量覆盖配置文件的变量
for k in push_config:
    if v := os.getenv(k):
        push_config[k] = v


def bark(title, content):
    print("\n")
    if not push_config.get('BARK'):
        print("bark 服务的 bark_token 未设置!!\n取消推送")
        return
    print("bark 服务启动")

    if push_config.get('BARK').startswith('http'):
        url = f"""{push_config.get('BARK')}/{title}/{content}"""
    else:
        url = f"""https://api.day.app/{push_config.get('BARK')}/{title}/{content}"""
    response = requests.get(url).json()

    if response['code'] == 200:
        print('bark 推送成功！')
    else:
        print('bark 推送失败！')


def go_cqhttp(title, content):
    print("\n")
    if not push_config.get('GOBOT_URL') or not push_config.get('GOBOT_QQ'):
        print("go-cqhttp 服务的 GOBOT_URL 或 GOBOT_QQ 未设置!!\n取消推送")
        return
    print("go-cqhttp 服务启动")

    url = f"""{push_config.get('GOBOT_URL')}?access_token={push_config.get('GOBOT_TOKEN')}&{push_config.get('GOBOT_QQ')}&message=标题:{title}\n内容:{content}"""
    response = requests.get(url).json()

    if response['status'] == 'ok':
        print('go-cqhttp 推送成功！')
    else:
        print('go-cqhttp 推送失败！')


def serverJ(title, content):
    print("\n")
    if not push_config.get('PUSH_KEY'):
        print("server 酱服务的 PUSH_KEY 未设置!!\n取消推送")
        return
    print("serverJ 服务启动")

    data = {
        "text": title,
        "desp": content.replace("\n", "\n\n")
    }
    response = requests.post(f"https://sct.ftqq.com/{push_config.get('PUSH_KEY')}.send", data=data).json()

    if response['errno'] == 0:
        print('serverJ 推送成功！')
    else:
        print('serverJ 推送失败！')


# tg通知
def telegram_bot(title, content):
    print("\n")
    if not push_config.get('TG_BOT_TOKEN') or not push_config.get('TG_USER_ID'):
        print("tg 服务的 bot_token 或者 user_id 未设置!!\n取消推送")
        return
    print("tg 服务启动")

    if push_config.get('TG_API_HOST'):
        url = f"https://{push_config.get('TG_API_HOST')}/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
    else:
        url = f"https://api.telegram.org/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'chat_id': str(push_config.get('TG_USER_ID')), 'text': f'{title}\n\n{content}',
               'disable_web_page_preview': 'true'}
    proxies = None
    if push_config.get('TG_PROXY_IP') and push_config.get('TG_PROXY_PORT'):
        proxyStr = "http://{}:{}".format(push_config.get('TG_PROXY_IP'), push_config.get('TG_PROXY_PORT'))
        proxies = {"http": proxyStr, "https": proxyStr}
    response = requests.post(url=url, headers=headers, params=payload, proxies=proxies).json()

    if response['ok']:
        print('tg 推送成功！')
    else:
        print('tg 推送失败！')


def dingding_bot(title, content):
    print("\n")
    if not push_config.get('DD_BOT_SECRET') or not push_config.get('DD_BOT_TOKEN'):
        print("钉钉机器人 服务的 DD_BOT_SECRET 或者 DD_BOT_TOKEN 未设置!!\n取消推送")
        return
    print("钉钉机器人 服务启动")

    timestamp = str(round(time.time() * 1000))
    secret_enc = push_config.get('DD_BOT_SECRET').encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, push_config.get('DD_BOT_SECRET'))
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://oapi.dingtalk.com/robot/send?access_token={push_config.get("DD_BOT_TOKEN")}&timestamp={timestamp}&sign={sign}'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {'content': f'{title}\n\n{content}'}
    }
    response = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=15).json()

    if not response['errcode']:
        print('钉钉机器人 推送成功！')
    else:
        print('钉钉机器人 推送失败！')


def coolpush_bot(title, content):
    print("\n")
    if not push_config.get('QQ_SKEY') or not push_config.get('QQ_MODE'):
        print("qmsg 的 QQ_SKEY 或者 QQ_MODE 未设置!!\n取消推送")
        return
    print("qmsg 启动")

    url = f"https://qmsg.zendee.cn/{push_config.get('QQ_MODE')}/{push_config.get('QQ_SKEY')}"
    payload = {'msg': f"{title}\n\n{content}".encode('utf-8')}
    response = requests.post(url=url, params=payload).json()

    if response['code'] == 0:
        print('qmsg 推送成功！')
    else:
        print('qmsg 推送失败！')


# push推送
def pushplus_bot(title, content):
    print("\n")
    if not push_config.get('PUSH_PLUS_TOKEN'):
        print("PUSHPLUS 服务的token未设置!!\n取消推送")
        return
    print("PUSHPLUS 服务启动")

    url = 'http://www.pushplus.plus/send'
    data = {
        "token": push_config.get('PUSH_PLUS_TOKEN'),
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response['code'] == 200:
        print('PUSHPLUS 推送成功！')
    else:
        print('PUSHPLUS 推送失败！')


# 企业微信 APP 推送
def wecom_app(title, content):
    print("\n")
    if not push_config.get('QYWX_AM'):
        print("QYWX_AM 未设置！！\n取消推送")
        return
    QYWX_AM_AY = re.split(',', push_config.get('QYWX_AM'))
    if 4 < len(QYWX_AM_AY) > 5:
        print("QYWX_AM 设置错误！！\n取消推送")
        return

    corpid = QYWX_AM_AY[0]
    corpsecret = QYWX_AM_AY[1]
    touser = QYWX_AM_AY[2]
    agentid = QYWX_AM_AY[3]
    try:
        media_id = QYWX_AM_AY[4]
    except KeyError:
        media_id = ''
    wx = WeCom(corpid, corpsecret, agentid)
    # 如果没有配置 media_id 默认就以 text 方式发送
    if not media_id:
        message = title + '\n\n' + content
        response = wx.send_text(message, touser)
    else:
        response = wx.send_mpnews(title, content, media_id, touser)

    if response == 'ok':
        print('推送成功！')
    else:
        print('推送失败！错误信息如下：\n', response)


class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace('\n', '<br/>'),
                        "digest": message
                    }
                ]
            }
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]


def one():
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
if push_config.get('QQ_SKEY') and push_config.get('QQ_MODE'):
    notify_function.append(coolpush_bot)
if push_config.get('PUSH_PLUS_TOKEN'):
    notify_function.append(pushplus_bot)
if push_config.get('QYWX_AM'):
    notify_function.append(wecom_app)


def send(title, content):
    hitokoto = push_config.get('HITOKOTO')

    text = one() if hitokoto else ''
    content += '\n\n' + text

    for mode in notify_function:
        try:
            mode(title=title, content=content)
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败： {str(e)}, {mode.__name__}")


def main():
    send('title', 'content')


if __name__ == '__main__':
    main()