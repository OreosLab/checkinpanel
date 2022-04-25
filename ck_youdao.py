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
        if res.get("q") is None:
            return 0
        return res.get("q")

    def sign(self, cookie):
        msg = f"签到前空间: {int(self.get_space(cookie))//1048576}M\n"
        c = ""
        ad = 0
        headers = {"Cookie": cookie}
        r = requests.get(
            "http://note.youdao.com/login/acc/pe/getsess?product=YNOTE", headers=headers
        )
        for key, value in r.cookies.items():
            c += key + "=" + value + ";"
        headers = {"Cookie": c}
        re = requests.post(
            "https://note.youdao.com/yws/api/daupromotion?method=sync", headers=headers
        )
        if "error" not in re.text:
            res = requests.post(
                "https://note.youdao.com/yws/mapi/user?method=checkin", headers=headers
            )
            time.sleep(1)
            res2 = requests.post(
                "https://note.youdao.com/yws/mapi/user?method=checkin",
                headers=headers,
                data={"device_type": "android"},
            )
            for _ in range(3):
                resp = requests.post(
                    "https://note.youdao.com/yws/mapi/user?method=adRandomPrompt",
                    headers=headers,
                )
                ad += resp.json()["space"] // 1048576
                time.sleep(2)
            if "reward" in re.text:
                s = self.get_space(cookie)
                msg += f"签到后空间: {int(self.get_space(cookie))//1048576}M\n"
                sync = re.json()["rewardSpace"] // 1048576
                checkin = res.json()["space"] // 1048576
                checkin2 = res2.json()["space"] // 1048576
                space = str(sync + checkin + checkin2 + ad)
                msg += f"获得空间：{space}M, 总空间：{int(s)//1048576}M"
        else:
            msg += "错误" + str(re.json())
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
    _check_items = data.get("YOUDAO", [])
    res = YouDao(check_items=_check_items).main()
    send("有道云笔记", res)
