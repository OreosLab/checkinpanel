# -*- coding: utf-8 -*-
"""
cron: 48 7 * * *
new Env('微博');
"""

from urllib.parse import parse_qsl, urlsplit

import requests

from notify_mtr import send
from utils import get_data


class WeiBo:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(token):
        headers = {"User-Agent": "Weibo/52588 (iPhone; iOS 14.5; Scale/3.00)"}
        res = requests.get(
            url=f"https://api.weibo.cn/2/checkin/add?c=iphone&{token}", headers=headers
        ).json()
        if res.get("status") == 10000:
            return (
                f'连续签到: {res.get("data").get("continuous")}天\n'
                f'本次收益: {res.get("data").get("desc")}'
            )

        if res.get("errno") == 30000:
            return "每日签到: 已签到"
        if res.get("status") == 90005:
            return f'每日签到: {res.get("msg")}'
        return "每日签到: 签到失败"

    @staticmethod
    def card(token):
        headers = {"User-Agent": "Weibo/52588 (iPhone; iOS 14.5; Scale/3.00)"}
        res = requests.get(
            url=f"https://api.weibo.cn/2/!/ug/king_act_home?c=iphone&{token}",
            headers=headers,
        ).json()
        if res.get("status") != 10000:
            return "每日打卡: 活动过期或失效"
        nickname = res.get("data").get("user").get("nickname")
        return (
            f"用户昵称: {nickname}\n"
            f'每日打卡: {res.get("data").get("signin").get("title").split("<")[0]}天\n'
            f'积分总计: {res.get("data").get("user").get("energy")}'
        )

    @staticmethod
    def pay(token):
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "pay.sc.weibo.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
            "Weibo (iPhone10,1__weibo__11.2.1__iphone__os14.5)",
        }
        data = f"{token}&lang=zh_CN&wm=3333_2001"
        response = requests.post(
            url="https://pay.sc.weibo.com/aj/mobile/home/welfare/signin/do",
            headers=headers,
            data=data,
        )
        try:
            res = response.json()
            if res.get("status") == 1:
                msg = f'微博钱包: {res.get("score")} 积分'
            elif res.get("status") == 2:
                msg = "微博钱包: 已签到"
                info_res = requests.post(
                    url="https://pay.sc.weibo.com/api/client/sdk/app/balance",
                    headers=headers,
                    data=data,
                ).json()
                msg += f"\n当前现金: {info_res.get('data').get('balance')} 元"
            else:
                msg = "微博钱包: Cookie失效"
            return msg
        except Exception:
            msg = "微博钱包: Cookie失效"
            return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            url = check_item.get("url")
            query_dict = dict(parse_qsl(urlsplit(url).query))
            token = "&".join(
                [
                    f"{key}={value}"
                    for key, value in query_dict.items()
                    if key in ["from", "uid", "s", "gsid"]
                ]
            )
            sign_msg = self.sign(token=token)
            card_msg = self.card(token=token)
            pay_msg = self.pay(token=token)
            msg = f"{sign_msg}\n{card_msg}\n{pay_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("WEIBO", [])
    result = WeiBo(check_items=_check_items).main()
    send("微博", result)
