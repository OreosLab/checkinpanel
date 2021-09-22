# -*- coding: utf-8 -*-
"""
cron: 12 13 * * *
new Env('咔叽网单');
"""

import re

import requests
import urllib3

from notify_mtr import send
from utils import get_data

urllib3.disable_warnings()


class WWW2nzz:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(session):
        response = session.get(url="http://www.2nzz.com/index.php",
                               verify=False)
        formhash = re.findall(
            r'<input type="hidden" name="formhash" value="(.*?)"',
            response.text
        )[0]
        params = (
            ("id", "dsu_paulsign:sign"),
            ("operation", "qiandao"),
            ("infloat", "1"),
            ("sign_as", "1"),
            ("inajax", "1"),
        )
        data = {
            "formhash": formhash,
            "qdxq": "kx",
            "qdmode": "2",
            "todaysay": "",
            "fastreply": "0"
        }
        response = session.post(url="http://www.2nzz.com/plugin.php",
                                params=params,
                                data=data,
                                verify=False)
        user_rep = session.get(url="http://www.2nzz.com/home.php")
        uid = re.findall(r"uid=(\d+)\"", user_rep.text)
        uid = uid[0] if uid else "未获取到 UID"
        if "您今天已经签到过了或者签到时间还未开始" in response.text:
            msg = f"用户信息: {uid}\n签到信息: 您今天已经签到过了或者签到时间还未开始"
        else:
            check_msg = re.findall(
                r"<div class=\"c\">(.*?)</div>",
                response.text, re.S
            )
            check_msg = check_msg[0].strip() if check_msg else "签到失败"
            msg = f"用户信息: {uid}\n签到信息: {check_msg}"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }
            session = requests.session()
            requests.utils.add_dict_to_cookiejar(session.cookies, cookie)
            session.headers.update({
                "Origin": "http://www.2nzz.com",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
                "Accept":
                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Referer": "http://www.2nzz.com/index.php",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            })
            msg = self.sign(session=session)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("WWW2NZZ", [])
    res = WWW2nzz(check_items=_check_items).main()
    print(res)
    send("咔叽网单", res)
