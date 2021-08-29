# -*- coding: utf-8 -*-
"""
cron: 00 8 * * *
new Env('王者营地');
"""

import json, os, requests
from urllib import parse
from getENV import getENv
from checksendNotify import send


class WZYDCheckIn:
    def __init__(self, wzyd_data_list):
        self.wzyd_data_list = wzyd_data_list

    @staticmethod
    def sign(data):
        response = requests.post(url="https://ssl.kohsocialapp.qq.com:10001/play/h5sign", data=data).json()
        try:
            if response["result"] == 0:
                msg = "签到成功"
            else:
                msg = response["returnMsg"]
        except:
            msg = "请求失败,请检查接口"
        return msg

    def main(self):
        msg_all = ""
        for wzyd_data in self.wzyd_data_list:
            wzyd_data = self.wzyd_data.get("wzyd_data")
            data = {k: v[0] for k, v in parse.parse_qs(wzyd_data).items()}
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
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    _wzyd_data_list = datas.get("WZYD_DATA_LIST", [])
    res = WZYDCheckIn(wzyd_data_list=_wzyd_data_list).main()
    print(res)
    send('王者营地', res)