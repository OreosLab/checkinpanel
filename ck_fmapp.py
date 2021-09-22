# -*- coding: utf-8 -*-
"""
cron: 30 14 * * *
new Env('Fa米家');
"""

import json

import requests

from notify_mtr import send
from utils import get_data


class FMAPP:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/market/member/signin/sign"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = (
                    f"在坚持{data.get('nextDay')}天即可获得{data.get('nextNumber')}个发米粒\n"
                    f"签到{data.get('lastDay')}天可获得{data.get('lastNumber')}个发米粒"
                )
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def user_info(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/info"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("nickName")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def mili_count(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/v1/mili/service/detail"
            response = requests.post(
                url=url,
                headers=headers,
                data=json.dumps({"pageSize": 10, "pageNo": 1})
            ).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("miliNum")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            token = check_item.get("token")
            cookie = check_item.get("cookie")
            blackbox = check_item.get("blackbox")
            device_id = check_item.get("device_id")
            fmversion = check_item.get("fmversion", "2.2.3")
            os = check_item.get("os", "ios")
            useragent = check_item.get("useragent", "Fa")
            headers = {
                "Accept": "*/*",
                "Accept-Language": "zh-Hans;q=1.0",
                "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
                "Host": "fmapp.chinafamilymart.com.cn",
                "Content-Type": "application/json",
                "loginChannel": "app",
                "token": token,
                "fmVersion": fmversion,
                "deviceId": device_id,
                "User-Agent": useragent,
                "os": os,
                "cookie": cookie,
                "blackBox": blackbox
            }
            sign_msg = self.sign(headers=headers)
            name_msg = self.user_info(headers=headers)
            mili_msg = self.mili_count(headers=headers)
            msg = f"帐号信息: {name_msg}\n签到状态: {sign_msg}\n米粒数量: {mili_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("FMAPP", [])
    res = FMAPP(check_items=_check_items).main()
    print(res)
    send("Fa米家", res)
