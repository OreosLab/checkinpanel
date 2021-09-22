# -*- coding: utf-8 -*-
"""
cron: 18 16 * * *
new Env('联通营业厅');
"""

import base64
import random
import re
import time

import requests
import rsa

from notify_mtr import send
from utils import get_data


class UniCom:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def str2key(s):
        b_str = base64.b64decode(s)
        if len(b_str) < 162:
            return False
        hex_str = ""
        for x in b_str:
            h = hex(x)[2:]
            h = h.rjust(2, "0")
            hex_str += h
        m_start = 29 * 2
        e_start = 159 * 2
        m_len = 128 * 2
        e_len = 3 * 2
        modulus = hex_str[m_start: m_start + m_len]
        exponent = hex_str[e_start: e_start + e_len]
        return modulus, exponent

    @staticmethod
    def encryption(message, key):
        modulus = int(key[0], 16)
        exponent = int(key[1], 16)
        rsa_pubkey = rsa.PublicKey(modulus, exponent)
        crypto = rsa.encrypt(message, rsa_pubkey)
        b64str = base64.b64encode(crypto)
        return b64str

    def login(self, mobile, password, app_id):
        session = requests.Session()
        pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB"
        key = self.str2key(pubkey)
        mobile = self.encryption(str.encode(mobile), key)
        password = self.encryption(str.encode(password), key)
        flag = False
        cookies = {
            "c_sfbm": "234g_00",
            "logHostIP": "null",
            "route": "cc3839c658dd60cb7c25f6c2fe6eb964",
            "channel": "GGPD",
            "city": "076|776",
            "devicedId": "B97CDE2A-D435-437D-9FEC-5D821A012972",
            "mobileService1": "ProEsSI6SM4DbWhaeVsPtve9pu7VWz0m94giTHkPBl40Gx8nebgV!-1027473388",
            "mobileServiceAll": "a92d76b26705a45a087027f893c70618",
        }

        headers = {
            "Host": "m.client.10010.com",
            "Accept": "/",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": "ChinaUnicom4.x/3.0 CFNetwork/1197 Darwin/20.0.0",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "deflate, br",
            "Content-Length": "891",
        }

        data = {
            "reqtime": round(time.time() * 1000),
            "simCount": "1",
            "version": "iphone_c@8.0004",
            "mobile": mobile,
            "netWay": "wifi",
            "isRemberPwd": "false",
            "appId": app_id,
            "deviceId": "b61f7efcba733583170df52d8f2f9f87521b3844d01ccbc774bbfa379eaeb3fa",
            "pip": "192.168.1.4",
            "password": password,
            "deviceOS": "14.0.1",
            "deviceBrand": "iphone",
            "deviceModel": "iPad",
            "remark4": "",
            "keyVersion": "",
            "deviceCode": "B97CDE2A-D435-437D-9FEC-5D821A012972",
        }

        response = session.post(
            url="https://m.client.10010.com/mobileService/login.htm", headers=headers, cookies=cookies, data=data
        )
        response.encoding = "utf-8"
        try:
            result = response.json()
            if result["code"] == "0":
                login_msg = {"name": "登录账号", "value": result["default"][:4] + "xxxx" + result["default"][-4:]}
                session.headers.update(
                    {
                        "User-Agent": "Mozilla/5.0 (Linux; Android 10; RMX1901 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36; unicom{version:android@8.0100,desmobile:"
                                      + str(mobile)
                                      + "};devicetype{deviceBrand:Realme,deviceModel:RMX1901};{yw_code:}"
                    }
                )
                flag = True
            else:
                login_msg = {"name": "登录账号", "value": result["dsc"]}
        except Exception as e:
            login_msg = {"name": "登录账号", "value": str(e)}
        if flag:
            return session, login_msg
        else:
            return False, login_msg

    @staticmethod
    def get_encryptmobile(session):
        page = session.post(url="https://m.client.10010.com/dailylottery/static/textdl/userLogin")
        page.encoding = "utf-8"
        match = re.search(r"encryptmobile=\w+", page.text, flags=0)
        user_number = match.group(0)[14:]
        return user_number

    # 每日签到
    @staticmethod
    def daily_daysign(session, mobile):
        try:
            session.headers.update({"referer": "https://img.client.10010.com/activitys/member/index.html"})
            param = f"yw_code=&desmobile={mobile}&version=android@$8.0100"
            session.get(url="https://act.10010.com/SigninApp/signin/querySigninActivity.htm?" + param)
            session.headers.update(
                {"referer": "https://act.10010.com/SigninApp/signin/querySigninActivity.htm?" + param}
            )
            day_sign = session.post(url="https://act.10010.com/SigninApp/signin/daySign")
            day_sign.encoding = "utf-8"
            session.post(url="https://act.10010.com/SigninApp/signin/todaySign")
            session.post(url="https://act.10010.com/SigninApp/signin/addIntegralDA")
            session.post(url="https://act.10010.com/SigninApp/signin/getContinuous")
            session.post(url="https://act.10010.com/SigninApp/signin/getIntegral")
            session.post(url="https://act.10010.com/SigninApp/signin/getGoldTotal")
            session.headers.pop("referer")
            res = day_sign.json()
            if res["status"] == "0000":
                return {"name": "每日签到", "value": "打卡成功!"}
            elif res["status"] == "0002":
                return {"name": "每日签到", "value": res["msg"]}
            time.sleep(1)
        except Exception as e:
            return {"name": "每日签到", "value": f"错误，原因为: {e}"}

    def daily_lottery(self, session):
        daily_lottery_msg = []
        try:
            numjsp = self.get_encryptmobile(session=session)
            session.post(url="https://m.client.10010.com/mobileservicequery/customerService/share/defaultShare.htm")
            session.get(
                url="https://m.client.10010.com/dailylottery/static/doubleball/firstpage?encryptmobile=" + numjsp
            )
            session.get(
                url="https://m.client.10010.com/dailylottery/static/outdailylottery/getRandomGoodsAndInfo?areaCode=076"
            )
            session.get(
                url="https://m.client.10010.com/dailylottery/static/active/findActivityInfo?areaCode=076&groupByType=&mobile="
                    + numjsp
            )
            for i in range(3):
                luck = session.post(
                    url="https://m.client.10010.com/dailylottery/static/doubleball/choujiang?usernumberofjsp=" + numjsp
                )
                luck.encoding = "utf-8"
                res = luck.json()
                daily_lottery_msg.append(res["RspMsg"])
        except Exception as e:
            daily_lottery_msg.append(str(e))
        return {"name": "天天抽奖", "value": ";".join(daily_lottery_msg)}

    def points_lottery(self, session):
        try:
            numjsp = self.get_encryptmobile(session=session)
            one_free = session.post(
                url="https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=" + numjsp
            )
            one_free.encoding = "utf-8"
            res = one_free.json()
            jifeng_msg = res["RspMsg"]
        except Exception as e:
            jifeng_msg = str(e)
        return {"name": "积分抽奖", "value": jifeng_msg}

    @staticmethod
    def game_signin(session, mobile):
        data = {"methodType": "iOSIntegralGet", "gameLevel": "1", "deviceType": "iOS"}
        try:
            session.get(
                url=f"https://img.client.10010.com/gametask/index.html?yw_code=&desmobile={mobile}&version=android@8.0100"
            )
            time.sleep(2)
            headers = {
                "origin": "https://img.client.10010.com",
                "referer": f"https://img.client.10010.com/gametask/index.html?yw_code=&desmobile={mobile}&version=android@8.0100",
            }
            session.headers.update(headers)
            game_center_exp = session.post(url="https://m.client.10010.com/producGameApp", data=data)
            game_center_exp.encoding = "utf-8"
            res = game_center_exp.json()
            session.headers.pop("referer")
            session.headers.pop("origin")
            time.sleep(1)
            if res["code"] == "0000":
                return {"name": "游戏频道打卡", "value": f"获得{res['integralNum']}积分"}
            else:
                return {"name": "游戏频道打卡", "value": res["msg"]}
        except Exception as e:
            return {"name": "游戏频道打卡", "value": f" 错误，原因为: {e}"}

    @staticmethod
    def daily_integral_100(session):
        data = {"from": random.choice("123456789") + "".join(random.choice("0123456789") for i in range(10))}
        try:
            integral = session.post(
                url="https://m.client.10010.com/welfare-mall-front/mobile/integral/gettheintegral/v1", data=data
            )
            integral.encoding = "utf-8"
            res = integral.json()
            return {"name": "100定向积分", "value": res["msg"]}
        except Exception as e:
            return {"name": "100定向积分", "value": str(e)}

    @staticmethod
    def game_dongao(session):
        data = {"from": random.choice("123456789") + "".join(random.choice("0123456789") for i in range(10))}
        trance = [600, 300, 300, 300, 300, 300, 300]
        try:
            dongao_point = session.post(
                url="https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/getIntegral/v1", data=data
            )
            dongao_point.encoding = "utf-8"
            res1 = dongao_point.json()
            dongao_num = session.post(
                url="https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/winterTwoShop/v1", data=data
            )
            dongao_num.encoding = "utf-8"
            res2 = dongao_num.json()
            if res1["resdata"]["code"] == "0000":
                return {
                    "name": "冬奥积分活动",
                    "value": res1["resdata"]["desc"] + "，" + str(trance[int(res2["resdata"]["signDays"])]) + "积分",
                }

            else:
                return {"name": "冬奥积分活动", "value": res1["resdata"]["desc"] + "，" + res2["resdata"]["desc"]}
        except Exception as e:
            return {"name": "冬奥积分活动", "value": str(e)}

    @staticmethod
    def get_wotree_glowlist(session):
        response = session.post(url="https://m.client.10010.com/mactivity/arbordayJson/index.htm")
        res = response.json()
        return res["data"]["flowChangeList"]

    def wo_tree(self, session):
        try:
            flow_list = self.get_wotree_glowlist(session)
            num = 1
            for flow in flow_list:
                # 这里会请求很长时间，发送即请求成功
                flag = False
                try:
                    take_flow = session.get(
                        url="https://m.client.10010.com/mactivity/flowData/takeFlow.htm?flowId=" + flow["id"], timeout=1
                    )
                    take_flow.encoding = "utf-8"
                except Exception as e:
                    flag = True
                    print("【沃之树-领流量】: 4M流量 x" + str(num))
                time.sleep(1)
                num = num + 1
                if flag:
                    continue
                res1 = take_flow.json()
                if res1["code"] == "0000":
                    print("【沃之树-领流量】: 4M流量 x" + str(num))
                else:
                    print("【沃之树-领流量】: 已领取过 x" + str(num))
                time.sleep(1)
                num = num + 1
            session.post(url="https://m.client.10010.com/mactivity/arbordayJson/getChanceByIndex.htm?index=0")
            grow = session.post(url="https://m.client.10010.com/mactivity/arbordayJson/arbor/3/0/3/grow.htm")
            grow.encoding = "utf-8"
            res2 = grow.json()
            time.sleep(1)
            return {"name": "沃之树-浇水", "value": str(res2["data"]["addedValue"]) + "培养值"}
        except Exception as e:
            return {"name": "沃之树-浇水", "value": str(e)}

    @staticmethod
    def user_info(session):
        resp = session.get(url="https://m.client.10010.com/mobileService/home/queryUserInfoSeven.htm?showType=3")
        user_info_msg = []
        for one in resp.json().get("data", {}).get("dataList", []):
            user_info_msg.append({"name": one.get("remainTitle"), "value": one.get("number") + one.get("unit")})
        return user_info_msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            mobile = check_item.get("mobile")
            password = check_item.get("password")
            app_id = check_item.get("app_id")
            session, login_msg = self.login(mobile=mobile, password=password, app_id=app_id)
            if session:
                daily_daysign_msg = self.daily_daysign(session=session, mobile=mobile)
                daily_integral_100_msg = self.daily_integral_100(session=session)
                daily_lottery_msg = self.daily_lottery(session=session)
                game_dongao_msg = self.game_dongao(session=session)
                game_signin_msg = self.game_signin(session=session, mobile=mobile)
                points_lottery_msg = self.points_lottery(session=session)
                wo_tree_msg = self.wo_tree(session=session)
                user_info_msg = self.user_info(session=session)
                msg = [
                    login_msg,
                    daily_daysign_msg,
                    daily_integral_100_msg,
                    daily_lottery_msg,
                    game_dongao_msg,
                    game_signin_msg,
                    points_lottery_msg,
                    wo_tree_msg,
                ] + user_info_msg
            else:
                msg = login_msg
            msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("UNICOM", [])
    res = UniCom(check_items=_check_items).main()
    print(res)
    send("联通营业厅", res)
