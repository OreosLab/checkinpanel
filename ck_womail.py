# -*- coding: utf-8 -*-
"""
cron: 36 13 * * *
new Env('联通沃邮箱');
"""

import json
import re

import requests

from notify_mtr import send
from utils import get_data


class WoMail:
    def __init__(self, check_items):
        self.check_items = check_items
        self.user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"

    def login(self, womail_url):
        try:
            url = womail_url
            headers = {"User-Agent": self.user_agent}
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("YZKF_SESSION.*?;", set_cookie)[0]
            if "YZKF_SESSION" in cookies:
                return cookies
            else:
                print("沃邮箱获取 cookies 失败")
                return None
        except Exception as e:
            print("沃邮箱错误:", e)
            return None

    def nyan_task(self, cookies, pause21days=True):
        msg = []
        headers = {
            "User-Agent": self.user_agent,
            "Cookie": cookies,
        }
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
            res = requests.post(url=url, headers=headers)
            result = res.json()
            wxname = result.get("result").get("wxName")
            usermobile = result.get("result").get("userMobile")
            keep_sign = result["result"]["keepSign"]
            msg.append(
                {
                    "name": "帐号信息",
                    "value": f"{wxname} - {usermobile[:3]}****{usermobile[-4:]}",
                }
            )
        except Exception as e:
            keep_sign = 0
            msg.append({"name": "帐号信息", "value": str(e)})
        try:
            if pause21days and keep_sign >= 21:
                msg.append({"name": "每日签到", "value": f"昨日为打卡{keep_sign}天，今日暂停打卡"})
            else:
                url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
                res = requests.post(url=url, headers=headers).json()
                result = res.get("result")
                if result == -2:
                    msg.append({"name": "每日签到", "value": f"已签到 {keep_sign} 天"})
                elif result is None:
                    msg.append({"name": "每日签到", "value": "签到失败"})
                else:
                    msg.append({"name": "每日签到", "value": f"签到成功~已签到{result}天！"})
        except Exception as e:
            msg.append({"name": "每日签到", "value": str(e)})
        try:
            url = (
                "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            )
            data_params = {
                "每日首次登录手机邮箱": {"taskName": "loginmail"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
                "小积分抽大奖": {"taskName": "clubactivity"},
                "每日答题赢奖": {"taskName": "answer"},
                "下载沃邮箱": {"taskName": "download"},
            }
            for key, data in data_params.items():
                try:
                    res = requests.post(url=url, data=data, headers=headers).json()
                    result = res.get("result")
                    if result == 1:
                        msg.append({"name": key, "value": "做任务成功"})
                    elif result == -1:
                        msg.append({"name": key, "value": "任务已做过"})
                    elif result == -2:
                        msg.append({"name": key, "value": "请检查登录状态"})
                    else:
                        msg.append({"name": key, "value": "未知错误"})
                except Exception as e:
                    msg.append({"name": key, "value": str(e)})
        except Exception as e:
            msg.append({"name": "执行任务错误", "value": str(e)})
        return msg

    def club_task(self, womail_url, pause21days=True):
        msg = []
        userdata = re.findall("mobile.*", womail_url)[0]
        url = "https://club.mail.wo.cn/clubwebservice/?" + userdata
        headers = {"User-Agent": self.user_agent}
        try:
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("SESSION.*?;", set_cookie)[0]
            if "SESSION" in cookies:
                headers = {
                    "User-Agent": self.user_agent,
                    "Cookie": cookies,
                    "Referer": "https://club.mail.wo.cn/clubwebservice/club-user/user-info/mine-task",
                }
                # 获取账号信息
                try:
                    url = "https://club.mail.wo.cn/clubwebservice/club-user/user-info/get-user-score-info/"
                    res = requests.get(url=url, headers=headers)
                    result = res.json()
                    integraltotal = result.get("integralTotal")
                    msg.append({"name": "当前积分", "value": f"{integraltotal}"})
                    task_data = [
                        # 签到任务
                        {
                            "resourceName": "每日签到（积分）",
                            "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create?channelId=",
                        },
                        # 积分任务
                        {
                            "irid": 539,
                            "resourceName": "参与俱乐部活动",
                            "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"1":"每天只增加一次积分"}',
                            "description": "参与俱乐部活动+1积分",
                            "sourceType": 0,
                            "link": '{"jumpLink":"https://club.mail.wo.cn/clubwebservice/club-index/activity-scope?currentPage=activityScope"}',
                            "taskState": 1,
                            "show": True,
                        },
                        {
                            "irid": 545,
                            "resourceName": "俱乐部积分兑换",
                            "resourceFlag": "Web_jifenduihuan+2jifen",
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"1":"每天只增加一次积分"}',
                            "description": "俱乐部积分兑换+1积分",
                            "sourceType": 0,
                            "link": '{"jumpLink":"https://club.mail.wo.cn/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover"}',
                            "taskState": 1,
                            "show": True,
                        },
                        # 成长值任务
                        {
                            "irid": 254,
                            "resourceName": "参与俱乐部活动",
                            "resourceFlag": "activity-web",
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"limit":"true","每日限定几次":"1次"}',
                            "description": "参与俱乐部活动",
                            "sourceType": 1,
                            "link": '{"jumpLink":"https://club.mail.wo.cn/clubwebservice/club-index/activity-scope?currentPage=activityScope"}',
                            "taskState": 0,
                            "show": True,
                        },
                        {
                            "irid": 561,
                            "resourceName": "俱乐部积分兑换",
                            "resourceFlag": "Web_jifenduihuan+5chengzhangzhi",
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"limit":"true","每日限定几次":"1次"}',
                            "description": "俱乐部积分兑换+1成长值",
                            "sourceType": 1,
                            "link": '{"jumpLink":"https://club.mail.wo.cn/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover"}',
                            "taskState": 0,
                            "show": True,
                        },
                    ]
                    for task_item in task_data:
                        resource_name = task_item["resourceName"]
                        try:
                            if "每日签到" in resource_name:
                                record_url = "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/query-continuous-sign-record"
                                record_res = requests.get(
                                    url=record_url, headers=headers
                                ).json()
                                if len(record_res):
                                    new_continuous_day = record_res[0].get(
                                        "newContinuousDay"
                                    )
                                else:
                                    new_continuous_day = 0
                                if pause21days and new_continuous_day >= 21:
                                    msg.append(
                                        {
                                            "name": resource_name,
                                            "value": f"昨日为打卡{new_continuous_day}天，今日暂停打卡",
                                        }
                                    )
                                else:
                                    url = task_item["url"]
                                    res = requests.get(url=url, headers=headers).json()
                                    result = res.get("description")
                                    if "success" in result:
                                        continuous_day = json.loads(res["data"])[
                                            "continuousDay"
                                        ]
                                        msg.append(
                                            {
                                                "name": resource_name,
                                                "value": f"签到成功~已连续签到{continuous_day}天！",
                                            }
                                        )
                                    else:
                                        if "您今天已签到" in result:
                                            msg.append(
                                                {
                                                    "name": resource_name,
                                                    "value": f"签到成功~已连续签到{new_continuous_day}天！",
                                                }
                                            )
                                        else:
                                            msg.append(
                                                {"name": resource_name, "value": result}
                                            )
                            else:
                                resource_flag = task_item["resourceFlag"]
                                resource_flag = resource_flag.replace("+", "%2B")
                                url = (
                                    f"https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?resourceType={resource_flag}"
                                    if task_item["sourceType"]
                                    else f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?resourceType={resource_flag}"
                                )
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                msg.append({"name": resource_name, "value": result})
                        except Exception as e:
                            msg.append({"name": resource_name, "value": str(e)})
                except Exception as e:
                    msg.append({"name": "沃邮箱俱乐部", "value": str(e)})
            else:
                msg.append({"name": "沃邮箱俱乐部", "value": "获取 SESSION 失败"})
        except Exception as e:
            print("沃邮箱俱乐部获取 COOKIES 失败", e)
            msg.append({"name": "沃邮箱俱乐部", "value": "获取 COOKIES 失败"})
        return msg

    def core_task(self, phone, password):
        msg = []
        try:
            url = "https://mail.wo.cn/coremail/s/json?func=user:login"
            headers = {"User-Agent": "okhttp/${project.version}"}
            data_json = {"uid": str(phone), "password": str(password)}
            response = requests.post(
                url=url, headers=headers, data=json.dumps(data_json)
            )
            sid = re.findall('"sid":"(.*?)"', response.text)[0]
            set_cookie = response.headers["Set-Cookie"]
            cookie = re.findall("Coremail.*?;", set_cookie)[0]
            cookie = cookie + "Coremail.sid=" + str(sid) + ";"
            if "Coremail" not in cookie:
                msg.append({"name": "Coremail", "value": "沃邮箱获取 sid,Coremail 失败"})
                return msg
            cookies = cookie + "domain=mail.wo.cn;"
            headers = {
                "User-Agent": self.user_agent,
                "Cookie": cookies,
                "Accept": "text/x-json",
                "Content-Type": "text/x-json",
                "X-CM-SERVICE": "PHONE",
                "Origin": "https://mail.wo.cn",
                "X-Requested-With": "com.asiainfo.android",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
            }
            # 增加积分
            integral_data = {
                "每日登录": "login",
                "发送邮件": "sendMail",
                "查看邮件": "listMail",
                "登录百度网盘": "baiduCloud",
                "新建日程": "createCal",
            }
            for key, userAction in integral_data.items():
                try:
                    url = (
                        "https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid="
                        + str(sid)
                    )
                    data_json = {
                        "uid": str(phone),
                        "userAction": "" + str(userAction),
                        "userType": "integral",
                    }
                    response = requests.post(
                        url=url, headers=headers, data=json.dumps(data_json)
                    )
                    code = json.loads(response.text).get("code")
                    msg.append({"name": key, "value": "app积分结果:" + str(code)})
                except Exception as e:
                    msg.append({"name": key, "value": f"app沃邮箱执行任务错误:{e}"})
            # 增加成长值
            growth_data = {
                "每日登录": "login",
                "发送邮件": "sendMail",
                "查看邮件": "listMail",
                "登录百度网盘": "baiduCloud",
                "新建日程": "createCal",
            }
            for key, userAction in growth_data.items():
                try:
                    url = (
                        "https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid="
                        + str(sid)
                    )
                    data_json = {
                        "uid": str(phone),
                        "userAction": str(userAction),
                        "userType": "growth",
                    }
                    response = requests.post(
                        url=url, headers=headers, data=json.dumps(data_json)
                    )
                    code = response.json().get("code")
                    msg.append({"name": key, "value": "app成长值结果:" + str(code)})
                except Exception as e:
                    msg.append({"name": key, "value": f"app沃邮箱执行任务错误:{e}"})
            # 网页
            cookies = (
                cookie
                + "CoremailReferer=https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Fhxphone%2F;"
            )
            headers = {
                "User-Agent": self.user_agent,
                "Cookie": cookies,
                "Accept": "text/x-json",
                "Content-Type": "text/x-json",
                "Origin": "https://mail.wo.cn",
                "X-Requested-With": "com.tencent.mm",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
            }
            # 增加积分
            integral_data = {
                "每日登录": "login",
                "发送邮件": "sendMail",
                "查看邮件": "listMail",
                "登录百度网盘": "baiduCloud",
                "新建日程": "createCal",
                "上传文件到中转站": "uploadFile",
            }
            for key, userAction in dict.items(integral_data):
                try:
                    url = (
                        "https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid="
                        + str(sid)
                    )
                    data_json = {
                        "uid": str(phone),
                        "userAction": str(userAction),
                        "userType": "integral",
                    }
                    response = requests.post(
                        url=url, headers=headers, data=json.dumps(data_json)
                    )
                    code = response.json().get("code")
                    msg.append({"name": key, "value": "网页端积分结果:" + str(code)})
                except Exception as e:
                    msg.append({"name": key, "value": "网页端沃邮箱执行任务错误:" + str(e)})
            # 增加成长值
            growth_data = {
                "每日登录": "login",
                "发送邮件": "sendMail",
                "查看邮件": "listMail",
                "登录百度网盘": "baiduCloud",
                "新建日程": "createCal",
                "上传文件到中转站": "uploadFile",
            }
            for key, userAction in growth_data.items():
                try:
                    url = (
                        "https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid="
                        + str(sid)
                    )
                    data_json = {
                        "uid": str(phone),
                        "userAction": str(userAction),
                        "userType": "growth",
                    }
                    response = requests.post(
                        url=url, headers=headers, data=json.dumps(data_json)
                    )
                    code = response.json().get("code")
                    msg.append({"name": key, "value": "网页端成长值结果:" + str(code)})
                except Exception as e:
                    msg.append({"name": key, "value": f"网页端沃邮箱执行任务错误:{e}"})
            # 电脑
            cookies = (
                cookie
                + "domain=;CoremailReferer=https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Findex.jsp%3Fcus%3D1;"
            )
            headers = {
                "User-Agent": self.user_agent,
                "Cookie": cookies,
                "Accept": "text/x-json",
                "Content-Type": "text/x-json",
                "Origin": "https://mail.wo.cn",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
            }
            # 增加积分
            integral_data = {
                "每日登录": "login",
                "发送邮件": "sendMail",
                "查看邮件": "listMail",
                "登录百度网盘": "baiduCloud",
                "新建日程": "createCal",
                "上传文件到中转站": "uploadFile",
            }
            for key, userAction in integral_data.items():
                try:
                    url = (
                        "https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid="
                        + str(sid)
                    )
                    data_json = {"userAction": "" + str(userAction) + ""}
                    response = requests.post(
                        url=url, headers=headers, data=json.dumps(data_json)
                    )
                    code = response.json().get("code")
                    msg.append({"name": key, "value": "电脑端积分结果:" + str(code)})
                except Exception as e:
                    msg.append({"name": key, "value": "电脑端沃邮箱执行任务错误:" + str(e)})
        except Exception as e:
            msg.append({"name": "web沃邮箱错误", "value": str(e)})
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            url = check_item.get("url")
            phone = check_item.get("phone")
            password = check_item.get("password")
            pause21days = check_item.get("pause21days", True)
            try:
                cookies = self.login(womail_url=url)
                if cookies:
                    nyan_task_msg = self.nyan_task(
                        cookies=cookies, pause21days=pause21days
                    )
                    club_task_msg = self.club_task(
                        womail_url=url, pause21days=pause21days
                    )
                    core_task_msg = self.core_task(phone=phone, password=password)
                    msg = nyan_task_msg + club_task_msg + core_task_msg
                else:
                    msg = [{"name": "账号信息", "value": "登录失败"}]
            except Exception as e:
                msg = [{"name": "账号信息", "value": str(e)}]
            msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("WOMAIL", [])
    res = WoMail(check_items=_check_items).main()
    send("联通沃邮箱", res)
