# -*- coding: utf-8 -*-
"""
cron: 27 8,22 * * *
new Env('Hax 续期提醒');
"""

import datetime
import re

import requests

from notify_mtr import send
from utils import get_data


class HaxClock:
    def __init__(self, check_items):
        self.check_items = check_items

    def check_vps_info(self, cookie):
        url = "https://hax.co.id/vps-info"
        headers = {
            "cookie": cookie,
            "referer": "https://hax.co.id/vps-info/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43",
        }
        datas = requests.get(url=url, headers=headers).text
        return datas

    def get_valid_until(self, cookie):
        html_text = self.check_vps_info(cookie)
        hostname = re.search("[0-9]+_hax", html_text).group(0)
        valid_until = re.search(
            "(?:(((Jan(uary)?|Ma(r(ch)?|y)|Jul(y)?|Aug(ust)?|Oct(ober)?|Dec(ember)?)\\ 31)|((Jan(uary)?|Ma(r(ch)?|y)|Apr(il)?|Ju((ly?)|(ne?))|Aug(ust)?|Oct(ober)?|(Sept|Nov|Dec)(ember)?)\\ (0?[1-9]|([12]\\d)|30))|(Feb(ruary)?\\ (0?[1-9]|1\\d|2[0-8]|(29(?=,\\ ((1[6-9]|[2-9]\\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))))\\,\\ ((1[6-9]|[2-9]\\d)\\d{2}))",
            html_text,
        ).group(0)
        return hostname, valid_until

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            hostname, valid_until = self.get_valid_until(cookie)
            d1 = datetime.datetime.today()
            today = d1.strftime("%B %d, %Y")
            d2 = datetime.datetime.strptime(valid_until, "%B %d, %Y")
            tip = (
                "Please wait until at least three days before the expiry date to renew. / 请等到至少过期前三天再去续期。"
                if (d2 - d1).days > 3
                else "AVAILABLE for RENEWAL / 可以续期了"
            )
            msg = f"Hostname / 主机名：{hostname}\nToday / 本地日期：{today}\nValid until / 有效期至：{valid_until}\n{tip}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("HAXCLOCK", [])
    res = HaxClock(check_items=_check_items).main()
    send("Hax 续期提醒", res)
