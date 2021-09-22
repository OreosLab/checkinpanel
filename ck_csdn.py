# -*- coding: utf-8 -*-
"""
cron: 30 10 * * *
new Env('CSDN');
"""

import requests

from notify_mtr import send
from utils import get_data


class CSDN:
    def __init__(self, check_items):
        self.check_items = check_items
        self.headers = {
            "user-agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74"
        }

    def sign(self, cookies):
        url = "https://me.csdn.net/api/LuckyDraw_v2/signIn"
        response = requests.get(
            url=url, headers=self.headers, cookies=cookies).json()
        if response.get("code") == 200:
            msg = response.get("data").get("msg")
        else:
            msg = "签到失败"
            print(response)
        return msg

    def draw(self, cookies):
        url = "https://me.csdn.net/api/LuckyDraw_v2/goodluck"
        response = requests.get(
            url=url, headers=self.headers, cookies=cookies).json()
        if response.get("code") == 200:
            msg = response.get("data").get("msg")
        else:
            msg = "抽奖失败"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }
            try:
                user_name = cookie.get("UserName", "")
            except Exception as e:
                print(f"获取用户信息失败: {e}")
                user_name = "未获取到用户信息"
            sign_msg = self.sign(cookies=cookie)
            draw_msg = self.draw(cookies=cookie)
            msg = f"帐号信息: {user_name}\n签到信息: {sign_msg}\n抽奖结果: {draw_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("CSDN", [])
    res = CSDN(check_items=_check_items).main()
    print(res)
    send("CSDN", res)
