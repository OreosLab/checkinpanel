# -*- coding: utf-8 -*-
"""
cron: 12 13 * * *
new Env('咔叽网单');
"""

import re

import requests

from notify_mtr import send
from utils import get_data


class WWW2nzz:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(session):
        response = session.get("http://www.2nzz.com/index.php", verify=False)
        formhash = re.findall(
            r'<input type="hidden" name="formhash" value="(.*?)"', response.text
        )[0]
        data = {
            "formhash": formhash,
            "qdxq": "kx",
            "qdmode": "2",
            "todaysay": "",
            "fastreply": "0",
        }
        params = (
            ("id", "dsu_paulsign:sign"),
            ("operation", "qiandao"),
            ("infloat", "1"),
            ("sign_as", "1"),
            ("inajax", "1"),
        )
        response = session.post(
            "http://www.2nzz.com/plugin.php", data, params=params, verify=False
        )

        user_resp = session.get(url="http://www.2nzz.com/home.php")
        uid = re.findall(r"uid=(\d+)\"", user_resp.text)
        uid = uid[0] if uid else "未获取到 UID"

        if "您今天已经签到过了或者签到时间还未开始" in response.text:
            return f"用户信息: {uid}\n签到信息: 您今天已经签到过了或者签到时间还未开始"

        check_msg = re.findall(r"<div class=\"c\">(.*?)</div>", response.text, re.S)
        check_msg = check_msg[0].strip() if check_msg else "签到失败"

        return f"用户信息: {uid}\n签到信息: {check_msg}"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }
            session = requests.session()
            session.cookies.update(cookie)
            session.headers.update(
                {
                    "Origin": "http://www.2nzz.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
                    "Accept": "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/webp,image/apng,*/*;"
                    "q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Referer": "http://www.2nzz.com/index.php",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                }
            )
            msg = self.sign(session)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("WWW2NZZ", [])
    result = WWW2nzz(check_items=_check_items).main()
    send("咔叽网单", result)
