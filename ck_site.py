# -*- coding: utf-8 -*-
"""
:author @gnodgl
cron: 11 6 * * *
new Env('Site');
"""

import json
import re
from json.decoder import JSONDecodeError

import requests

from notify_mtr import send
from utils import get_data

desp = ""
_print = print


def print(info):
    _print(info)
    global desp
    desp = desp + info + "\n\n"


class Site:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def generateHeader(url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": url
        }
        return header

    @staticmethod
    def cookieParse(cookiesStr):
        cookie_dict = {}
        cookies = cookiesStr.split(';')
        for cookie in cookies:
            cookie = cookie.split('=')
            cookie_dict[cookie[0]] = cookie[1]
        return cookie_dict

    @staticmethod
    def signin(session, url):
        # hdarea签到
        if url == "https://www.hdarea.co":
            attendance_url = url + "/sign_in.php"
            data = {"action": "sign_in"}
            with session.post(attendance_url, data) as res:
                r = re.compile(r"获得了\d+魔力值")
                r1 = re.compile(r"重复")
                print(res.text)
                if r.search(res.text):
                    tip = "签到成功"
                elif r1.search(res.text):
                    tip = "重复签到"
                else:
                    tip = "cookie 已过期或网站类型不对"
                print(f"{url} {tip}")
        # 猫站签到
        elif url == "https://pterclub.com":
            attendance_url = url + "/attendance-ajax.php"
            with session.get(attendance_url) as res:
                try:
                    msg = json.loads(res.text.encode("utf-8").decode("unicode-escape")).get("message")
                except JSONDecodeError:
                    msg = res.text
                if "连续签到" in msg:
                    tip = "签到成功"
                elif "重复刷新" in msg:
                    tip = "重复签到"
                else:
                    tip = "cookie 已过期或网站类型不对"
                print(f"{url} {tip}")
        # 海胆签到
        elif url == "https://www.haidan.video":
            attendance_url = url + "/signin.php"
            with session.get(attendance_url) as res:
                r = re.compile(r"已经打卡")
                r1 = re.compile(r"退出")
                if r.search(res.text):
                    tip = "签到成功"
                elif r1.search(res.text):
                    tip = "重复签到"
                else:
                    tip = "cookie 已过期或网站类型不对!"
                print(f"{url} {tip}")
        # bschool
        elif url == "https://pt.btschool.club":
            attendance_url = url + "/index.php?action=addbonus"
            with session.get(attendance_url) as res:
                r = re.compile(r"今天签到您获得\d+点魔力值")
                r1 = re.compile(r"退出")
                if r.search(res.text):
                    tip = "签到成功"
                elif r1.search(res.text):
                    tip = "重复签到"
                else:
                    tip = "cookie已过期"
                print(f"{url} {tip}")
        # lemonhd
        elif url == "https://lemonhd.org":
            attendance_url = url + "/attendance.php"
            with session.get(attendance_url) as res:
                r = re.compile(r"已签到")
                r1 = re.compile(r"请勿重复刷新")
                # print(res.text)
                if r.search(res.text):
                    tip = "签到成功"
                elif r1.search(res.text):
                    tip = "重复签到"
                else:
                    tip = "cookie 已过期或网站类型不对"
                print(f"{url} {tip}")
        else:
            attendance_url = url + "/attendance.php"
            with session.get(attendance_url) as res:
                r = re.compile(r"请勿重复刷新")
                r1 = re.compile(r"签到已得[\s]*\d+")
                if r.search(res.text):
                    tip = "重复签到"
                elif r1.search(res.text):
                    tip = "签到成功"
                else:
                    tip = "cookie 已过期或网站类型不对"
                print(f"{url} {tip}")

    @staticmethod
    # discuz 系列签到
    def signin_discuz_dsu(session, url):
        attendance_url = url + "/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
        hash_url = url + "/plugin.php?id=dsu_paulsign:sign"
        with session.get(hash_url) as hashurl:
            h = re.compile(r'name="formhash" value="(.*?)"')
            formhash = h.search(hashurl.text).group(1)
        data = {"qdmode": 3, "qdxq": "kx", "fastreply": 0, "formhash": formhash, "todaysay": ""}
        with session.post(attendance_url, data) as res:
            r = re.compile(r"签到成功")
            r1 = re.compile(r"已经签到")
            if r.search(res.text):
                print(f"{url} 签到成功")
            elif r1.search(res.text):
                print(f"{url} 重复签到")
            else:
                print(f"{url} {res.text}")

    @staticmethod
    # hifi 签到
    def signin_hifi(session, url):
        attendance_url = url + "/sg_sign.htm"
        with session.post(attendance_url) as res:
            r = re.compile(r"成功")
            r1 = re.compile(r"今天已经")
            if r.search(res.text):
                print(f"{url} 签到成功")
            elif r1.search(res.text):
                print(f"{url} 重复签到")
            else:
                print(f"{url} {res.text}")

    def main(self):
        s = requests.session()
        for check_item in self.check_items:
            url = check_item.get("url")
            type = check_item.get("type")
            cookie = self.cookieParse(check_item.get("cookie"))
            header = self.generateHeader(url)
            s.headers.update(header)
            s.cookies.update(cookie)
            if type == "pt":
                self.signin(s, url)
            elif type == "discuz":
                self.signin_discuz_dsu(s, url)
            elif type == "hifi":
                self.signin_hifi(s, url)
            else:
                print("请在配置文件中配置网站类型，如 type: 'pt'")
        return desp


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("Site", [])
    res = Site(check_items=_check_items).main()
    send("Site", res)
