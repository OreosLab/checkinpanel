# -*- coding: utf-8 -*-
"""
cron: 55 10 * * *
new Env('腾讯视频');
"""

import re
import time
from urllib import parse

import requests

from notify_mtr import send
from utils import get_data


class VQQ:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def refresh_cookie(url, headers, cookies):
        login = requests.get(url=url, headers=headers, cookies=cookies)
        nick = re.findall(r'nick":"(.*?)"', login.text)
        if nick:
            nick = nick[0]
            try:
                nick = parse.unquote(nick)
            except Exception as e:
                print(f"nick 转换失败: {e}")
        else:
            nick = "未获取到用户"
        cookie = requests.utils.dict_from_cookiejar(login.cookies)
        return cookie, nick

    @staticmethod
    def sign_once(headers, cookies):
        url = "http://v.qq.com/x/bu/mobile_checkin?isDarkMode=0&uiType=REGULAR"
        res = requests.get(url=url, headers=headers, cookies=cookies)
        res.encoding = "utf8"
        match = re.search(r'isMultiple" />\s+(.*?)\s+<', res.text)
        if "isMultiple" in res.text:
            try:
                value = match.group(1)
            except Exception:
                print(res.text)
                value = "数据获取失败"
            msg = f"成长值x{value}"
        elif "Unauthorized" in res.text:
            msg = "cookie 失效"
        else:
            msg = "签到失败(可能已签到)\n签到失败: 自行在腾讯视频APP内登录网址签到 http://v.qq.com/x/bu/mobile_checkin (基本每周都需要手动签到一次才可以)"
        return msg

    @staticmethod
    def sign_twice(headers, cookies):
        this_time = int(round(time.time() * 1000))
        url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2&_=" + \
            str(this_time)
        res = requests.get(url=url, headers=headers, cookies=cookies)
        res.encoding = "utf8"
        if "Account Verify Error" in res.text:
            msg = "签到失败-Cookie失效"
        elif "Not VIP" in res.text:
            msg = "非会员无法签到"
        else:
            try:
                value = re.search('checkin_score": (.*?),', res.text).group(1)
            except Exception as e:
                print("获取成长值失败", e)
                value = res.text
            msg = f"成长值x{value}"
        return msg

    @staticmethod
    def tasks(headers, cookies):
        task_map = {
            "1": "观看视频60min",
            "3": "使用弹幕特权",
            "6": "使用赠片特权",
            "7": "使用下载特权",
        }
        task_msg_list = []
        for task_id, task_name in task_map.items():
            this_time = int(round(time.time() * 1000))
            url = f"https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id={task_id}&_=${this_time}"
            res = requests.get(url=url, headers=headers, cookies=cookies)
            res.encoding = "utf8"
            if "score" in res.text:
                msg = "获得+10成长值"
            elif "已发过货" in res.text:
                msg = "任务已完成"
            elif "任务未完成" in res.text:
                msg = "任务未完成，需手动完成任务"
            else:
                msg = res.text
            task_msg_list.append(f"{task_name}: {msg}")
            time.sleep(1)
        return "\n".join(task_msg_list)

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            auth_refresh = check_item.get("auth_refresh")
            if not auth_refresh:
                return "参数错误: 缺少 auth_refresh 参数，请查看配置文档"
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }
            headers = {
                "Referer": "https://v.qq.com",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
            }
            login_cookie, nick = self.refresh_cookie(url=auth_refresh,
                                                     headers=headers,
                                                     cookies=cookie)
            if login_cookie.get("main_login") == "qq":
                cookie["vqq_vusession"] = login_cookie.get("vqq_vusession")
            else:
                cookie["vusession"] = login_cookie.get("vusession")
                cookie["access_token"] = login_cookie.get("access_token")
            sign_once_msg = self.sign_once(headers=headers, cookies=cookie)
            sign_twice_msg = self.sign_twice(headers=headers, cookies=cookie)
            task_msg = self.tasks(headers=headers, cookies=cookie)
            msg = f"用户信息: {nick}\n签到奖励1: {sign_once_msg}\n签到奖励2: {sign_twice_msg}\n{task_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("VQQ", [])
    res = VQQ(check_items=_check_items).main()
    print(res)
    send("腾讯视频", res)
