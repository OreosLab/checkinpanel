# -*- coding: utf-8 -*-
"""
cron: 51 9 * * *
new Env('什么值得买APP');
"""


import requests
import json
import time
import hashlib

from notify_mtr import send
from utils import get_data


class Smzdm:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        try:
            ts = int(round(time.time() * 1000))
            url = 'https://user-api.smzdm.com/robot/token'
            headers = {
                'Host': 'user-api.smzdm.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'{cookie}',
                'User-Agent': 'smzdm_android_V10.4.1 rv:841 (22021211RC;Android12;zh)smzdmapp',
            }
            data = {
                "f": "android",
                "v": "10.4.1",
                "weixin": 1,
                "time": ts,
                "sign": hashlib.md5(bytes(f'f=android&time={ts}&v=10.4.1&weixin=1&key=apr1$AwP!wRRT$gJ/q.X24poeBInlUJC', encoding='utf-8')).hexdigest().upper()
            }
            html = requests.post(url=url, headers=headers, data=data)
            res = html.json()
            token = res['data']['token']

            Timestamp = int(round(time.time() * 1000))
            data = {
                "f": "android",
                "v": "10.4.1",
                "sk": "ierkM0OZZbsuBKLoAgQ6OJneLMXBQXmzX+LXkNTuKch8Ui2jGlahuFyWIzBiDq/L",
                "weixin": 1,
                "time": Timestamp,
                "token": token,
                "sign": hashlib.md5(bytes(f'f=android&sk=ierkM0OZZbsuBKLoAgQ6OJneLMXBQXmzX+LXkNTuKch8Ui2jGlahuFyWIzBiDq/L&time={Timestamp}&token={token}&v=10.4.1&weixin=1&key=apr1$AwP!wRRT$gJ/q.X24poeBInlUJC', encoding='utf-8')).hexdigest().upper()
            }
            url = 'https://user-api.smzdm.com/checkin'
            url2 = 'https://user-api.smzdm.com/checkin/all_reward'
            headers = {
                'Host': 'user-api.smzdm.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'{cookie}',
                'User-Agent': 'smzdm_android_V10.4.1 rv:841 (22021211RC;Android12;zh)smzdmapp',
            }
            html = requests.post(url=url, headers=headers, data=data)
            html2 = requests.post(url=url2, headers=headers, data=data)
            res = json.loads(html.text)
            res2 = json.loads(html2.text)
            if res2['error_code'] == '0':
                msg = res2["title"] + res2["sub_title"]
            else:
                msg = res['error_msg']
        except Exception as e:
            msg = f"签到状态: 签到失败\n错误信息: {e}，请重新获取 cookie"
        return msg

    def main(self):
        msg_all = ""

        for check_item in self.check_items:
            msg = self.sign(check_item.get("cookie"))
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("SMZDM", [])
    result = Smzdm(check_items=_check_items).main()
    send("什么值得买APP", result)
