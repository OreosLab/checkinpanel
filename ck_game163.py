# -*- coding: utf-8 -*-
"""
cron: 20 8 * * *
new Env('网易云游戏');
"""

import requests

from notify_mtr import send
from utils import get_data


class Game163:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def checkin(authorization):
        url = "http://n.cg.163.com/api/v2/sign-today"
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Build/QKQ1.190825.002; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
            "Chrome/85.0.4183.127 Mobile Safari/537.36",
            "authorization": authorization,
        }
        res = requests.post(url, headers=headers).text
        return "cookie 已失效" if res[0] == "{" else "签到成功"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            authorization = str(check_item.get("authorization"))
            msg = self.checkin(authorization)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("GAME163", [])
    result = Game163(check_items=_check_items).main()
    send("网易云游戏", result)
