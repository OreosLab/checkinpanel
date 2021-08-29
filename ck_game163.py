# -*- coding: utf-8 -*-
"""
cron: 20 8 * * *
new Env('网易云游戏');
"""

import json, requests
from getENV import getENv
from checksendNotify import send


class Game163Checkin:
    def __init__(self, GAME163_AUTH_LIST):
        self.game163_auth_list = game163_auth_list

    @staticmethod
    def game163(Authorization):
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36',
            'Authorization': Authorization
        }
        url = 'http://n.cg.163.com/api/v2/sign-today'
        r = requests.post(url, headers=headers).text
        if r[0] == "{":
            return "cookie 已失效"
        else:
            return "签到成功"

    def main(self):
        msg_all = ""
        for game163_auth in self.game163_auth_list:
            Authorization = str(game163_auth.get("Authorization"))
            msg = self.game163(Authorization=Authorization)
            msg_all += msg + '\n\n'
        return msg_all

def start():
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    _game163_auth_list = datas.get("GAME163_AUTH_LIST", [])
    res = Game163Checkin(game163_auth_list=_game163_auth_list).main()
    print(res)
    send("网易云游戏", res)

if __name__ == "__main__":
    start()