# -*- coding: utf-8 -*-
"""
cron: 0 10 */7 * *
new Env('EUserv');
"""

import base64
import json
import re
import time

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data

#
# SPDX-FileCopyrightText: (c) 2020-2021 CokeMine & Its repository contributors
# SPDX-FileCopyrightText: (c) 2021 A beam of light
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
euserv auto-renew script
       v2021.09.30
* Captcha automatic recognition using TrueCaptcha API
* Email notification
* Add login failure retry mechanism
* reformat log info
"""


# default value is TrueCaptcha demo credential,
# you can use your own credential via set environment variables:
# userid and apikey
# demo: https://apitruecaptcha.org/demo
# demo2: https://apitruecaptcha.org/demo2
# demo apikey also has a limit of 100 times per day
# {
# 'error': '101.0 above free usage limit 100 per day and no balance',
# 'requestId': '7690c065-70e0-4757-839b-5fd8381e65c7'
# }


desp = ""  # 空值


def log(info: str):
    global desp
    desp = desp + info + "\n\n"


class EUserv:
    def __init__(self, check_items):
        self.check_items = check_items
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/94.0.4606.61 Safari/537.36 "
        )

    def captcha_solver(
        self, captcha_image_url: str, session: requests.session, userid, apikey
    ) -> dict:
        """
        TrueCaptcha API doc: https://apitruecaptcha.org/api
        Free to use 100 requests per day.
        """
        response = session.get(captcha_image_url)
        encoded_string = base64.b64encode(response.content)
        url = "https://api.apitruecaptcha.org/one/gettext"

        data = {
            "userid": userid,
            "apikey": apikey,
            "case": "mixed",
            "mode": "human",
            "data": str(encoded_string)[2:-1],
        }
        r = requests.post(url=url, json=data)
        j = json.loads(r.text)
        return j

    def handle_captcha_solved_result(self, solved: dict) -> str:
        """Since CAPTCHA sometimes appears as a very simple binary arithmetic expression.
        But since recognition sometimes doesn't show the result of the calculation directly,
        that's what this function is for.
        """
        if "result" in solved:
            solved_text = solved["result"]
            if "RESULT  IS" in solved_text:
                log("[Captcha Solver] You are using the demo apikey.")
                print("There is no guarantee that demo apikey will work in the future!")
                # because using demo apikey
                text = re.findall(r"RESULT  IS . (.*) .", solved_text)[0]
            else:
                # using your own apikey
                log("[Captcha Solver] You are using your own apikey.")
                text = solved_text
            operators = ["X", "x", "+", "-"]
            if any(x in text for x in operators):
                for operator in operators:
                    operator_pos = text.find(operator)
                    if operator == "x" or operator == "X":
                        operator = "*"
                    if operator_pos != -1:
                        left_part = text[:operator_pos]
                        right_part = text[operator_pos + 1 :]
                        if left_part.isdigit() and right_part.isdigit():
                            return eval(
                                "{left} {operator} {right}".format(
                                    left=left_part, operator=operator, right=right_part
                                )
                            )
                        else:
                            # Because these symbols("X", "x", "+", "-") do not appear at the same time,
                            # it just contains an arithmetic symbol.
                            return text
            else:
                return text
        else:
            print(solved)
            raise KeyError("Failed to find parsed results.")

    def get_captcha_solver_usage(self, userid, apikey) -> dict:
        url = "https://api.apitruecaptcha.org/one/getusage"

        params = {
            "username": userid,
            "apikey": apikey,
        }
        r = requests.get(url=url, params=params)
        j = json.loads(r.text)
        return j

    def login(
        self,
        username: str,
        password: str,
        userid: str,
        apikey: str,
        check_captcha_solver_usage: bool,
    ) -> tuple:
        headers = {"user-agent": self.user_agent, "origin": "https://www.euserv.com"}
        url = "https://support.euserv.com/index.iphp"
        captcha_image_url = "https://support.euserv.com/securimage_show.php"
        session = requests.Session()

        sess = session.get(url, headers=headers)
        sess_id = re.findall("PHPSESSID=(\\w{10,100});", str(sess.headers))[0]
        # visit png
        logo_png_url = "https://support.euserv.com/pic/logo_small.png"
        session.get(logo_png_url, headers=headers)

        login_data = {
            "email": username,
            "password": password,
            "form_selected_language": "en",
            "Submit": "Login",
            "subaction": "login",
            "sess_id": sess_id,
        }
        f = session.post(url, headers=headers, data=login_data)
        f.raise_for_status()

        if (
            f.text.find("Hello") == -1
            and f.text.find("Confirm or change your customer data here") == -1
        ):
            if (
                f.text.find(
                    "To finish the login process please solve the following captcha."
                )
                == -1
            ):
                return "-1", session
            else:
                log("[Captcha Solver] 进行验证码识别...")
                solved_result = self.captcha_solver(
                    captcha_image_url, session, userid, apikey
                )
                captcha_code = self.handle_captcha_solved_result(solved_result)
                log("[Captcha Solver] 识别的验证码是: {}".format(captcha_code))

                if check_captcha_solver_usage:
                    usage = self.get_captcha_solver_usage(userid, apikey)
                    log(
                        "[Captcha Solver] current date {0} api usage count: {1}".format(
                            usage[0]["date"], usage[0]["count"]
                        )
                    )

                f2 = session.post(
                    url,
                    headers=headers,
                    data={
                        "subaction": "login",
                        "sess_id": sess_id,
                        "captcha_code": captcha_code,
                    },
                )
                if (
                    f2.text.find(
                        "To finish the login process please solve the following captcha."
                    )
                    == -1
                ):
                    log("[Captcha Solver] 验证通过")
                    return sess_id, session
                else:
                    log("[Captcha Solver] 验证失败")
                    return "-1", session

        else:
            return sess_id, session

    def get_servers(self, sess_id: str, session: requests.session) -> dict:
        d = {}
        url = "https://support.euserv.com/index.iphp?sess_id=" + sess_id
        headers = {"user-agent": self.user_agent, "origin": "https://www.euserv.com"}
        f = session.get(url=url, headers=headers)
        f.raise_for_status()
        soup = BeautifulSoup(f.text, "html.parser")
        for tr in soup.select(
            "#kc2_order_customer_orders_tab_content_1 .kc2_order_table.kc2_content_table tr"
        ):
            server_id = tr.select(".td-z1-sp1-kc")
            if not len(server_id) == 1:
                continue
            flag = (
                True
                if tr.select(".td-z1-sp2-kc .kc2_order_action_container")[0]
                .get_text()
                .find("Contract extension possible from")
                == -1
                else False
            )
            d[server_id[0].get_text()] = flag
        return d

    def renew(
        self, sess_id: str, session: requests.session, password: str, order_id: str
    ) -> bool:
        url = "https://support.euserv.com/index.iphp"
        headers = {
            "user-agent": self.user_agent,
            "Host": "support.euserv.com",
            "origin": "https://support.euserv.com",
            "Referer": "https://support.euserv.com/index.iphp",
        }
        data = {
            "Submit": "Extend contract",
            "sess_id": sess_id,
            "ord_no": order_id,
            "subaction": "choose_order",
            "choose_order_subaction": "show_contract_details",
        }
        session.post(url, headers=headers, data=data)
        data = {
            "sess_id": sess_id,
            "subaction": "kc2_security_password_get_token",
            "prefix": "kc2_customer_contract_details_extend_contract_",
            "password": password,
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
            "token": token,
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
                log("[EUserv] ServerID: %s Renew Failed!" % key)

        if flag:
            log("[EUserv] ALL Work Done! Enjoy~")

    def main(self):
        i = 0
        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")
            check_captcha_solver_usage = check_item.get("captcha")
            userid = check_item.get("userid")
            apikey = check_item.get("apikey")
            log("*" * 12)
            log("[EUserv] 正在续费第 %d 个账号" % (i + 1))
            sessid, s = self.login(
                username, password, userid, apikey, check_captcha_solver_usage
            )
            if sessid == "-1":
                log("[EUserv] 第 %d 个账号登陆失败，请检查登录信息" % (i + 1))
                continue
            SERVERS = self.get_servers(sessid, s)
            log("[EUserv] 检测到第 {} 个账号有 {} 台 VPS，正在尝试续期".format(i + 1, len(SERVERS)))
            for k, v in SERVERS.items():
                if v:
                    if not self.renew(sessid, s, password, k):
                        log("[EUserv] ServerID: %s Renew Error!" % k)
                    else:
                        log("[EUserv] ServerID: %s has been successfully renewed!" % k)
                else:
                    log("[EUserv] ServerID: %s does not need to be renewed" % k)
            time.sleep(15)
            self.check(sessid, s)
            time.sleep(5)
            log("*" * 12)
            i += 1
        return desp


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("EUSERV", [])
    res = EUserv(check_items=_check_items).main()
    send("EUserv", res)
