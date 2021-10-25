# -*- coding: utf-8 -*-
"""
cron: 8 8,12,18 * * *
new Env('企鹅电竞');
"""

import datetime
import time

import requests

from notify_mtr import send
from utils import get_data


class Egame:
    def __init__(self, check_items):
        self.check_items = check_items
        self.app_info = '{"platform":4,"terminal_type":2,"egame_id":"egame_official","imei":"","version_code":"9.9.9.9","version_name":"9.9.9.9","ext_info":{"_qedj_t":"","ALG-flag_type":"","ALG-flag_pos":""},"pvid":"344111513621080422"}'
        self.url = "https://game.egame.qq.com/cgi-bin/pgg_async_fcgi"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

    # 报名
    def attendance_sign_up(self, class_type, cookie, act_title):
        url = f"https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?pgg_gtk=1960736180&_={int(time.time()*1000)}&pgg_tk=1960736180&pgg_gtk=1960736180"
        data = {
            "param": '{"0":{"param":{"amt_type":1,"class_type":class_type_th},"module":"pgg_operation_activity_mt_svr","method":"attendance_sign_up"}}'.replace(
                "class_type_th", str(class_type)
            ),
            "app_info": '{"platform":4,"terminal_type":4,"version_code":"","version_name":"undefined","pvid":"907134976","ssid":"4238740480","imei":"0","qimei":"0"}',
        }
        headers = {
            "user-agent": self.user_agent,
            "cookie": cookie,
        }
        res = requests.post(url=url, data=data, headers=headers)
        # print(res.text)
        ret_msg = res.json().get("data", {}).get("0", {}).get("retMsg", "")
        if "余额不足" in ret_msg:
            ret_msg = "失败, 余额不足"
        msg = f"报名-{act_title}: {ret_msg}"
        return msg

    # 打卡
    def attendance_mark(self, signup_ts, class_type, cookie, act_title):
        url = f"https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?pgg_gtk=1960736180&_={int(time.time()*1000)}&pgg_tk=1960736180&pgg_gtk=1960736180"
        data = {
            "param": '{"0":{"param":{"amt_type":1,"class_type":class_type_th,"signup_ts":signup_ts_th},"module":"pgg_operation_activity_mt_svr","method":"attendance_mark"}}'.replace(
                "signup_ts_th", str(signup_ts)
            ).replace(
                "class_type_th", str(class_type)
            ),
            "app_info": '{"platform":4,"terminal_type":4,"version_code":"","version_name":"undefined","pvid":"907134976","ssid":"3056811008","imei":"0","qimei":"0"}',
        }
        headers = {
            "user-agent": self.user_agent,
            "cookie": cookie,
        }
        res = requests.post(url=url, data=data, headers=headers)
        # print(res.text)
        ret_msg = res.json().get("data", {}).get("0", {}).get("retMsg", "")
        msg = f"打卡-{act_title}: {ret_msg}\n"
        return msg

    # 获取报名情况
    def get_attendance_status(self, cookie):
        headers = {
            "user-agent": self.user_agent,
            "cookie": cookie,
        }
        for i in range(3):
            url = f"https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?pgg_gtk=1960736180&_={int(time.time()*1000)}&pgg_tk=1960736180&pgg_gtk=1960736180"
            data = {
                "param": '{"0":{"param":{"amt_type":1,"class_type":class_type_th},"module":"pgg_operation_activity_mt_svr","method":"get_attendance_status"}}'.replace(
                    "class_type_th", str(i + 1)
                ),
                "app_info": '{"platform":4,"terminal_type":4,"version_code":"","version_name":"undefined","pvid":"907134976","ssid":"855127040","imei":"0","qimei":"0"}',
            }
            res = requests.post(url=url, data=data, headers=headers).json()
            # print(str(res))
            if res.get("uid") == 0:
                msg = "cookie 失效，退出报名打卡\n"
            else:
                data = (
                    res.get("data", {}).get("0", {}).get("retBody", {}).get("data", {})
                )
                prev = data.get("prev", {})
                curr = data.get("curr", {})
                if (
                    prev.get("join_status", 0) == 1
                    and datetime.datetime.now().hour == 8
                ):  # 0: 未报名，1: 报名?，2: 要打卡?，3: 打卡了?
                    msg = f'打卡 加入状态:{prev.get("join_status")} 标题:{prev.get("act_title")} 类型:{prev.get("class_type")}\n'
                    time.sleep(1)
                    attendance_mark_msg = self.attendance_mark(
                        prev.get("signup_ts"),
                        prev.get("class_type"),
                        cookie,
                        prev.get("act_title"),
                    )
                    msg += attendance_mark_msg
                else:
                    msg = "未到打卡时间\n"
                if curr.get("join_status") == 0 and str(i + 1) in self.signin(
                    cookie
                ):  # 0: 未报名，1: 已报名
                    msg += f'报名 加入状态:{curr.get("join_status")} 标题:{curr.get("act_title")} 类型:{curr.get("class_type")}\n'
                    time.sleep(1)
                    attendance_sign_up_msg = self.attendance_sign_up(
                        prev.get("class_type"), cookie, prev.get("act_title")
                    )
                    msg += attendance_sign_up_msg
            return msg

    # 领取奖励
    def task_gift(self, cookie, id, award_desc, title):
        url = self.url
        headers = {
            "user-agent": self.user_agent,
            "cookie": cookie,
        }
        params = {
            "param": '{"key":{"module":"pgg.user_task_srf_svr.CPGGUserTaskSrfSvrObj","method":"AcquireTaskGift","param":{"task_id":task_id_th,"anchor_id":0,"role_info":{}}}}'.replace(
                "task_id_th", str(id)
            ),
            "app_info": self.app_info,
        }
        res = requests.get(url=url, headers=headers, params=params).json()
        if res["data"]["key"]["retBody"]["message"] == "成功":  # 奖励已领取
            msg = f"{award_desc} 领取成功\n"
        else:
            msg = f'{res["data"]["key"]["retBody"]["message"]}\n'
        return msg

    # 任务列表
    def task_list(self, cookie):
        msg = ""
        url = self.url
        headers = {
            "user-agent": self.user_agent,
            "cookie": cookie,
        }
        params = {
            "param": '{"key":{"module":"pgg.user_task_srf_svr.CPGGUserTaskSrfSvrObj","method":"GetUserTaskList","param":{"anchor_id":0}}}',
            "app_info": self.app_info,
        }
        res = requests.get(url=url, headers=headers, params=params).json()
        hour = datetime.datetime.now().hour
        if hour in [12, 13, 18, 19, 20]:
            time.sleep(1)
            res = requests.get(url=url, headers=headers, params=params).json()
        if res.get("uid") == 0:
            msg = "cookie 失效，退出任务奖励领取\n"
        else:
            data = res.get("data", {}).get("key", {}).get("retBody", {}).get("data", {})
            task_list = data.get("task_list", [])
            user_tab_tasks = data.get("user_tab_tasks", [])
            for i in task_list:
                if i.get("percent", 0) == 100 and i.get("acquired") == 0:
                    msg += i.get("title") + ": 任务已完成, 开始领取奖励...\n"
                    gift_msg = self.task_gift(
                        cookie,
                        i.get("id"),
                        i.get("gift", {}).get("award_desc"),
                        i.get("title"),
                    )
                    msg += gift_msg
            for i in user_tab_tasks:
                if i.get("percent", 0) == 100 and i.get("acquired") == 0:
                    msg += i.get("title") + ": 任务已完成, 开始领取奖励...\n"
                    gift_msg = self.task_gift(
                        cookie,
                        i.get("id"),
                        i.get("gift", {}).get("award_desc"),
                        i.get("title"),
                    )
                    msg += gift_msg
        return msg

    # 签到
    def signin(self, cookie):
        url = self.url
        header = {
            "user-agent": self.user_agent,
            "cookie": cookie,
        }
        params0 = {
            "param": '{"key":{"module":"pgg.user_task_srf_svr.CPGGUserTaskSrfSvrObj","method":"QueryOldUserCheckinAwards","param":{}}}',
            "app_info": self.app_info,
        }
        params1 = {
            "param": '{"key":{"module":"pgg.user_task_srf_svr.CPGGUserTaskSrfSvrObj","method":"OldUserCheckin","param":{}}}',
            "app_info": self.app_info,
        }
        res = requests.get(url, headers=header, params=params0)
        if res.json().get("uid") == 0:
            msg = "cookie 失效\n"
        elif res.json()["data"]["key"]["retBody"]["data"]["is_today_checked"] == 1:
            msg = "今日已签\n"
        else:
            res = requests.get(url=url, headers=header, params=params1)
            data = res.json()
            msg = f"签到成功, 获得{data['data']['key']['retBody']['data']['award']['description']}\n"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            sign_msg = self.signin(cookie)
            attendance_msg = self.get_attendance_status(cookie)
            task_msg = self.task_list(cookie)
            msg = sign_msg + attendance_msg + task_msg
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("EGAME", [])
    res = Egame(check_items=_check_items).main()
    send("EGAME", res)
