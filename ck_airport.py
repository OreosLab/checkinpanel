# -*- coding: utf-8 -*-
"""
:author @Icrons
cron: 20 10 * * *
new Env('机场签到');
"""

import re

import requests
import urllib3

from notify_mtr import send
from utils import get_data

urllib3.disable_warnings()


class SspanelQd(object):
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def checkin(url, email, password):
        email = email.split("@")
        email = email[0] + "%40" + email[1]
        session = requests.session()
        try:
            # 以下 except 都是用来捕获当 requests 请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            session.get(url, verify=False)
        except requests.exceptions.ConnectionError:
            msg = url + "\n" + "网络不通"
            return msg
        except requests.exceptions.ChunkedEncodingError:
            msg = url + "\n" + "分块编码错误"
            return msg
        except Exception:
            msg = url + "\n" + "未知错误"
            return msg

        login_url = url + "/auth/login"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        post_data = "email=" + email + "&passwd=" + password + "&code="
        post_data = post_data.encode()
        session.post(login_url, post_data, headers=headers, verify=False)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Referer": url + "/user"
        }

        response = session.post(
            url + "/user/checkin", headers=headers, verify=False)
        # print(response.text)
        msg = url + "\n" + (response.json()).get("msg")

        info_url = url + "/user"
        response = session.get(info_url, verify=False)
        """
        以下只适配了editXY主题
        """
        try:
            level = re.findall(r'\["Class", "(.*?)"],', response.text)[0]
            day = re.findall(r'\["Class_Expire", "(.*)"],', response.text)[0]
            rest = re.findall(r'\["Unused_Traffic", "(.*?)"]', response.text)[0]
            msg = (
                url
                + "\n- 今日签到信息：" + str(msg)
                + "\n- 用户等级：" + str(level)
                + "\n- 到期时间：" + str(day)
                + "\n- 剩余流量：" + str(rest)
            )
            return msg
        except Exception:
            return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            # 机场地址
            url = str(check_item.get("url"))
            # 登录信息
            email = str(check_item.get("email"))
            password = str(check_item.get("password"))
            if url and email and password:
                msg = self.checkin(url=url, email=email, password=password)
            else:
                msg = "配置错误"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("AIRPORT", [])
    res = SspanelQd(check_items=_check_items).main()
    print(res)
    send("机场签到", res)
