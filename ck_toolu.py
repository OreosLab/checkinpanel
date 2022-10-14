# -*- coding: utf-8 -*-
"""
cron: 0 6 * * *
new Env('在线工具');
"""

import re

import requests

from notify_mtr import send
from utils import get_data


class ToolLu:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        url = "https://id.tool.lu/sign"
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        response = requests.get(url, headers=headers)
        day = re.findall("你已经连续签到(.*)，再接再厉！", response.text)
        if len(day) == 0:
            return "cookie 失效"
        day = day[0].replace(" ", "")
        return f"连续签到 {day}"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            msg = self.sign(cookie)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("TOOLU", [])
    result = ToolLu(check_items=_check_items).main()
    send("在线工具", result)
