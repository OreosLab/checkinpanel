# -*- coding: utf-8 -*-
"""
cron: 31 7 * * *
new Env('AcFun');
"""

import requests
import urllib3

from notify_mtr import send
from utils import get_data

urllib3.disable_warnings()


class AcFun:
    def __init__(self, check_items):
        self.check_items = check_items
        self.contentid = "27259341"

    @staticmethod
    def get_cookies(session, phone, password):
        url = "https://id.app.acfun.cn/rest/app/login/signin"
        headers = {
            "Host": "id.app.acfun.cn",
            "user-agent": "AcFun/6.39.0 (iPhone; iOS 14.3; Scale/2.00)",
            "devicetype": "0",
            "accept-language": "zh-Hans-CN;q=1, en-CN;q=0.9, ja-CN;q=0.8, zh-Hant-HK;q=0.7, io-Latn-CN;q=0.6",
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        data = f"password={password}&username={phone}"
        response = session.post(
            url=url, data=data, headers=headers, verify=False)
        acpasstoken = response.json().get("acPassToken")
        auth_key = str(response.json().get("auth_key"))
        if acpasstoken and auth_key:
            cookies = {"acPasstoken": acpasstoken, "auth_key": auth_key}
            return cookies
        else:
            return False

    @staticmethod
    def get_token(session, cookies):
        url = "https://id.app.acfun.cn/rest/web/token/get"
        data = "sid=acfun.midground.api"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = session.post(url=url, cookies=cookies,
                                data=data, headers=headers, verify=False)
        return response.json().get("acfun.midground.api_st")

    def get_video(self, session):
        url = "https://www.acfun.cn/rest/pc-direct/rank/channel"
        data = "channelId=0&rankPeriod=DAY"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = session.post(
            url=url, data=data, headers=headers, verify=False)
        self.contentid = response.json().get("rankList")[0].get("contentId")
        return self.contentid

    @staticmethod
    def sign(session, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/user/signIn"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = session.post(
            url=url, cookies=cookies, headers=headers, verify=False)
        return response.json().get("msg")

    @staticmethod
    def danmu(session, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/new-danmaku/add"
        body = "body=sitoi&color=16777215&id=27259341&mode=1&position=5019&size=25&subChannelId=84&subChannelName=%E4%B8%BB%E6%9C%BA%E5%8D%95%E6%9C%BA&type=douga&videoId=22898696"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = session.post(url=url, cookies=cookies,
                                data=body, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "弹幕成功"
        else:
            msg = "弹幕失败"
        return msg

    def throwbanana(self, session, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/banana/throwBanana"
        body = f"count=1&resourceId={self.contentid}&resourceType=2"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = session.post(url=url, cookies=cookies,
                                data=body, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "香蕉成功"
        else:
            msg = "香蕉失败"
        return msg

    def like(self, session, token):
        like_url = "https://api.kuaishouzt.com/rest/zt/interact/add"
        unlike_url = "https://api.kuaishouzt.com/rest/zt/interact/delete"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        cookies = {"acfun.midground.api_st": token, "kpn": "ACFUN_APP"}
        body = f"interactType=1&objectId={self.contentid}&objectType=2&subBiz=mainApp"
        response = session.post(url=like_url, cookies=cookies,
                                data=body, headers=headers, verify=False)
        session.post(url=unlike_url, cookies=cookies,
                     data=body, headers=headers, verify=False)
        if response.json().get("result") == 1:
            msg = "点赞成功"
        else:
            msg = "点赞失败"
        return msg

    def share(self, session, cookies):
        url = "https://api-ipv6.acfunchina.com/rest/app/task/reportTaskAction?taskType=1&market=tencent&product=ACFUN_APP&appMode=0"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = session.get(
            url=url, cookies=cookies, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "分享成功"
        else:
            msg = "分享失败"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            phone = check_item.get("phone")
            password = check_item.get("password")
            session = requests.session()

            self.get_video(session=session)
            cookies = self.get_cookies(
                session=session, phone=phone, password=password)
            token = self.get_token(session=session, cookies=cookies)

            sign_msg = self.sign(session=session, cookies=cookies)
            like_msg = self.like(session=session, token=token)
            share_msg = self.share(session=session, cookies=cookies)
            danmu_msg = self.danmu(session=session, cookies=cookies)
            throwbanana_msg = self.throwbanana(session=session, cookies=cookies)

            msg = (
                f"帐号信息: *******{phone[-4:]}\n"
                f"签到状态: {sign_msg}\n"
                f"点赞任务: {like_msg}\n"
                f"弹幕任务: {danmu_msg}\n"
                f"香蕉任务: {throwbanana_msg}\n"
                f"分享任务: {share_msg}"
            )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("ACFUN", [])
    res = AcFun(check_items=_check_items).main()
    print(res)
    send("AcFun", res)
