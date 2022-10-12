# -*- coding: utf-8 -*-
"""
cron: 55 18 * * *
new Env('CCAVA');
"""

import requests

from notify_mtr import send
from utils import get_data


class CCAVA:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        url = "https://pc.ccava.net/zb_users/plugin/mochu_us/cmd.php?act=qiandao"
        res = requests.get(url, headers={"Cookie": cookie}).json()
        if "登录" in res["msg"]:
            return "cookie 失效"
        if "今天" in res["msg"]:
            return f'重复签到，剩余 {res["giod"]} 月光币'
        return f'签到成功，剩余 {res["giod"]} 月光币'

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            msg = self.sign(cookie)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("CCAVA", [])
    result = CCAVA(check_items=_check_items).main()
    send("CCAVA", result)
