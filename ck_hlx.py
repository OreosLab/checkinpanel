# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('葫芦侠');
"""

import hashlib
import json

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data


class HLX:
    def __init__(self, check_items):
        self.check_items = check_items

    def md5(self, password):
        m = hashlib.md5()
        b = password.encode(encoding="utf-8")
        m.update(b)
        password_md5 = m.hexdigest()
        return password_md5

    def login(self, username, password):
        password_md5 = self.md5(password)
        url = "https://floor.huluxia.com/account/login/IOS/4.0"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "account": username,
            "deviceCode": "",
            "device_code": "",
            "login_type": "2",
            "password": password_md5,
        }
        response = requests.post(url=url, data=data, headers=headers)
        key = json.loads(response.text)["_key"]
        nick = json.loads(response.text)["user"]["nick"]
        userID = json.loads(response.text)["user"]["userID"]
        msg = "[+]用户：" + nick + " userID：" + str(userID)
        return key, nick, userID, msg

    def get_level(self, userID, key):
        url = f"http://floor.huluxia.com/view/level?viewUserID={userID}&_key={key}"
        response = requests.post(url=url)
        soup = BeautifulSoup(response.text, "html.parser")  # 解析html页面
        level = soup.select(".lev_li_forth span")  # 筛选经验值
        msg = (
            "[+]当前经验值："
            + level[0].string
            + "\n[+]距离下一等级："
            + level[1].string
            + " 还需："
            + level[2].string
            + " 经验"
        )
        return msg

    def sign(self, key):
        # 获取所有板块 url
        url = "https://floor.huluxia.com/category/forum/list/IOS/1.0"
        # 获取所有板块下的内容 url
        ura = "https://floor.huluxia.com/category/forum/list/all/IOS/1.0"
        # 签到板块 url
        urs = "https://floor.huluxia.com/user/signin/IOS/1.1"
        # 获取所有板块
        categoryforum = requests.post(url).json()["categoryforum"]
        result = ""
        for i in categoryforum:
            # 获取所有板块下的内容
            categories = requests.post(url=ura, data={"fum_id": i["id"]}).json()[
                "categories"
            ]
            for cat in categories:
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
                res = requests.post(
                    url=urs,
                    data={"_key": key, "cat_id": cat["categoryID"]},
                    headers=headers,
                ).json()
                msg = res["msg"]
                status = res["status"]
                if status == 0:
                    result += "\n[+]" + cat["title"] + " 签到失败 错误原因：" + msg
                elif status == 1:
                    result += (
                        "\n[+]"
                        + cat["title"]
                        + " 签到成功 获得经验："
                        + str(res["experienceVal"])
                    )
        return result

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")
            key, nick, userID, login_msg = self.login(username, password)
            level_msg = self.get_level(userID, key)
            sign_msg = self.sign(key)
            msg = login_msg + "\n" + level_msg + sign_msg
            msg_all += msg + "\n\n"
        return msg_all


def start():
    data = get_data()
    _check_items = data.get("HLX", [])
    res = HLX(check_items=_check_items).main()
    send("葫芦侠", res)


if __name__ == "__main__":
    start()
