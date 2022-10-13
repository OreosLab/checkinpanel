# -*- coding: utf-8 -*-
"""
cron: 30 14 * * *
new Env('Fa米家');
"""

import requests

from notify_mtr import send
from utils import get_data


class FMAPP:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(headers):
        try:
            url = (
                "https://fmapp.chinafamilymart.com.cn/api/app/market/member/signin/sign"
            )
            res = requests.post(url, headers=headers).json()
            if res.get("code") == "200":
                data = res.get("data", {})
                msg = (
                    f"再坚持 {data.get('nextDay')} 天即可获得 {data.get('nextNumber')} 个发米粒\n"
                    f"签到 {data.get('lastDay')} 天可获得 {data.get('lastNumber')} 个发米粒"
                )
            else:
                msg = res.get("message")
        except Exception as e:
            print("错误信息", e)
            msg = f"未知错误：{e}"
        return msg

    @staticmethod
    def user_info(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/info"
            res = requests.post(url, headers=headers).json()
            if res.get("code") == "200":
                msg = res.get("data", {}).get("nickName")
            else:
                msg = res.get("message")
        except Exception as e:
            print("错误信息", e)
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def mili_count(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/v1/mili/service/detail"
            res = requests.post(
                url, headers=headers, json={"pageSize": 10, "pageNo": 1}
            ).json()
            if res.get("code") == "200":
                msg = res.get("data", {}).get("miliNum")
            else:
                msg = res.get("message")
        except Exception as e:
            print("错误信息", e)
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
                "blackBox": blackbox,
            }
            sign_msg = self.sign(headers)
            name_msg = self.user_info(headers)
            mili_msg = self.mili_count(headers)
            msg = f"帐号信息: {name_msg}\n签到状态: {sign_msg}\n米粒数量: {mili_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("FMAPP", [])
    result = FMAPP(check_items=_check_items).main()
    send("Fa米家", result)
