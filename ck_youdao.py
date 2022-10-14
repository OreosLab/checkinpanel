# -*- coding: utf-8 -*-
"""
cron: 18 20 * * *
new Env('有道云笔记');
"""

import time

import requests

from notify_mtr import send
from utils import get_data


class YouDao:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def get_space(cookie):
        url = "https://note.youdao.com/yws/mapi/user?method=get"
        headers = {"Cookie": cookie}
        res = requests.get(url=url, headers=headers).json()
        return 0 if res.get("q") is None else res.get("q")

    def sign(self, cookie):
        msg = f"签到前空间: {int(self.get_space(cookie))//1048576}M\n"
        ad = 0

        headers = {"Cookie": cookie}
        r = requests.get(
            "http://note.youdao.com/login/acc/pe/getsess?product=YNOTE", headers=headers
        )
        c = "".join(f"{key}={value};" for key, value in r.cookies.items())
        headers = {"Cookie": c}

        r2 = requests.post(
            "https://note.youdao.com/yws/api/daupromotion?method=sync", headers=headers
        )
        if "error" not in r2.text:
            checkin1 = requests.post(
                "https://note.youdao.com/yws/mapi/user?method=checkin", headers=headers
            )
            time.sleep(1)
            checkin2 = requests.post(
                "https://note.youdao.com/yws/mapi/user?method=checkin",
                {"device_type": "android"},
                headers=headers,
            )

            for _ in range(3):
                resp = requests.post(
                    "https://note.youdao.com/yws/mapi/user?method=adRandomPrompt",
                    headers=headers,
                )
                ad += resp.json()["space"] // 1048576
                time.sleep(2)

            if "reward" in r2.text:
                s = self.get_space(cookie)
                msg += f"签到后空间: {int(s)//1048576}M\n"
                sync = r2.json()["rewardSpace"] // 1048576
                checkin_1 = checkin1.json()["space"] // 1048576
                checkin_2 = checkin2.json()["space"] // 1048576
                space = str(sync + checkin_1 + checkin_2 + ad)
                msg += f"获得空间：{space}M, 总空间：{int(s)//1048576}M"
        else:
            msg += f"错误 {str(r2.json())}"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            msg = self.sign(cookie)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("YOUDAO", [])
    result = YouDao(check_items=_check_items).main()
    send("有道云笔记", result)
