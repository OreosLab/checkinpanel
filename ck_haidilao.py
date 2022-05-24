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
        url = "https://superapp-public.kiwa-tech.com/"
        headers = {
            "Host": "superapp-public.kiwa-tech.com",
            "Content-Length": "115",
            "appId": "15",
            "content-type": "application/json",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile MicroMessenger NetType/4G Language/en miniProgram",
            "Referer": "https://servicewechat.com/wx1ddeb67115f30d1a/14/page-frame.html",
        }
        login_data = {
            "openId": openid,
            "country": "CN",
            "uid": uid,
            "type": 1,
            "codeType": 1,
        }
        login = requests.post(
            url + "login/thirdCommLogin", headers=headers, data=json.dumps(login_data)
        ).text
        try:
            login = json.loads(login)
            if login["success"] != True:
                return "登陆失败"
        except json.decoder.JSONDecodeError:
            return "请求失败"
        headers["_HAIDILAO_APP_TOKEN"] = login["data"]["token"]
        headers["ReqType"] = "APPH5"
        headers["Referer"] = (
            url
            + "app-sign-in/?SignInToken="
            + login["data"]["token"]
            + "&source=MiniApp"
        )
        signin = requests.post(
            url + "activity/wxapp/signin/signin",
            headers=headers,
            data=json.dumps({"signinSource": "MiniApp"}),
        ).text
        try:
            signin = json.loads(signin)
            if signin["success"] != True:
                return "今日签到过了"
        except json.decoder.JSONDecodeError:
            return "请求失败"
        fragment = requests.post(
            url + "activity/wxapp/signin/queryFragment", headers=headers
        ).text
        try:
            fragment = json.loads(fragment)
            if signin["success"] == True:
                return (
                    "账号："
                    + login["data"]["name"]
                    + "\n签到成功，碎片余额："
                    + fragment["data"]["total"]
                )
        except json.decoder.JSONDecodeError:
            return "请求失败"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            msg = self.checkin(
                openid=str(check_item.get("openid")), uid=str(check_item.get("uid"))
            )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("HAIDILAO", [])
    res = Haidilao(check_items=_check_items).main()
    send("海底捞会员签到", res)
