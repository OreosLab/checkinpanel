# -*- coding: utf-8 -*-
"""
cron: 26 13 * * *
new Env('NGA');
"""

import re
import time

import requests

from notify_mtr import send
from utils import get_data


class NGA:
    def __init__(self, check_items):
        self.check_items = check_items
        self.url = "https://ngabbs.com/nuke.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
            "Chrome/83.0.4103.106 Mobile Safari/537.36 Nga_Official/90021",
            "X-Requested-With": "gov.pianzong.androidnga",
            "X-USER-AGENT": "Nga_Official/90021(HUAWEI NOH-AN00;Android 10)",
        }

    def signin(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "check_in",
            "__lib": "check_in",
            "__output": "12",
        }
        return requests.post(self.url, data, headers=self.headers).json()

    def get_silver_coin(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "mid": "2",
            "__act": "check_mission",
            "__lib": "mission",
            "__output": "11",
        }
        try:
            res = requests.post(self.url, data, headers=self.headers).json()
            stat = res["data"][0]
            silver_coin_get_stat = stat[4] if "已经" in stat[4] else stat[2]["2"]
        except Exception as e:
            silver_coin_get_stat = str(e)
        return silver_coin_get_stat

    def get_n_coin(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "mid": "30",
            "__act": "check_mission",
            "__lib": "mission",
            "__output": "11",
        }
        try:
            res = requests.post(self.url, data, headers=self.headers).json()
            stat = res["data"][0]
            n_coin_get_stat = stat[4] if "已经" in stat[4] else stat[2]["30"]
        except Exception as e:
            n_coin_get_stat = str(e)
        return n_coin_get_stat

    def view_video(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "video_view_task_counter_add_v2",
            "__lib": "mission",
            "__output": "11",
        }
        success_sum = 0
        failure_sum = 0
        failure_msg = ""
        failure_msg_all = ""
        for _ in range(4):
            try:
                res = requests.post(self.url, data, headers=self.headers).json()
                time.sleep(30)
                raw_stat = re.search(r"\'raw_stat\':\s*{([^}]+)", str(res))[1]
                task_code = re.search(r"\'6\':\s(\d)", raw_stat)[1]
                time_code = re.search(r"\'5\':\s(\d)", raw_stat)[1]
                if task_code == "1" or (task_code == "0" and time_code == "1"):
                    success_sum += 1
            except Exception as e:
                failure_msg = str(e)
                failure_sum += 1
            failure_msg_all += failure_msg + "\n"
        video_coin = success_sum // 2 * 1
        return (
            f"观看视频成功次数：{success_sum}，共获得N币：{video_coin}"
            if failure_sum == 0
            else f"观看视频成功次数：{success_sum}，共获得N币：{video_coin}；\n"
            f"观看视频失败次数：{failure_sum}；\n"
            f"错误信息：{failure_msg_all}"
        )

    def view_video_for_adfree_24h(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "video_view_task_counter_add_v2_for_adfree_sp1",
            "__lib": "mission",
            "__output": "11",
        }
        try:
            res = requests.post(self.url, data, headers=self.headers).json()
            time.sleep(30)
            if str(res["data"][1][0]) == "{}":
                code = res["data"][1][1]["141"]["raw_stat"]["6"]
            else:
                code = res["data"][1][0]["141"]["raw_stat"]["6"]
            adfree_24h_stat = "已获得免广告状态：24h" if code == 1 else "观看视频失败！"
        except Exception as e:
            adfree_24h_stat = str(e)
        return adfree_24h_stat

    def view_video_for_adfree(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "video_view_task_counter_add_v2_for_adfree",
            "__lib": "mission",
            "__output": "11",
        }
        ids = ("142", "143", "144", "145")
        success_sum = 0
        failure_sum = 0
        failure_msg = ""
        failure_msg_all = ""
        code = {}
        for i, item in enumerate(ids):
            try:
                res = requests.post(self.url, data, headers=self.headers).json()
                time.sleep(30)
                code[i] = res["data"][1][0][item]["raw_stat"]["6"]
                if code[i] == 1:
                    success_sum += 1
                else:
                    failure_sum += 1
            except Exception as e:
                failure_msg = str(e)
                failure_sum += 1
            failure_msg_all += failure_msg + "\n"
        adfree_time = success_sum * 6
        return (
            f"观看视频成功次数：{success_sum}，共获得免广告时长：{adfree_time}h"
            if failure_sum == 0
            else f"观看视频成功次数：{success_sum}，共获得免广告时长：{adfree_time} h；\n"
            f"观看视频失败次数：{failure_sum}；\n"
            f"错误信息：{failure_msg_all}"
        )

    def get_signin_stat(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "sign": "",
            "app_id": "1010",
            "__act": "get_stat",
            "__lib": "check_in",
            "__output": "14",
        }
        res = requests.post(self.url, data, headers=self.headers).json()["result"][0]
        continued = res["continued"]
        total = res["sum"]
        return continued, total

    def get_user(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "sign": "",
            "app_id": "1010",
            "__act": "iflogin",
            "__lib": "login",
            "__output": "12",
        }
        res = requests.post(self.url, data, headers=self.headers).json()
        return res["result"]["username"]

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            token = check_item.get("token")
            uid = check_item.get("uid")
            signin_res = self.signin(token, uid)
            try:
                continued, total = self.get_signin_stat(token, uid)
                username = self.get_user(token, uid)
                if signin_res["code"] == 0:
                    signin_stat = (
                        f"用户：{username}\n统计信息：签到成功，连续签到{continued}天，累计签到{total}天"
                    )
                elif signin_res["code"] == 1:
                    signin_stat = (
                        f"用户：{username}\n统计信息：今日已签，连续签到{continued}天，累计签到{total}天"
                    )
                else:
                    signin_stat = f'用户：{username}\n统计信息：{signin_res["msg"]}'
                time.sleep(1)
                silver_coin_get_stat = self.get_silver_coin(token, uid)
                n_coin_get_stat = self.get_n_coin(token, uid)
                video_view_stat = self.view_video(token, uid)
                adfree_24h_stat = self.view_video_for_adfree_24h(token, uid)
                msg = (
                    f"{signin_stat}\n"
                    f"------【每日签到得银币】------\n"
                    f"{silver_coin_get_stat}\n"
                    f"------【每日签到得N币】------\n"
                    f"{n_coin_get_stat}\n"
                    f"------【每天看两次视频】------\n"
                    f"{video_view_stat}\n"
                    f"------【看视频免广告(限时任务)】------\n"
                    f"{adfree_24h_stat}\n"
                )
            except Exception as e:
                msg = str(e)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("NGA", [])
    result = NGA(check_items=_check_items).main()
    send("NGA", result)
