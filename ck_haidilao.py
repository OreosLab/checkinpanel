# -*- coding: utf-8 -*-
"""
cron: 20 8 * * *
new Env('海底捞会员签到');
"""

import json

import requests

from notify_mtr import send
from utils import get_data


class Haidilao:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def checkin(openid, uid):
        headers = {
            "Host": "superapp-public.kiwa-tech.com",
            "Content-Length": "115",
            "appId": "15",
            "content-type": "application/json",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Mobile MicroMessenger NetType/4G Language/en miniProgram",
            "Referer": "https://servicewechat.com/wx1ddeb67115f30d1a/14/page-frame.html",
        }
        login_data = {
            "openId": openid,
            "country": "CN",
            "uid": uid,
            "type": 1,
            "codeType": 1,
        }
        url = "https://superapp-public.kiwa-tech.com/"

        try:
            login_res = requests.post(
                f"{url}login/thirdCommLogin", headers=headers, json=login_data
            ).json()
            if not login_res["success"]:
                return "登录失败"
            data = login_res["data"]
        except json.decoder.JSONDecodeError:
            return "登录请求失败"

        headers["_HAIDILAO_APP_TOKEN"] = data["token"]
        headers["ReqType"] = "APPH5"
        headers[
            "Referer"
        ] = f'{url}app-sign-in/?SignInToken={data["token"]}&source=MiniApp'

        try:
            signin_res = requests.post(
                f"{url}activity/wxapp/signin/signin",
                headers=headers,
                json={"signinSource": "MiniApp"},
            ).json()
            if "请勿重复操作" in signin_res["msg"]:
                return "今日签到过了"
        except json.decoder.JSONDecodeError:
            return "签到请求失败"

        try:
            fragment_res = requests.post(
                f"{url}activity/wxapp/signin/queryFragment", headers=headers
            ).json()
            if fragment_res["success"]:
                return (
                    f'账号：{data["name"]} 签到成功\n' f'碎片余额：{fragment_res["data"]["total"]}'
                )
        except json.decoder.JSONDecodeError:
            return "查询请求失败"

        return "未知错误"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            msg = self.checkin(
                openid=str(check_item.get("openid")), uid=str(check_item.get("uid"))
            )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("HAIDILAO", [])
    result = Haidilao(check_items=_check_items).main()
    send("海底捞会员签到", result)
