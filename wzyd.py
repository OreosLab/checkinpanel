# -*- coding: utf-8 -*-
import json
import os
import time
from urllib import parse
from checksendNotify import send
import requests


class WZYDCheckIn:
    def __init__(self, check_item):
        self.check_item = check_item

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
        wzyd_data = self.check_item
        data = {k: v[0] for k, v in parse.parse_qs(wzyd_data).items()}
        try:
            user_id = data.get("userId", "")
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            user_id = "未获取到用户信息"
        sign_msg = self.sign(data=data)
        msg = f"帐号信息: {user_id}\n签到信息: {sign_msg}"
        return msg


if __name__ == "__main__":
    if 'wzyd' in os.environ:
        print('王者营地签到开始')
        text = WZYDCheckIn(check_item=os.environ.get('wzyd')).main()
        localtime = time.asctime(time.localtime(time.time()))
        result=f'当前时间{localtime}\n结果：{text}'
        send('王者营地签到',result)
    else:print('未找到变量请填入')