# -*- coding: utf-8 -*-
"""
cron: 7 21 * * *
new Env('智友邦');
"""

import re

import requests

from notify_mtr import send
from utils import get_data


class Zhiyoo:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(session):
        response = session.get(
            url="http://bbs.zhiyoo.net/plugin.php?id=dsu_paulsign:sign", verify=False
        )
        formhash = re.findall(
            r'<input type="hidden" name="formhash" value="(.*?)"', response.text
        )[0]
        data = {"formhash": formhash, "qdxq": "kx"}
        params = (
            ("id", "dsu_paulsign:sign"),
            ("operation", "qiandao"),
            ("infloat", "1"),
            ("inajax", "1"),
        )

        response = session.post(
            url="http://bbs.zhiyoo.net/plugin.php",
            params=params,
            data=data,
            verify=False,
        )
        user_resp = session.get(url="http://bbs.zhiyoo.net/home.php")
        uid = re.findall(r"uid=(\d+)\"", user_resp.text)
        uid = uid[0] if uid else "未获取到 UID"
        if "今日已经签到" in response.text:
            return f"用户信息: {uid}\n签到信息: 您今日已经签到，请明天再来！"

        check_msg = re.findall(r"恭喜你签到成功!获得随机奖励 金币 (\d+) 元.", response.text, re.S)
        check_msg = check_msg[0].strip() if check_msg else "签到失败"

        return f"用户信息: {uid}\n签到信息: 恭喜你签到成功!获得随机奖励 金币 {check_msg} 元."

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
                    "Origin": "http://bbs.zhiyoo.net",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54",
                    "Accept": "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/webp,image/apng,*/*;"
                    "q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Referer": "http://bbs.zhiyoo.net/plugin.php?id=dsu_paulsign:sign",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                }
            )
            msg = self.sign(session)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("ZHIYOO", [])
    result = Zhiyoo(check_items=_check_items).main()
    send("智友邦", result)
