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

    def sign(self, cookie):
        url = "https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1"
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Cookie': cookie
        }
        session = requests.session()
        resp = session.get(url, headers=headers)
        try:
            coin = re.findall("恩山币: </em>(.*?)nb &nbsp;", resp.text)[0]
            point = re.findall("<em>积分: </em>(.*?)<span", resp.text)[0]
            result = f"恩山币：{coin}\n积分：{point}"
        except Exception as e:
            result = str(e)
        return result

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            cookie = str(check_item.get("cookie"))
            result = self.sign(cookie=cookie)
            msg = f"账号{i}" + "\n------ 签到结果 ------\n" + result
            time.sleep(1)
            i += 1
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("ENSHAN", [])
    res = Enshan(check_items=_check_items).main()
    print(res)
    send("恩山论坛", res)
