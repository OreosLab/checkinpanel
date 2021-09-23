# -*- coding: utf-8 -*-
"""
:author @cokemine
:modifier @o0oo0ooo0 & @Oreo
cron: 0 10 */7 * *
new Env('EUserv');
"""

import os
import json
import re
import time

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data


desp = ""
# 防止 config.sh export TG_API_HOST="" 的情况
TG_API_HOST = os.environ.get("TG_API_HOST", "api.telegram.org")
if TG_API_HOST == "":
    TG_API_HOST = "api.telegram.org"
_print = print


def print(info):
    _print(info)
    global desp
    desp = desp + info + "\n\n"


class EUserv:
    def __init__(self, check_items):
        self.check_items = check_items

    def login(self, username: str, password: str) -> tuple:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36",
            "origin": "https://www.euserv.com",
        }
        url = "https://support.euserv.com/index.iphp"
        session = requests.Session()

        sess = session.get(url, headers=headers)
        sess_id = re.findall("PHPSESSID=(\\w{10,100});", str(sess.headers))[0]
        # 访问png
        png_url = "https://support.euserv.com/pic/logo_small.png"
        session.get(png_url, headers=headers)

        login_data = {
            "email": username,
            "password": password,
            "form_selected_language": "en",
            "Submit": "Login",
            "subaction": "login",
            "sess_id": sess_id
        }
        f = session.post(url, headers=headers, data=login_data)
        f.raise_for_status()

        if f.text.find("Hello") == -1 and f.text.find("Confirm or change your customer data here") == -1:
            return "-1", session
        return sess_id, session

    def get_servers(self, sess_id: str, session: requests.session) -> tuple:
        d = {}
        url = "https://support.euserv.com/index.iphp?sess_id=" + sess_id
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36",
            "origin": "https://www.euserv.com"
        }
        f = session.get(url=url, headers=headers)
        f.raise_for_status()
        soup = BeautifulSoup(f.text, "html.parser")
        for tr in soup.select("#kc2_order_customer_orders_tab_content_1 .kc2_order_table.kc2_content_table tr"):
            server_id = tr.select(".td-z1-sp1-kc")
            if not len(server_id) == 1:
                continue
            flag = True if tr.select(".td-z1-sp2-kc .kc2_order_action_container")[
                0].get_text().find("Contract extension possible from") == -1 else False
            d[server_id[0].get_text()] = flag
        return d

    def renew(self, sess_id: str, session: requests.session, password: str, order_id: str) -> bool:
        url = "https://support.euserv.com/index.iphp"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36",
            "Host": "support.euserv.com",
            "origin": "https://support.euserv.com",
            "Referer": "https://support.euserv.com/index.iphp"
        }
        data = {
            "Submit": "Extend contract",
            "sess_id": sess_id,
            "ord_no": order_id,
            "subaction": "choose_order",
            "choose_order_subaction": "show_contract_details"
        }
        session.post(url, headers=headers, data=data)
        data = {
            "sess_id": sess_id,
            "subaction": "kc2_security_password_get_token",
            "prefix": "kc2_customer_contract_details_extend_contract_",
            "password": password
        }
        f = session.post(url, headers=headers, data=data)
        f.raise_for_status()
        if not json.loads(f.text)["rs"] == "success":
            return False
        token = json.loads(f.text)["token"]["value"]
        data = {
            "sess_id": sess_id,
            "ord_id": order_id,
            "subaction": "kc2_customer_contract_details_extend_contract_term",
            "token": token
        }
        session.post(url, headers=headers, data=data)
        time.sleep(5)
        return True

    def check(self, sess_id: str, session: requests.session):
        print("Checking.......")
        d = self.get_servers(sess_id, session)
        flag = True
        for key, val in d.items():
            if val:
                flag = False
                print("ServerID: %s Renew Failed!" % key)
        if flag:
            print("ALL Work Done! Enjoy")

    def main(self):
        i = 1
        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")
            print("*" * 30)
            print("正在续费第 %d 个账号" % i)
            sessid, s = self.login(username, password)
            if sessid == "-1":
                print("第 %d 个账号登陆失败，请检查登录信息" % i)
                continue
            servers = self.get_servers(sessid, s)
            print("检测到第 {} 个账号有 {} 台 VPS，正在尝试续期".format(i, len(servers)))
            for k, v in servers.items():
                if v:
                    if not self.renew(sessid, s, password, k):
                        print("ServerID: %s Renew Error!" % k)
                    else:
                        print("ServerID: %s has been successfully renewed!" % k)
                else:
                    print("ServerID: %s does not need to be renewed" % k)
            time.sleep(15)
            self.check(sessid, s)
            time.sleep(5)
            i += 1
        print("*" * 30)
        return desp


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("EUSERV", [])
    res = EUserv(check_items=_check_items).main()
    send("EUserv", res)
