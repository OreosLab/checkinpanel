# -*- coding: utf-8 -*-
"""
:author @CAB233
:url https://github.com/CAB233/everphoto_checkin
cron: 3 22 * * *
new Env('时光相册');
"""

import requests

from notify_mtr import send
from utils import get_data


class EverPhoto:
    def __init__(self, check_items):
        self.check_items = check_items

    def main(self):
        msg_all = ""
        url = "https://openapi.everphoto.cn/sf/3/v4/PostCheckIn"
        login_url = "https://web.everphoto.cn/api/auth"
        for check_item in self.check_items:
            mobile = check_item.get("mobile")
            password = check_item.get("password")

            login_key = f"mobile={mobile}&password={password}"
            header = {
                "user-agent": "EverPhoto/4.5.0 (Android;4050002;MuMu;23;dev)",
                "application": "tc.everphoto",
            }
            data = requests.post(login_url, login_key, headers=header).json()["data"]

            header = {
                "user-agent": "EverPhoto/4.5.0 (Android;4050002;MuMu;23;dev)",
                "application": "tc.everphoto",
                "content-type": "application/json",
                "host": "openapi.everphoto.cn",
                "connection": "Keep-Alive",
                "authorization": f'Bearer {data["token"]}',
            }

            res = requests.post(url, headers=header).json()
            checkin_result = res["data"]["checkin_result"]
            continuity = res["data"]["continuity"]

            msg = f"是否为今日第一次签到：{checkin_result}\n累积签到天数：{continuity}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("EVERPHOTO", [])
    result = EverPhoto(check_items=_check_items).main()
    send("时光相册", result)
