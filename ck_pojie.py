# -*- coding: utf-8 -*-
"""
cron: 53 11 * * *
new Env('吾爱破解');
"""

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data


class Pojie:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        result = ""
        headers = {
            "Cookie": cookie,
            "ContentType": "text/html;charset=gbk",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        requests.session().put(
            "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2", headers=headers
        )
        fa = requests.session().put(
            "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2", headers=headers
        )
        fb = BeautifulSoup(fa.text, "html.parser")
        fc = fb.find("div", id="messagetext").find("p").text
        if "您需要先登录才能继续本操作" in fc:
            result += "Cookie 失效"
        elif "恭喜" in fc:
            result += "签到成功"
        elif "不是进行中的任务" in fc:
            result += "不是进行中的任务"
        else:
            result += "签到失败"
        return result

    def main(self):
        i = 1
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            sign_msg = self.sign(cookie=cookie)
            msg = f"账号 {i} 签到状态: {sign_msg}"
            msg_all += msg + "\n\n"
            i += 1
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("POJIE", [])
    res = Pojie(check_items=_check_items).main()
    send("吾爱破解", res)
