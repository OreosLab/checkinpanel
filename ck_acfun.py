# -*- coding: utf-8 -*-
"""
cron: 31 7 * * *
new Env('AcFun');
"""

import re

import requests

from notify_mtr import send
from utils import get_data


class AcFun:
    def __init__(self, check_items):
        self.check_items = check_items
        self.contentid = "27259341"
        self.st = ""

    @staticmethod
    def login(phone, password, session):
        url = "https://id.app.acfun.cn/rest/web/login/signin"
        body = f"username={phone}&password={password}&key=&captcha="
        res = session.post(url=url, data=body).json()
        return (True, res) if res.get("result") == 0 else (False, res.get("err_msg"))

    def get_video(self, session):
        url = "https://www.acfun.cn/rest/pc-direct/rank/channel"
        res = session.get(url=url).json()
        self.contentid = res.get("rankList")[0].get("contentId")

    @staticmethod
    def sign(session):
        url = "https://www.acfun.cn/rest/pc-direct/user/signIn"
        res = session.post(url=url).json()
        return res.get("msg")

    def danmu(self, session):
        url = "https://www.acfun.cn/rest/pc-direct/new-danmaku/add"
        data = {
            "mode": "1",
            "color": "16777215",
            "size": "25",
            "body": "123321",
            "videoId": "26113662",
            "position": "2719",
            "type": "douga",
            "id": "31224739",
            "subChannelId": "1",
            "subChannelName": "动画",
        }
        response = session.get(url=f"https://www.acfun.cn/v/ac{self.contentid}")
        videoId = re.findall(r'"currentVideoId":(\d+),', response.text)
        subChannel = re.findall(
            r'{subChannelId:(\d+),subChannelName:"([\u4e00-\u9fa5]+)"}', response.text
        )
        if videoId:
            data["videoId"] = videoId[0]
            data["subChannelId"] = subChannel[0][0]
            data["subChannelName"] = subChannel[0][1]
        res = session.post(url=url, data=data).json()
        return "弹幕成功" if res.get("result") == 0 else "弹幕失败"

    def get_token(self, session):
        url = "https://id.app.acfun.cn/rest/web/token/get?sid=acfun.midground.api"
        res = session.post(url=url).json()
        self.st = res.get("acfun.midground.api_st") if res.get("result") == 0 else ""

    def like(self, session):
        like_url = "https://kuaishouzt.com/rest/zt/interact/add"
        unlike_url = "https://kuaishouzt.com/rest/zt/interact/delete"
        body = (
            f"kpn=ACFUN_APP&kpf=PC_WEB&subBiz=mainApp&interactType=1&"
            f"objectType=2&objectId={self.contentid}&acfun.midground.api_st={self.st}&"
            f"extParams%5BisPlaying%5D=false&extParams%5BshowCount%5D=1&extParams%5B"
            f"otherBtnClickedCount%5D=10&extParams%5BplayBtnClickedCount%5D=0"
        )
        res = session.post(url=like_url, data=body).json()
        session.post(url=unlike_url, data=body)
        return "点赞成功" if res.get("result") == 1 else "点赞失败"

    def throwbanana(self, session):
        url = "https://www.acfun.cn/rest/pc-direct/banana/throwBanana"
        data = {"resourceId": self.contentid, "count": "1", "resourceType": "2"}
        res = session.post(url=url, data=data).json()
        return "投🍌成功" if res.get("result") == 0 else "投🍌失败"

    @staticmethod
    def get_info(session):
        url = "https://www.acfun.cn/rest/pc-direct/user/personalInfo"
        res = session.get(url=url).json()
        if res.get("result") != 0:
            return "查询失败"
        info = res.get("info")
        return f'当前等级: {info.get("level")}\n持有香蕉: {info.get("banana")}'

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            phone = check_item.get("phone")
            password = check_item.get("password")

            s = requests.session()
            s.headers.update(
                {
                    "accept": "*/*",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70",
                    "Referer": "https://www.acfun.cn/",
                }
            )

            flag, res = self.login(phone, password, s)

            if flag is True:
                self.get_video(s)
                self.get_token(s)

                msg = (
                    f"帐号信息: *******{phone[-4:]}\n"
                    f"签到状态: {self.sign(s)}\n"
                    f"点赞任务: {self.like(s)}\n"
                    f"弹幕任务: {self.danmu(s)}\n"
                    f"香蕉任务: {self.throwbanana(s)}\n"
                    f"{self.get_info(s)}"
                )

            else:
                msg = f"*******{phone[-4:]} {res}"

            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("ACFUN", [])
    result = AcFun(check_items=_check_items).main()
    send("AcFun", result)
