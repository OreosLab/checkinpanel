# -*- coding: utf-8 -*-
"""
cron: 1 15 * * *
new Env('恩山论坛');
"""

import re
import time

import requests

from notify_mtr import send
from utils import get_data


class Enshan:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        url = (
            "https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1"
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/92.0.4515.131 Safari/537.36",
            "Cookie": cookie,
        }
        session = requests.session()
        response = session.get(url, headers=headers)
        try:
            coin = re.findall("恩山币: </em>(.*?)nb &nbsp;", response.text)[0]
            point = re.findall("<em>积分: </em>(.*?)<span", response.text)[0]
            res = f"恩山币：{coin}\n积分：{point}"
        except Exception as e:
            res = str(e)
        return res

    def main(self):
        msg_all = ""
        for i, check_item in enumerate(self.check_items, start=1):
            cookie = str(check_item.get("cookie"))
            msg = f"账号{i}\n------ 签到结果 ------\n{self.sign(cookie)}"
            time.sleep(1)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("ENSHAN", [])
    result = Enshan(check_items=_check_items).main()
    send("恩山论坛", result)
