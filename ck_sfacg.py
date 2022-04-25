# -*- coding: utf-8 -*-
"""
cron: 15 10 * * *
new Env('SF 轻小说');
"""

import json
import time
from datetime import datetime, timedelta, timezone

import requests

from notify_mtr import send
from utils import get_data

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
timestamp = bj_dt.timestamp()
readingDate = datetime.fromtimestamp(timestamp).strftime("%Y 年 %m 月 %d 日")


class SFACG:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def generate_headers(authorization, cookie, useragent, sfsecurity):
        headers = {
            "Host": "api.sfacg.com",
            "accept-charset": "UTF-8",
            "accept": "application/vnd.sfacg.api+json;version=1",
            "authorization": authorization,
            "cookie": cookie,
            "user-agent": useragent,
            "sfsecurity": sfsecurity.split("&")[0]
            + "&timestamp="
            + str(int(timestamp))
            + "&"
            + sfsecurity.split("&")[2]
            + "&"
            + sfsecurity.split("&")[3],
            "accept-encoding": "gzip",
        }
        return headers

    @staticmethod
    def post_re(api, headers, data):
        return requests.post(api, headers=headers, data=data).json()

    @staticmethod
    def get_re(api, headers):
        return requests.get(url=api, headers=headers).json()

    @staticmethod
    def put_re(api, put_headers, data):
        return requests.put(api, headers=put_headers, data=data).json()

    def check_cookie(self, authorization, cookie, useragent, sfsecurity):
        headers = self.generate_headers(authorization, cookie, useragent, sfsecurity)
        res = requests.get("https://api.sfacg.com/user?", headers=headers).json()
        money = requests.get("https://api.sfacg.com/user/money", headers=headers).json()
        try:
            nickname = res["data"]["nickName"]
            fire_money_remain = money["data"]["fireMoneyRemain"]
            vip_level = money["data"]["vipLevel"]
            info = (
                "账号名称: "
                + nickname
                + "\n火卷余额: "
                + str(fire_money_remain)
                + "\nVIP: "
                + str(vip_level)
            )
            print("Cookie 凭证有效！")
        except Exception:
            info = "Cookie 凭证失效 httpCode: " + str(res["status"]["httpCode"])
            print(info)
        return info

    def task(self, authorization, cookie, useragent, sfsecurity):
        headers = self.generate_headers(authorization, cookie, useragent, sfsecurity)
        print("运行时间:", readingDate)
        read_time = {"seconds": 3605, "readingDate": readingDate, "entityType": 2}
        listen_time = {"seconds": 3605, "readingDate": readingDate, "entityType": 3}
        read_data = json.dumps(read_time)
        listen_data = json.dumps(listen_time)

        put_headers = headers
        put_headers["accept-encoding"] = "gzip"
        put_headers["content-length"] = "57"
        put_headers["content-type"] = "application/json; charset=UTF-8"

        print("开始执行任务")
        self.put_re(
            "https://api.sfacg.com/user/readingtime", put_headers, data=listen_data
        )
        self.post_re("https://api.sfacg.com/user/tasks/4", headers, data=listen_data)
        self.post_re("https://api.sfacg.com/user/tasks/5", headers, data=listen_data)
        self.post_re("https://api.sfacg.com/user/tasks/17", headers, data=listen_data)
        for _ in range(3):
            self.put_re(
                "https://api.sfacg.com/user/readingtime", put_headers, read_data
            )
            time.sleep(0.5)
            self.put_re(
                "https://api.sfacg.com/user/tasks/5", put_headers, data=listen_data
            )
            self.put_re(
                "https://api.sfacg.com/user/tasks/4", put_headers, data=listen_data
            )
            self.put_re(
                "https://api.sfacg.com/user/tasks/17", put_headers, data=listen_data
            )

    def checkin(self, authorization, cookie, useragent, sfsecurity):
        headers = self.generate_headers(authorization, cookie, useragent, sfsecurity)
        print("运行时间:", readingDate)
        sign_date = "{} 年 {} 月 {} 日"
        for data in self.get_re("https://api.sfacg.com/user/signInfo", headers)["data"]:
            sign_date = sign_date.format(data["year"], data["month"], data["day"])
        if sign_date == readingDate:
            sign_msg = "已签提醒: 您今天已经签过到了,请明天再来"
            print(sign_msg)
        else:
            print("检测到今天还未签到，开始自动签到和完成任务")
            res = requests.put(
                "https://api.sfacg.com/user/signInfo", headers=headers
            ).json()
            # print(res)
            if res["status"]["httpCode"] == 200:
                sign_tip = "签到提醒: 签到成功！"
            else:
                sign_tip = "签到提醒: " + str(res["status"]["msg"])
            sign_msg = ""
            for data in self.get_re("https://api.sfacg.com/user/signInfo", headers)[
                "data"
            ]:
                sign_msg = (
                    "签到日期: "
                    + sign_date.format(data["year"], data["month"], data["day"])
                    + "，连续签到 "
                    + str(data["continueNum"])
                    + " 天"
                )
            sign_msg += "\n" + sign_tip
            self.task(authorization, cookie, useragent, sfsecurity)
        return sign_msg

    def check_coin(self, authorization, cookie, useragent, sfsecurity):
        headers = self.generate_headers(authorization, cookie, useragent, sfsecurity)
        res = self.get_re("https://api.sfacg.com/user/welfare/income", headers)
        try:
            coin_info = "金币数量: " + str(res["data"]["coinRemain"])
        except Exception:
            coin_info = "Cookie 凭证失效 httpCode: " + str(res["status"]["httpCode"])
        return coin_info

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            authorization = check_item.get("authorization")
            cookie = check_item.get("cookie")
            useragent = check_item.get("useragent")
            sfsecurity = check_item.get("sfsecurity")
            info = self.check_cookie(authorization, cookie, useragent, sfsecurity)
            sign_msg = self.checkin(authorization, cookie, useragent, sfsecurity)
            coin_info = self.check_coin(authorization, cookie, useragent, sfsecurity)
            msg = info + "\n" + sign_msg + "\n" + coin_info
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("SFACG", [])
    res = SFACG(check_items=_check_items).main()
    send("SFACG", res)
