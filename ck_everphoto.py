# -*- coding: utf-8 -*-
"""
:author @CAB233
:url https://github.com/CAB233/everphoto_checkin
cron: 3 22 * * *
new Env('时光相册');
"""

import json

import requests

from notify_mtr import send
from utils import get_data


class EverPhoto:
    def __init__(self, check_items):
        self.check_items = check_items

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            mobile = check_item.get("mobile")
            password = check_item.get("password")
            header = {}
            url = "https://api.everphoto.cn/users/self/checkin/v2"
            login_url = "https://web.everphoto.cn/api/auth"
            login_key = f"mobile={mobile}&password={password}"
            login_res = requests.post(login_url, data=login_key, headers=header)
            login_data = json.loads(login_res.text)["data"]
            header["authorization"] = "Bearer "+login_data["token"]

            response = requests.post(url, headers=header)
            data = json.loads(response.text)
            checkin_result = data["data"]["checkin_result"]
            continuity = data["data"]["continuity"]

            msg = (
                "是否为今日第一次签到："
                + str(checkin_result)
                + "\n"
                + "累积签到天数："
                + str(continuity)
            )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("EVERPHOTO", [])
    res = EverPhoto(check_items=_check_items).main()
    print(res)
    send("时光相册", res)
