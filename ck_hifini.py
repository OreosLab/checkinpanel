# -*- coding: utf-8 -*-
"""
cron: 0 0 0 * * *
new Env('HiFiNi');
"""

import requests

from notify_mtr import send
from utils import get_data


class HiFiNi:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def signin(cookies):
        sign_in_url = "https://www.hifini.com/sg_sign.htm"
        data = {"x-requested-with": "XMLHttpRequest"}
        cookies = {"enwiki_session": f"{cookies}"}
        r1 = requests.post(sign_in_url, data=data, cookies=cookies)
        html_text = r1.text
        is_sign = False
        msg = ""
        for line in html_text.splitlines():
            if line.find("今天已经签过啦") != -1:
                msg = "今天已经签过啦"
                is_sign = True
        if not is_sign:
            msg = "签到成功!"
        return msg

    def main(self):
        msg_all = ""
        for i, check_item in enumerate(self.check_items, start=1):
            cookie = check_item.get("cookie")
            msg = f"账号{i}\n{self.signin(cookie)}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("HIFINI", [])
    result = HiFiNi(check_items=_check_items).main()
    send("HiFiNi", result)
