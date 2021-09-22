# -*- coding: utf-8 -*-

import requests

from notify_mtr import send
from utils import get_data


class KJWJ:
    def __init__(self, check_items):
        self.check_items = check_items

    def login(self, usr, pwd):
        login_url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token'
        headers = {
            'user-agent':
                'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'
        }
        data = {
            'nickname': '',
            'username': usr,
            'password': pwd,
            'code': '',
            'img_code': '',
            'invitation_code': '',
            'token': '',
            'smsToken': '',
            'luoToken': '',
            'confirmPassword': '',
            'loginType': ''
        }
        res = requests.post(login_url, headers=headers, data=data)
        if res.status_code == 200:
            status = res.json()
            login_stat = f"账号：{status.get('name')} 登陆成功"
            id = f"ID：{status.get('id')}"
            coin = f"金币：{status.get('credit')}"
            level = f"等级：{status.get('lv').get('lv').get('name')}"
            token = status.get('token')
            check_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
            check_head = {
                'authorization':
                    f'Bearer {token}',
                'origin':
                    'https://www.kejiwanjia.com',
                'referer':
                    'https://www.kejiwanjia.com/task',
                'user-agent':
                    'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'
            }
            resp = requests.post(check_url, headers=check_head)
            if resp.status_code == 200:
                info = resp.json()
                # print(info)
                if 'date' in info:
                    sign_info = f"签到成功：{info.get('credit')} 金币"
                else:
                    sign_info = f"已经签到：{info}金币"
        else:
            sign_info = '账号登陆失败: 账号或密码错误'
        return login_stat, id, coin, level, sign_info

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            username = str(check_item.get("username"))
            password = str(check_item.get("password"))
            login_stat, id, coin, level, sign_info = self.login(
                usr=username, pwd=password)
            msg = (
                f"===> 账号{i} 开始 <==="
                f"\n{login_stat}"
                f"\n{id}"
                f"\n{coin}"
                f"\n{level}"
                "\n===> 签到信息 <===\n"
                f"{sign_info}"
            )
            i += 1
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == '__main__':
    data = get_data()
    _check_items = data.get("KJWJ", [])
    res = KJWJ(check_items=_check_items).main()
    print(res)
    send("科技玩家", res)
