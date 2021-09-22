# -*- coding: utf-8 -*-
"""
cron: 45 5 * * *
new Env('哔咔漫画');
"""

import hashlib
import hmac
import json
import random
import string
import time

import requests

from notify_mtr import send
from utils import get_data


class Picacomic:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def generate_headers(path: str, data: dict = None, token: str = None):
        api_key = "C69BAF41DA5ABD1FFEDC6D2FEA56B"
        api_secret = "~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn"
        headers = {
            "api-key": api_key,
            "accept": "application/vnd.picacomic.com.v1+json",
            "app-channel": "2",
            "app-version": "2.2.1.2.3.3",
            "app-uuid": "defaultUuid",
            "app-platform": "android",
            "app-build-version": "44",
            "User-Agent": "okhttp/3.8.1",
            "image-quality": "original"
        }
        current_time = str(int(time.time()))
        nonce = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=32)
        )
        raw = path + current_time + nonce + "POST" + api_key
        raw = raw.lower()
        h = hmac.new(api_secret.encode(), digestmod=hashlib.sha256)
        h.update(raw.encode())
        signature = h.hexdigest()
        headers["time"] = current_time
        headers["nonce"] = nonce
        headers["signature"] = signature
        if data is not None:
            headers["Content-Type"] = "application/json; charset=UTF-8"
        if token is not None:
            headers["authorization"] = token
        return headers

    def sign(self, email, password):
        try:
            data = {"email": email, "password": password}
            sign_headers = self.generate_headers(path="auth/sign-in", data=data)
            sign_response = requests.post(
                url="https://picaapi.picacomic.com/auth/sign-in",
                data=json.dumps(
                    {
                        "email": "sitoi",
                        "password": "123456st"
                    }
                ),
                headers=sign_headers,
                timeout=60,
            ).json()
            token = sign_response.get("data", {}).get("token")
            punch_headers = self.generate_headers(
                path="users/punch-in", token=token)
            response = requests.post(
                url="https://picaapi.picacomic.com/users/punch-in",
                headers=punch_headers,
                timeout=60).json()
            if response.get("data", {}).get("res", {}).get("status", {}) == "ok":
                msg = "打卡成功"
            else:
                msg = "重复签到"
        except Exception as e:
            msg = str(e)
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            email = check_item.get("email")
            password = check_item.get("password")
            sign_msg = self.sign(email=email, password=password)
            msg = f"帐号信息: {email}\n签到状态: {sign_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("PICACOMIC", [])
    res = Picacomic(
        check_items=_check_items).main()
    print(res)
    send("哔咔漫画", res)
