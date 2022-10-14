# -*- coding: utf-8 -*-
"""
cron: 00 8 * * *
new Env('王者营地');
"""

from urllib.parse import parse_qsl

import requests

from notify_mtr import send
from utils import get_data


class WZYD:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(data):
        res = requests.post(
            url="https://ssl.kohsocialapp.qq.com:10001/play/h5sign", data=data
        ).json()
        try:
            msg = "签到成功" if res["result"] == 0 else res["returnMsg"]
        except Exception:
            msg = "请求失败，请检查接口"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            data = dict(parse_qsl(check_item.get("data")))
            try:
                user_id = data.get("userId", "")
            except Exception as e:
                print(f"获取用户信息失败: {e}")
                user_id = "未获取到用户信息"
            sign_msg = self.sign(data)
            msg = f"帐号信息: {user_id}\n签到信息: {sign_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("WZYD", [])
    result = WZYD(check_items=_check_items).main()
    send("王者营地", result)
