# -*- coding: utf-8 -*-
"""
建议cron: 31 7 * * *
new Env('AcFun');
"""

import json, requests, urllib3
from getENV import getENv
from checksendNotify import send

urllib3.disable_warnings()


class AcFunCheckIn:
    def __init__(self, acfun_account_list):
        self.acfun_account_list = acfun_account_list
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
            "content-type": "application/x-www-form-urlencoded",
        }
        data = f"password={password}&username={phone}"
        response = session.post(url=url, data=data, headers=headers, verify=False)
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
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = session.post(url=url, cookies=cookies, data="sid=acfun.midground.api", headers=headers, verify=False)
        return response.json().get("acfun.midground.api_st")

    def get_video(self, session):
        url = "https://api-ipv6.acfunchina.com/rest/app/rank/channel"
        data = "channelId=0&rankPeriod=DAY"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = session.post(url=url, data=data, headers=headers, verify=False)
        self.contentid = response.json().get("rankList")[0].get("contentId")
        return self.contentid

    @staticmethod
    def sign(session, cookies):
        headers = {"acPlatform": "IPHONE"}
        response = session.post(
            url="https://api-ipv6.acfunchina.com/rest/app/user/signIn", headers=headers, cookies=cookies, verify=False
        )
        return response.json().get("msg")

    @staticmethod
    def danmu(session, cookies):
        url = "https://api-ipv6.acfunchina.com/rest/app/new-danmaku/add"
        body = "body=sitoi&color=16777215&id=27259341&mode=1&position=5019&size=25&subChannelId=84&subChannelName=%E4" \
               "%B8%BB%E6%9C%BA%E5%8D%95%E6%9C%BA&type=douga&videoId=22898696 "
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = session.post(url=url, headers=headers, cookies=cookies, data=body, verify=False)
        if response.json().get("result") == 0:
            msg = "弹幕成功"
        else:
            msg = "弹幕失败"
        return msg

    def throwbanana(self, session, cookies):
        url = "https://api-ipv6.acfunchina.com/rest/app/banana/throwBanana"
        body = f"count=1&resourceId={self.contentid}&resourceType=2"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = session.post(url=url, headers=headers, cookies=cookies, data=body, verify=False)
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
        }
        cookies = {"acfun.midground.api_st": token, "kpn": "ACFUN_APP"}
        body = f"interactType=1&objectId={self.contentid}&objectType=2&subBiz=mainApp"
        response = session.post(url=like_url, headers=headers, cookies=cookies, data=body, verify=False)
        session.post(url=unlike_url, headers=headers, cookies=cookies, data=body, verify=False)
        if response.json().get("result") == 1:
            msg = "点赞成功"
        else:
            msg = "点赞失败"
        return msg

    def share(self, session, cookies):
        url = "https://api-ipv6.acfunchina.com/rest/app/task/reportTaskAction?taskType=1&market=tencent&product=ACFUN_APP&appMode=0"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = session.get(url=url, headers=headers, cookies=cookies, verify=False)
        if response.json().get("result") == 0:
            msg = "分享成功"
        else:
            msg = "分享失败"
        return msg

    def main(self):
        msg_all = ""
        for acfun_account in self.acfun_account_list:
            phone = acfun_account.get("acfun_phone")
            password = acfun_account.get("acfun_password")
            session = requests.session()
            self.get_video(session=session)
            cookies = self.get_cookies(session=session, phone=phone, password=password)
            token = self.get_token(session=session, cookies=cookies)
            sign_msg = self.sign(session=session, cookies=cookies)
            like_msg = self.like(session=session, token=token)
            share_msg = self.share(session=session, cookies=cookies)
            danmu_msg = self.danmu(session=session, cookies=cookies)
            throwbanana_msg = self.throwbanana(session=session, cookies=cookies)
            msg = (
                f"帐号信息: {phone}\n签到状态: {sign_msg}\n点赞任务: {like_msg}\n"
                f"弹幕任务: {danmu_msg}\n香蕉任务: {throwbanana_msg}\n分享任务: {share_msg}"
            )
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
    else:
        print('加载配置文件失败，请检查！')
        exit(1)
    _acfun_account_list = datas.get("ACFUN_ACCOUNT_LIST", [])
    res = AcFunCheckIn(acfun_account_list=_acfun_account_list).main()
    print(res)
    send('AcFun', res)