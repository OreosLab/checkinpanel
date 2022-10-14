# -*- coding: utf-8 -*-
"""
cron: 10 19 * * *
new Env('V2EX');
"""

import re

import requests
import urllib3

from notify_mtr import send
from utils import get_data

urllib3.disable_warnings()


class V2ex:
    def __init__(self, check_items):
        self.check_items = check_items
        self.url = "https://www.v2ex.com/mission/daily"

    def sign(self, session):
        msg = ""

        response = session.get(self.url, verify=False)
        pattern = (
            r"<input type=\"button\" class=\"super normal button\""
            r" value=\".*?\" onclick=\"location\.href = \'(.*?)\';\" />"
        )
        urls = re.findall(pattern, response.text)
        url = urls[0] if urls else None
        if url is None:
            return "cookie 可能过期"
        if url != "/balance":
            data = {"once": url.split("=")[-1]}
            session.get(
                f'https://www.v2ex.com{url.split("?")[0]}', verify=False, params=data
            )

        response = session.get("https://www.v2ex.com/balance", verify=False)
        totals = re.findall(
            r"<td class=\"d\" style=\"text-align: right;\">(\d+\.\d+)</td>",
            response.text,
        )
        total = totals[0] if totals else "签到失败"
        today = re.findall(
            r'<td class="d"><span class="gray">(.*?)</span></td>', response.text
        )
        today = today[0] if today else "签到失败"

        usernames = re.findall(
            r"<a href=\"/member/.*?\" class=\"top\">(.*?)</a>", response.text
        )
        username = usernames[0] if usernames else "用户名获取失败"

        msg += f"帐号信息: {username}\n今日签到: {today}\n帐号余额: {total}"

        response = session.get(url=self.url, verify=False)
        datas = re.findall(r"<div class=\"cell\">(.*?)天</div>", response.text)
        data = f"{datas[0]} 天" if datas else "获取连续签到天数失败"
        msg += f"\n签到天数: {data}"

        msg = msg.strip()
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }

            session = requests.session()
            if check_item.get("proxy", ""):
                proxies = {
                    "http": check_item.get("proxy", ""),
                    "https": check_item.get("proxy", ""),
                }
                session.proxies.update(proxies)
            session.cookies.update(cookie)
            session.headers.update(
                {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
                    "referer": self.url,
                    "accept": "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/webp,image/apng,*/*;"
                    "q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                }
            )

            msg = self.sign(session)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("V2EX", [])
    result = V2ex(check_items=_check_items).main()
    send("V2EX", result)
