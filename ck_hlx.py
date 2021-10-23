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

    def login(self, password, username):
        password_md5 = self.md5(password)
        url = "http://floor.huluxia.com/account/login/ANDROID/4.0?device_code=1"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "account": username,
            "login_type": "2",
            "password": password_md5,
        }
        response = requests.post(url=url, data=data, headers=headers)
        key = json.loads(response.text)["_key"]
        nick = json.loads(response.text)["user"]["nick"]
        userID = json.loads(response.text)["user"]["userID"]
        msg = "[+]用户：" + nick + ";userID:" + str(userID)
        return key, nick, userID, msg

    def get_level(self, userID, key):
        url = f"http://floor.huluxia.com/view/level?viewUserID={userID}&_key={key}"
        response = requests.post(url=url)
        soup = BeautifulSoup(response.text, "html.parser")  # 解析html页面
        level = soup.select(".lev_li_forth span")  # 筛选经验值
        msg = (
            "[+]当前经验值:"
            + level[0].string
            + "\n[+]距离下一等级:"
            + level[1].string
            + "还需:"
            + level[2].string
            + "经验"
        )
        return msg

    def sign(self, key):
        url = "https://floor.huluxia.com/category/list/ANDROID/2.0"
        response = requests.get(url=url)
        categories = json.loads(response.text)["categories"]
        count = 0  # 签到次数
        for list in categories:
            categoryID = list["categoryID"]
            title = list["title"]
            url = f"https://floor.huluxia.com/user/signin/ANDROID/4.0?_key={key}&cat_id={categoryID}"
            response = requests.get(url=url)
            msg = json.loads(response.text)["msg"]
            status = json.loads(response.text)["status"]
            if status == 0:
                msg = "[+]" + msg
            if status == 1:
                count += 1
                msg = "[+]板块" + str(count) + "：" + title + " 签到成功"
        msg += "\n[+]共计签到" + str(count) + "个板块"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")
            key, nick, userID, login_msg = self.login(username, password)
            level_msg = self.get_level(userID, key)
            sign_msg = self.sign(key)
            msg = login_msg + "\n" + level_msg + "\n" + sign_msg
            msg_all += msg + "\n\n"
        return msg_all


def start():
    data = get_data()
    _check_items = data.get("HLX", [])
    res = HLX(check_items=_check_items).main()
    send("葫芦侠", res)


if __name__ == "__main__":
    start()
