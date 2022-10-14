# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('葫芦侠');
"""

import hashlib

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data


class HLX:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def md5(password):
        m = hashlib.md5()
        b = password.encode(encoding="utf-8")
        m.update(b)
        return m.hexdigest()

    def login(self, username, password):
        password_md5 = self.md5(password)
        url = "https://floor.huluxia.com/account/login/IOS/4.0"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "account": username,
            "deviceCode": "",
            "device_code": "",
            "login_type": "2",
            "password": password_md5,
        }
        res = requests.post(url, data=data, headers=headers).json()
        key = res["_key"]
        nick = res["user"]["nick"]
        userID = res["user"]["userID"]
        msg = f"[+]用户: {nick} ({userID})"
        return key, userID, msg

    @staticmethod
    def get_level(userID, key):
        url = f"http://floor.huluxia.com/view/level?viewUserID={userID}&_key={key}"
        response = requests.post(url)
        soup = BeautifulSoup(response.text, "html.parser")  # 解析 html 页面
        level = soup.select(".lev_li_forth span")  # 筛选经验值
        return (
            f"[+]当前经验: {level[0].string}\n"
            f"[+]距下一级: {level[1].string} 还需：{level[2].string} 经验"
        )

    @staticmethod
    def sign(key):
        # 获取所有板块 url
        url = "https://floor.huluxia.com/category/forum/list/IOS/1.0"
        # 获取所有板块下的内容 url
        url_all = "https://floor.huluxia.com/category/forum/list/all/IOS/1.0"
        # 签到板块 url
        sign_url = "https://floor.huluxia.com/user/signin/IOS/1.1"
        # 获取所有板块
        result = ""
        for i in requests.post(url).json()["categoryforum"]:
            # 获取所有板块下的内容
            res = requests.post(url_all, data={"fum_id": i["id"]}).json()
            for cat in res["categories"]:
                headers = {
                    "Host": "floor.huluxia.com",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "Floor/1.3.0 (iPhone; iOS 15.3; Scale/3.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "304",
                    "Accept-Encoding": "gzip, deflate, br",
                }
                res2 = requests.post(
                    sign_url,
                    data={"_key": key, "cat_id": cat["categoryID"]},
                    headers=headers,
                ).json()
                if res2["status"] == 0:
                    result += f'\n[+]{cat["title"]} 签到失败 错误原因：{res2["msg"]}'
                elif res2["status"] == 1:
                    result += f'\n[+]{cat["title"]} 签到成功 获得经验：{res2["experienceVal"]}'
        return result

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")
            key, userID, login_msg = self.login(username, password)
            level_msg = self.get_level(userID, key)
            sign_msg = self.sign(key)
            msg = login_msg + "\n" + level_msg + sign_msg
            msg_all += msg + "\n\n"
        return msg_all


def start():
    _data = get_data()
    _check_items = _data.get("HLX", [])
    result = HLX(check_items=_check_items).main()
    send("葫芦侠", result)


if __name__ == "__main__":
    start()
