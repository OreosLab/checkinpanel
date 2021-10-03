# -*- coding: utf-8 -*-
"""
:source https://github.com/MayoBlueSky/My-Actions/blob/master/function/cloud189/checkin.py
cron: 30 9 * * *
new Env('天翼云盘');
"""

import base64
import re
import time

import requests
import rsa

from notify_mtr import send
from utils import get_data


class Cloud189:
    def __init__(self, check_items):
        self.check_items = check_items
        self.b64map = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")

    @staticmethod
    def int2char(a):
        return list("0123456789abcdefghijklmnopqrstuvwxyz")[a]

    def b64tohex(self, a):
        d = ""
        e = 0
        c = 0
        for i in range(len(a)):
            if list(a)[i] != "=":
                v = self.b64map.index(list(a)[i])
                if 0 == e:
                    e = 1
                    d += self.int2char(v >> 2)
                    c = 3 & v
                elif 1 == e:
                    e = 2
                    d += self.int2char(c << 2 | v >> 4)
                    c = 15 & v
                elif 2 == e:
                    e = 3
                    d += self.int2char(c)
                    d += self.int2char(v >> 2)
                    c = 3 & v
                else:
                    e = 0
                    d += self.int2char(c << 2 | v >> 4)
                    d += self.int2char(15 & v)
        if e == 1:
            d += self.int2char(c << 2)
        return d

    def rsa_encode(self, j_rsakey, string):
        rsa_key = (
            f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----")
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = self.b64tohex(
            (base64.b64encode(rsa.encrypt(f"{string}".encode(), pubkey))).decode())
        return result

    def login(self, session, username, password):
        url = "https://cloud.189.cn/api/portal/loginUrl.action?redirectURL=https://cloud.189.cn/web/redirect.html"
        r = session.get(url=url)
        captchatoken = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
        lt = re.findall(r'lt = "(.+?)"', r.text)[0]
        returnurl = re.findall(r"returnUrl = '(.+?)'", r.text)[0]
        paramid = re.findall(r'paramId = "(.+?)"', r.text)[0]
        j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
        session.headers.update({"lt": lt})

        username = self.rsa_encode(j_rsakey, username)
        password = self.rsa_encode(j_rsakey, password)
        url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0",
            "Referer": "https://open.e.189.cn/"
        }
        data = {
            "appKey": "cloud",
            "accountType": "01",
            "userName": f"{{RSA}}{username}",
            "password": f"{{RSA}}{password}",
            "validateCode": "",
            "captchaToken": captchatoken,
            "returnUrl": returnurl,
            "mailSuffix": "@189.cn",
            "paramId": paramid
        }
        r = session.post(url, data=data, headers=headers, timeout=5)
        if r.json()["result"] == 0:
            redirect_url = r.json()["toUrl"]
            session.get(url=redirect_url)
            return True
        else:
            return "登陆状态: " + r.json()["msg"]

    @staticmethod
    def sign(session):
        rand = str(round(time.time() * 1000))
        surl = f"https://api.cloud.189.cn/mkt/userSign.action?rand={rand}&clientType=TELEANDROID&version=8.6.3&model=SM-G930K"
        url = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN"
        url2 = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN"
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 \
                 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6",
            "Referer":
                "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
            "Host": "m.cloud.189.cn",
            "Accept-Encoding": "gzip, deflate"
        }
        response = session.get(url=surl, headers=headers)
        netdiskbonus = response.json().get("netdiskBonus")
        if response.json().get("isSign") == "false":
            msg = f"签到结果: 未签到，签到获得 {netdiskbonus}M 空间"
        else:
            msg = f"签到结果: 已经签到过了，签到获得 {netdiskbonus}M 空间"
        response = session.get(url=url, headers=headers)
        if "errorCode" in response.text:
            msg += f"\n第一次抽奖: {response.json().get('errorCode')}"
        else:
            description = response.json().get("description", "")
            if description in ["1", 1]:
                description = "50M空间"
            msg += f"\n第一次抽奖: 获得{description}"
        response = session.get(url=url2, headers=headers)
        if "errorCode" in response.text:
            msg += f"\n第二次抽奖: {response.json().get('errorCode')}"
        else:
            description = response.json().get("description", "")
            if description in ["1", 1]:
                description = "50M空间"
            msg += f"\n第二次抽奖: 获得{description}"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            phone = check_item.get("phone")
            password = check_item.get("password")
            session = requests.Session()
            flag = self.login(session=session, username=phone,
                              password=password)
            if flag is True:
                sign_msg = self.sign(session=session)
            else:
                sign_msg = flag
            msg = f"帐号信息: *******{phone[-4:]}\n{sign_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("CLOUD189", [])
    res = Cloud189(check_items=_check_items).main()
    print(res)
    send("天翼云盘", res)
