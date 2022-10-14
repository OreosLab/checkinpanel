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


def log(info):
    global desp
    desp = desp + info + "\n\n"


class Site:
    def __init__(self, check_items):
        self.check_items = check_items
        self.error_tip = "cookie 已过期或网站类型不对"
        self.url = ""

    @staticmethod
    def generate_headers(url):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": url,
        }

    @staticmethod
    def cookie_parse(cookie_str):
        cookie_dict = {}
        cookies = cookie_str.split(";")
        for cookie in cookies:
            cookie = cookie.split("=")
            cookie_dict[cookie[0]] = cookie[1]
        return cookie_dict

    def signin(self, session, url):
        # hdarea 签到
        if url == "https://www.hdarea.co":
            attendance_url = f"{url}/sign_in.php"
            data = {"action": "sign_in"}
            with session.post(attendance_url, data) as response:
                r = re.compile(r"获得了\d+魔力值")
                r1 = re.compile(r"重复")
                log(response.text)
                if r.search(response.text):
                    tip = "签到成功"
                elif r1.search(response.text):
                    tip = "重复签到"
                else:
                    tip = self.url
                    print(f"{url} {tip}")
                log(f"{url} {tip}")
        elif url == "https://pterclub.com":
            attendance_url = f"{url}/attendance-ajax.php"
            with session.get(attendance_url) as response:
                try:
                    msg = json.loads(
                        response.text.encode("utf-8").decode("unicode-escape")
                    ).get("message")
                except JSONDecodeError:
                    msg = response.text
                if "连续签到" in msg:
                    pattern = re.compile(r"</?.>")
                    tip = f"签到成功, {re.sub(pattern, '', msg)}"
                elif "重复刷新" in msg:
                    tip = "重复签到"
                else:
                    tip = self.url
                    print(f"{url} {tip}")
                log(f"{url} {tip}")
        elif url == "https://www.haidan.video":
            attendance_url = f"{url}/signin.php"
            with session.get(attendance_url) as response:
                r = re.compile(r"已经打卡")
                r1 = re.compile(r"退出")
                if r.search(response.text):
                    tip = "签到成功"
                elif r1.search(response.text):
                    tip = "重复签到"
                else:
                    tip = "cookie 已过期或网站类型不对!"
                    print(f"{url} {tip}")
                log(f"{url} {tip}")
        elif url == "https://pt.btschool.club":
            attendance_url = f"{url}/index.php?action=addbonus"
            with session.get(attendance_url) as response:
                r = re.compile(r"今天签到您获得\d+点魔力值")
                r1 = re.compile(r"退出")
                location = r.search(response.text)
                if location:
                    tip = location.group()
                elif r1.search(response.text):
                    tip = "重复签到"
                else:
                    tip = "cookie已过期"
                    print(f"{url} {tip}")
                log(f"{url} {tip}")
        elif url == "https://lemonhd.org":
            attendance_url = f"{url}/attendance.php"
            with session.get(attendance_url) as response:
                r = re.compile(r"已签到")
                r1 = re.compile(r"请勿重复刷新")
                # log(response.text)
                if r.search(response.text):
                    tip = "签到成功"
                elif r1.search(response.text):
                    tip = "重复签到"
                else:
                    tip = self.url
                    print(f"{url} {tip}")
                log(f"{url} {tip}")
        elif url in ["https://hdtime.org", "https://www.pttime.org"]:
            attendance_url = f"{url}/attendance.php"
            with session.get(attendance_url) as response:
                r = re.compile(r"签到成功")
                r1 = re.compile(r"请勿重复刷新")
                if r.search(response.text):
                    tip = "签到成功"
                elif r1.search(response.text):
                    tip = "重复签到"
                else:
                    tip = "cookie已过期"
                    print(f"{url} {tip}")
                log(f"{url} {tip}")
        else:
            attendance_url = f"{url}/attendance.php"
            with session.get(attendance_url) as response:
                r = re.compile(r"请勿重复刷新")
                r1 = re.compile(r"签到已得\s*\d+")
                location = r1.search(response.text).span()
                if r.search(response.text):
                    tip = "重复签到"
                elif location:
                    tip = response.text[location[0], location[1]]
                else:
                    tip = self.url
                    print(f"{url} {tip}")
                log(f"{url} {tip}")

    @staticmethod
    def signin_discuz_dsu(session, url):
        attendance_url = (
            f"{url}/plugin.php?"
            f"id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
        )
        hash_url = f"{url}/plugin.php?id=dsu_paulsign:sign"
        with session.get(hash_url) as hashurl:
            h = re.compile(r'name="formhash" value="(.*?)"')
            formhash = h.search(hashurl.text)[1]
        data = {
            "qdmode": 3,
            "qdxq": "kx",
            "fastreply": 0,
            "formhash": formhash,
            "todaysay": "",
        }
        with session.post(attendance_url, data) as response:
            r = re.compile(r"签到成功")
            r1 = re.compile(r"已经签到")
            if r.search(response.text):
                log(f"{url} 签到成功")
            elif r1.search(response.text):
                log(f"{url} 重复签到")
            else:
                log(f"{url} {response.text}")
                print(f"{url} {response.text}")

    @staticmethod
    def signin_hifi(session, url):
        attendance_url = f"{url}/sg_sign.htm"
        with session.post(attendance_url) as response:
            r = re.compile(r"成功")
            r1 = re.compile(r"今天已经")
            if r.search(response.text):
                log(f"{url} 签到成功")
            elif r1.search(response.text):
                log(f"{url} 重复签到")
            else:
                log(f"{url} {response.text}")
                print(f"{url} {response.text}")

    def main(self):
        for check_item in self.check_items:
            s = requests.session()
            url = check_item.get("url")
            site_type = check_item.get("type")
            cookie = self.cookie_parse(check_item.get("cookie"))
            header = self.generate_headers(url)
            s.headers.update(header)
            s.cookies.update(cookie)
            if site_type == "pt":
                self.signin(s, url)
            elif site_type == "discuz":
                self.signin_discuz_dsu(s, url)
            elif site_type == "hifi":
                self.signin_hifi(s, url)
            else:
                log("请在配置文件中配置网站类型，如 type: 'pt'")
                print("请在配置文件中配置网站类型，如 type: 'pt'")
        return desp


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("SITE", [])
    result = Site(check_items=_check_items).main()
    send("Site", result)
