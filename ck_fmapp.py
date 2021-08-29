# -*- coding: utf-8 -*-
"""
建议cron: 30 14 * * *
new Env('米家');
"""
import json
import requests
from getENV import getENv
from checksendNotify import send


class FMAPPCheckIn:
    def __init__(self, check_item):
        self.check_item = check_item

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
        fmapp_token = self.check_item.get("fmapp_token")
        fmapp_cookie = self.check_item.get("fmapp_cookie")
        fmapp_blackbox = self.check_item.get("fmapp_blackbox")
        fmapp_device_id = self.check_item.get("fmapp_device_id")
        fmapp_fmversion = self.check_item.get("fmapp_fmversion", "2.2.3")
        fmapp_os = self.check_item.get("fmapp_os", "ios")
        fmapp_useragent = self.check_item.get("fmapp_useragent", "Fa")
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
        return msg


if __name__ == "__main__":
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    else:
        print('加载配置文件失败，请检查！')
        exit(1)
    _check_item = datas.get("FMAPP_ACCOUNT_LIST", [])[0]
    res = FMAPPCheckIn(check_item=_check_item).main()
    print(res)
    send("米家APP", res)