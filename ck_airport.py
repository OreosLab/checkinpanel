# -*- coding: utf-8 -*-
"""
:author @Icrons
cron: 20 10 * * *
new Env('机场签到');
"""

import json
import re
import traceback

import requests
import urllib3

from notify_mtr import send
from utils import get_data

urllib3.disable_warnings()


class SspanelQd:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def checkin(url, email, password):
        url = url.rstrip("/")
        emails = email.split("@")
        email = f"{emails[0]}%40{emails[1]}" if len(emails) > 1 else emails[0]
        session = requests.session()

        # 以下 except 都是用来捕获当 requests 请求出现异常时，
        # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
        try:
            session.get(url, verify=False)
        except requests.exceptions.ConnectionError:
            return f"{url}\n网络不通"
        except requests.exceptions.ChunkedEncodingError:
            return f"{url}\n分块编码错误"
        except Exception:
            print(f"未知错误，错误信息：\n{traceback.format_exc()}")
            return f"{url}\n未知错误，请查看日志"

        login_url = f"{url}/auth/login"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/56.0.2924.87 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        login_data = f"email={email}&passwd={password}&code=".encode()

        try:
            response = session.post(
                login_url, login_data, headers=headers, verify=False
            )
            login_text = response.text.encode("utf-8").decode("unicode_escape")
            print(f"{url} 接口登录返回信息：{login_text}")
            login_json = json.loads(login_text)
            if login_json.get("ret") == 0:
                return f'{url}\n{login_json.get("msg")}'
        except Exception:
            print(f"登录失败，错误信息：\n{traceback.format_exc()}")
            return f"{url}\n登录失败，请查看日志"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/56.0.2924.87 Safari/537.36",
            "Referer": f"{url}/user",
        }

        try:
            response = session.post(
                f"{url}/user/checkin", headers=headers, verify=False
            )
            sign_text = response.text.encode("utf-8").decode("unicode_escape")
            print(f"{url} 接口签到返回信息：{sign_text}")
            sign_json = json.loads(sign_text)
            sign_msg = sign_json.get("msg")
            msg = f"{url}\n{sign_msg}" if sign_msg else f"{url}\n{sign_json}"
        except Exception:
            msg = f"{url}\n签到失败失败，请查看日志"
            print(f"签到失败，错误信息：\n{traceback.format_exc()}")

        # 以下只适配了editXY主题
        try:
            info_url = f"{url}/user"
            response = session.get(info_url, verify=False)
            level = re.findall(r'\["Class", "(.*?)"],', response.text)[0]
            day = re.findall(r'\["Class_Expire", "(.*)"],', response.text)[0]
            rest = re.findall(r'\["Unused_Traffic", "(.*?)"]', response.text)[0]
            return (
                f"{url}\n"
                f"- 今日签到信息：{msg}\n"
                f"- 用户等级：{level}\n"
                f"- 到期时间：{day}\n"
                f"- 剩余流量：{rest}"
            )
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
                msg = self.checkin(url, email, password)
            else:
                msg = "配置错误"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("AIRPORT", [])
    res = SspanelQd(check_items=_check_items).main()
    send("机场签到", res)
