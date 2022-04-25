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

    def sign(self, cookie):
        session = requests.Session()
        url = "https://id.tool.lu/sign"
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        response = session.get(url=url, headers=headers)
        day = re.findall("你已经连续签到(.*)，再接再厉！", response.text)
        if len(day) == 0:
            msg = "cookie 失效"
        else:
            day = day[0].replace(" ", "")
            msg = f"连续签到 {day}"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            msg = self.sign(cookie)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("TOOLU", [])
    res = ToolLu(check_items=_check_items).main()
    send("在线工具", res)
