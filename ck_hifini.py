# -*- coding: utf-8 -*-
"""
cron: 0 0 0 * * *
new Env('HiFiNi');
"""

import requests

from notify_mtr import send
from utils import get_data


class HiFiNi(object):
    def __init__(self, check_items):
        self.check_items = check_items

    def signin(self, cookies):
        sign_in_url = "https://www.hifini.com/sg_sign.htm"
        data = {"x-requested-with": "XMLHttpRequest"}
        cookies = {"enwiki_session": f"{cookies}"}
        r1 = requests.post(url=sign_in_url, data=data, cookies=cookies)
        html_text = r1.text
        is_sign = False
        for line in html_text.splitlines():
            if line.find("今天已经签过啦") != -1:
                msg = "今天已经签过啦"
                is_sign = True
        if not is_sign:
            msg = "签到成功!"
        return msg

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            msg = f"账号{i}\n{self.signin(cookie)}"
            i += 1
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("HIFINI", [])
    res = HiFiNi(check_items=_check_items).main()
    print(res)
    send("HiFiNi", res)
