# -*- coding: utf-8 -*-
"""
cron: 51 9 * * *
new Env('什么值得买');
"""

from urllib.parse import quote, unquote

import requests

from notify_mtr import send
from utils import get_data


class Smzdm:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(session):
        try:
            current = session.get(
                url="https://zhiyou.smzdm.com/user/info/jsonp_get_current"
            ).json()
            if current["checkin"]["has_checkin"]:
                msg = (
                    f"用户信息: {current.get('nickname', '')}\n"
                    f"目前积分: {current.get('point', '')}\n"
                    f"经验值: {current.get('exp', '')}\n"
                    f"金币: {current.get('gold', '')}\n"
                    f"碎银子: {current.get('silver', '')}\n"
                    f"威望: {current.get('prestige', '')}\n"
                    f"等级: {current.get('level', '')}\n"
                    f"已经签到: {current.get('checkin', {}).get('daily_checkin_num', '')} 天"
                )
            else:
                data = (
                    session.get(
                        url="https://zhiyou.smzdm.com/user/checkin/jsonp_checkin"
                    )
                    .json()
                    .get("data", {})
                )
                msg = (
                    f"用户信息: {current.get('nickname', '')}\n"
                    f"目前积分: {data.get('point', '')}\n"
                    f"增加积分: {data.get('add_point', '')}\n"
                    f"经验值: {data.get('exp', '')}\n"
                    f"金币: {data.get('gold', '')}\n"
                    f"威望: {data.get('prestige', '')}\n"
                    f"等级: {data.get('rank', '')}\n"
                    f"已经签到: {data.get('checkin_num', {})} 天"
                )
        except Exception as e:
            msg = f"签到状态: 签到失败\n错误信息: {e}，请重新获取 cookie"
        return msg

    def main(self):
        msg_all = ""

        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: quote(unquote(item.split("=")[1]))
                for item in check_item.get("cookie").split("; ")
                if item.split("=")[0] == "sess"
            }
            session = requests.session()
            session.cookies.update(cookie)
            session.headers.update(
                {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "keep-alive",
                    "Host": "zhiyou.smzdm.com",
                    "Referer": "https://www.smzdm.com/",
                    "Sec-Fetch-Dest": "script",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
                }
            )
            msg = self.sign(session)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("SMZDM", [])
    result = Smzdm(check_items=_check_items).main()
    send("什么值得买", result)
