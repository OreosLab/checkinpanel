# -*- coding: utf-8 -*-
"""
cron: 7 11 * * *
new Env('掘金');
"""

import json

import requests

from notify_mtr import send
from utils import get_data


class Juejin:
    def __init__(self, check_items):
        self.check_items = check_items
        self.base_url = "https://api.juejin.cn/"
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        }

    def sign(self, cookie):
        sign_url = self.base_url + "growth_api/v1/check_in"
        res = requests.post(
            url=sign_url,
            headers=self.headers,
            cookies={"Cookie": cookie}
        ).content
        res = json.loads(res)
        return res

    def lottery(self, cookie):
        lottery_url = self.base_url + "growth_api/v1/lottery/draw"
        res = requests.post(
            url=lottery_url,
            headers=self.headers,
            cookies={"Cookie": cookie}
        ).content
        res = json.loads(res)
        return res

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            cookie = str(check_item.get("cookie"))
            sign_msg = self.sign(cookie=cookie)["err_msg"]
            lottery_msg = self.lottery(cookie=cookie)["err_msg"]
            msg = (
                f"账号 {i}\n------ 掘金签到结果 ------\n"
                + sign_msg
                + "\n------ 掘金抽奖结果 ------\n"
                + lottery_msg
            )
            i += 1
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("JUEJIN", [])
    res = Juejin(check_items=_check_items).main()
    print(res)
    send("掘金", res)
