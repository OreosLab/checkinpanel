# -*- coding: utf-8 -*-
"""
cron: 36 13 * * *
new Env('联通沃邮箱');
"""

import re

import requests

from notify_mtr import send
from utils import get_data


class WoMail:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def login(url):
        try:
            url = url
            headers = {
                "User-Agent":
                    "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
            }
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

    @staticmethod
    def dotask(cookies):
        msg = ""
        headers = {
            "User-Agent":
                "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
            "Cookie": cookies
        }
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
            res = requests.post(url=url, headers=headers)
            result = res.json()
            wxname = result.get("result").get("wxName")
            usermobile = result.get("result").get("userMobile")
            userdata = f"帐号信息: {wxname} - {usermobile[:3]}****{usermobile[-4:]}\n"
            msg += userdata
        except Exception as e:
            print("沃邮箱获取用户信息失败", e)
            msg += "沃邮箱获取用户信息失败\n"
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
            res = requests.post(url=url, headers=headers).json()
            result = res.get("result")
            if result == -2:
                msg += "每日签到: 已签到\n"
            elif result is None:
                msg += "每日签到: 签到失败\n"
            else:
                msg += f"每日签到: 签到成功~已签到{result}天！\n"
        except Exception as e:
            print("沃邮箱签到错误", e)
            msg += "沃邮箱签到错误\n"
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "每日首次登录手机邮箱": {
                    "taskName": "loginmail"
                },
                "和WOWO熊一起寻宝": {
                    "taskName": "treasure"
                },
                "去用户俱乐部逛一逛": {
                    "taskName": "club"
                }
            }
            for key, data in data_params.items():
                try:
                    res = requests.post(url=url, data=data,
                                        headers=headers).json()
                    result = res.get("result")
                    if result == 1:
                        msg += f"{key}: 做任务成功\n"
                    elif result == -1:
                        msg += f"{key}: 任务已做过\n"
                    elif result == -2:
                        msg += f"{key}: 请检查登录状态\n"
                    else:
                        msg += f"{key}: 未知错误\n"
                except Exception as e:
                    print(f"沃邮箱执行任务【{key}】错误", e)
                    msg += f"沃邮箱执行任务【{key}】错误"

        except Exception as e:
            print("沃邮箱执行任务错误", e)
            msg += "沃邮箱执行任务错误错误"
        return msg

    @staticmethod
    def dotask2(url):
        msg = ""
        userdata = re.findall("mobile.*", url)[0]
        url = "https://club.mail.wo.cn/clubwebservice/?" + userdata
        headers = {
            "User-Agent":
                "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
        }
        try:
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("SESSION.*?;", set_cookie)[0]
            if "SESSION" in cookies:
                headers = {
                    "User-Agent":
                        "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
                    "Cookie": cookies,
                    "Referer":
                        "https://club.mail.wo.cn/clubwebservice/club-user/user-info/mine-task"
                }
                # 获取用户信息
                try:
                    url = "https://club.mail.wo.cn/clubwebservice/club-user/user-info/get-user-score-info/"
                    res = requests.get(url=url, headers=headers)
                    result = res.json()
                    integraltotal = result.get("integralTotal")
                    usermobile = result.get("userPhoneNum")
                    userdata = f"帐号信息: {usermobile[:3]}****{usermobile[-4:]}\n当前积分:{integraltotal}\n"
                    msg += userdata
                    integral_task_data = [
                        {
                            "resourceName": "每日签到（积分）",
                            "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create"
                        },
                        {
                            "irid": 539,
                            "resourceName": "参与俱乐部活动",
                            "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/club-index/activity-scope?currentPage=activityScope"}',
                            "description": "Web端参与俱乐部活动+1积分"
                        },
                        {
                            "irid": 545,
                            "resourceName": "俱乐部积分兑换",
                            "resourceFlag": "Web_jifenduihuan+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData":
                            '{"jumpLink":"/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover"}',
                            "description": "Web端积分兑换+1积分"
                        }
                    ]
                    lenth = len(integral_task_data)
                    # msg+="--------积分任务--------\n"
                    # 执行积分任务
                    for i in range(lenth):
                        resource_name = integral_task_data[i]["resourceName"]
                        try:
                            if "每日签到" in resource_name:
                                url = integral_task_data[i]["url"]
                                res = requests.get(url=url,
                                                   headers=headers).json()
                                result = res.get("description")
                                if "success" in result:
                                    continuous_day = res["data"][
                                        "continuousDay"]
                                    msg += f"{resource_name}: 签到成功~已连续签到{str(continuous_day)}天！\n"
                                else:
                                    msg += f"{resource_name}: {result}\n"
                            else:
                                resource_flag = integral_task_data[i][
                                    "resourceFlag"]
                                resource_flag = resource_flag.replace(
                                    "+", "%2B")
                                url = f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={usermobile}&resourceType={resource_flag}"
                                res = requests.get(url=url,
                                                   headers=headers).json()
                                result = res.get("description")
                                msg += f"{resource_name}: {result}\n"
                        except Exception as e:
                            print(f"沃邮箱俱乐部执行任务【{resource_name}】错误", e)
                            msg += f"沃邮箱俱乐部执行任务【{resource_name}】错误"
                    growthtask_data = [
                        {
                            "resourceName": "每日签到（积分）",
                            "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create"
                        },
                        {
                            "irid": 539,
                            "resourceName": "参与俱乐部活动",
                            "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/club-index/activity-scope?currentPage=activityScope"}',
                            "description": "Web端参与俱乐部活动+1积分"
                        },
                        {
                            "irid": 545,
                            "resourceName": "俱乐部积分兑换",
                            "resourceFlag": "Web_jifenduihuan+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover"}',
                            "description": "Web端积分兑换+1积分"
                        }
                    ]
                    lenth = len(growthtask_data)
                    for i in range(lenth):
                        resource_name = growthtask_data[i]["resourceName"]
                        try:
                            if "每日签到" in resource_name:
                                url = growthtask_data[i]["url"]
                                res = requests.get(url=url,
                                                   headers=headers).json()
                                result = res.get("description")
                                if "success" in result:
                                    continuous_day = res["data"][
                                        "continuousDay"]
                                    msg += f"{resource_name}: 签到成功~已连续签到{str(continuous_day)}天！\n"
                                else:
                                    msg += f"{resource_name}: {result}\n"
                            else:
                                resource_flag = growthtask_data[i][
                                    "resourceFlag"]
                                resource_flag = resource_flag.replace(
                                    "+", "%2B")
                                url = f"https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?phoneNum={usermobile}&resourceType={resource_flag}"
                                res = requests.get(url=url,
                                                   headers=headers).json()
                                result = res.get("description")
                                msg += f"{resource_name}: {result}\n"
                        except Exception as e:
                            print(f"沃邮箱俱乐部执行任务【{resource_name}】错误", e)
                            msg += f"沃邮箱俱乐部执行任务【{resource_name}】错误"
                except Exception as e:
                    print("沃邮箱俱乐部获取用户信息失败", e)
                    msg += "沃邮箱俱乐部获取用户信息失败\n"
            else:
                msg += "沃邮箱俱乐部获取SESSION失败\n"
        except Exception as e:
            print("沃邮箱俱乐部获取cookies失败", e)
            msg += "沃邮箱俱乐部获取cookies失败\n"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            url = check_item.get("url")
            try:
                cookies = self.login(url)
                if cookies:
                    msg = self.dotask(cookies)
                    msg += f"\n沃邮箱俱乐部\n{self.dotask2(url)}"
                else:
                    msg = "登录失败"
            except Exception as e:
                print(e)
                msg = "登录失败"
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("WOMAIL", [])
    res = WoMail(check_items=_check_items).main()
    print(res)
    send("联通沃邮箱", res)
