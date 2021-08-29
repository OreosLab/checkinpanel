# -*- coding: utf-8 -*-
"""
cron: 30 14 * * *
new Env('米家');
"""

import json, requests
from getENV import getENv
from checksendNotify import send


class FMAPPCheckIn:
    def __init__(self, fmapp_account_list):
        self.fmapp_account_list = fmapp_account_list

    @staticmethod
    def sign(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/market/member/signin/sign"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = (
                    f"在坚持{data.get('nextDay')}天即可获得{data.get('nextNumber')}个发米粒\n"
                    f"签到{data.get('lastDay')}天可获得{data.get('lastNumber')}个发米粒"
                )
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def user_info(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/info"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("nickName")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def mili_count(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/v1/mili/service/detail"
            response = requests.post(url=url, headers=headers, data=json.dumps({"pageSize": 10, "pageNo": 1})).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("miliNum")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    def main(self):
        for fmapp_account in fmapp_account_list:
            fmapp_token = self.fmapp_account.get("fmapp_token")
            fmapp_cookie = self.fmapp_account.get("fmapp_cookie")
            fmapp_blackbox = self.fmapp_account.get("fmapp_blackbox")
            fmapp_device_id = self.fmapp_account.get("fmapp_device_id")
            fmapp_fmversion = self.fmapp_account.get("fmapp_fmversion", "2.2.3")
            fmapp_os = self.fmapp_account.get("fmapp_os", "ios")
            fmapp_useragent = self.fmapp_account.get("fmapp_useragent", "Fa")
            headers = {
                "Accept": "*/*",
                "Accept-Language": "zh-Hans;q=1.0",
                "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
                "Host": "fmapp.chinafamilymart.com.cn",
                "Content-Type": "application/json",
                "loginChannel": "app",
                "token": fmapp_token,
                "fmVersion": fmapp_fmversion,
                "deviceId": fmapp_device_id,
                "User-Agent": fmapp_useragent,
                "os": fmapp_os,
                "cookie": fmapp_cookie,
                "blackBox": fmapp_blackbox,
            }
            sign_msg = self.sign(headers=headers)
            name_msg = self.user_info(headers=headers)
            mili_msg = self.mili_count(headers=headers)
            msg = f"帐号信息: {name_msg}\n签到状态: {sign_msg}\n米粒数量: {mili_msg}"
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == "__main__":
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    _fmapp_account_list = datas.get("FMAPP_ACCOUNT_LIST", [])
    res = FMAPPCheckIn(fmapp_account_list=_fmapp_account_list).main()
    print(res)
    send("米家APP", res)