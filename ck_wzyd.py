# -*- coding: utf-8 -*-
"""
cron: 00 8 * * *
new Env('王者营地');
"""

from urllib import parse

import requests

from notify_mtr import send
from utils import get_data


class WZYD:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(data):
        response = requests.post(
            url="https://ssl.kohsocialapp.qq.com:10001/play/h5sign",
            data=data).json()
        try:
            if response["result"] == 0:
                msg = "签到成功"
            else:
                msg = response["returnMsg"]
        except Exception:
            msg = "请求失败,请检查接口"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            data = check_item.get("data")
            data = {k: v[0] for k, v in parse.parse_qs(data).items()}
            try:
                user_id = data.get("userId", "")
            except Exception as e:
                print(f"获取用户信息失败: {e}")
                user_id = "未获取到用户信息"
            sign_msg = self.sign(data=data)
            msg = f"帐号信息: {user_id}\n签到信息: {sign_msg}"
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("WZYD", [])
    res = WZYD(check_items=_check_items).main()
    print(res)
    send('王者营地', res)
