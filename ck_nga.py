# -*- coding: utf-8 -*-
"""
cron: 6,26 13 * * *
new Env('NGA');
"""
import json
import time

import requests

from notify_mtr import send
from utils import get_data

requests.packages.urllib3.disable_warnings()


class NGA:
    def __init__(self, check_items):
        self.check_items = check_items
        self.url = "https://ngabbs.com/nuke.php"
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Nga_Official/90021",
            "X-Requested-With": "gov.pianzong.androidnga",
            "X-USER-AGENT": "Nga_Official/90021(HUAWEI NOH-AN00;Android 10)"
        }

    def signin(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "check_in",
            "__lib": "check_in",
            "__output": "12"
        }
        req = requests.post(self.url,
                            headers=self.headers,
                            data=data,
                            verify=False).content
        # print(json.loads(req))
        return json.loads(req)

    def silver_coin_get(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "mid": "2",
            "__act": "check_mission",
            "__lib": "mission",
            "__output": "11"
        }
        res = requests.post(self.url,
                            headers=self.headers,
                            data=data,
                            verify=False).content
        res = json.loads(res)
        data = res["data"][0]
        # print(data)
        try:
            if "已经" in data[4]:
                silver_coin_get_stat = data[4]
            else:
                silver_coin_get_stat = data[2]["2"]
        except Exception as e:
            silver_coin_get_stat = e
        return silver_coin_get_stat

    def N_coin_get(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "mid": "30",
            "__act": "check_mission",
            "__lib": "mission",
            "__output": "11"
        }
        res = requests.post(self.url,
                            headers=self.headers,
                            data=data,
                            verify=False).content
        res = json.loads(res)
        data = res["data"][0]
        # print(data)
        try:
            if "已经" in data[4]:
                N_coin_get_stat = data[4]
            else:
                N_coin_get_stat = data[2]["30"]
        except Exception as e:
            N_coin_get_stat = str(e)
        return N_coin_get_stat

    def view_video(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "video_view_task_counter_add_v2",
            "__lib": "mission",
            "__output": "11"
        }
        ids = ("157", "157", "158", "158")
        success_sum = 0
        failure_sum = 0
        failure_msg = ""
        failure_msg_all = ""
        task_code = {}
        time_code = {}
        for i in range(len(ids)):
            try:
                res = requests.post(self.url,
                                    headers=self.headers,
                                    data=data,
                                    verify=False).content
                res = json.loads(res)
                # print(res)
                time.sleep(30)
                if str(res["data"][1][0]) == "{}":
                    task_code[i] = res["data"][1][1][ids[i]]["raw_stat"]["6"]
                    time_code[i] = res["data"][1][1][ids[i]]["raw_stat"]["5"]
                else:
                    task_code[i] = res["data"][1][0][ids[i]]["raw_stat"]["6"]
                    time_code[i] = res["data"][1][0][ids[i]]["raw_stat"]["5"]
                if task_code[i] == 1:
                    success_sum += 1
                elif task_code[i] == 0 and time_code == 1:
                    success_sum += 1
            except Exception as e:
                failure_msg = str(e)
                failure_sum += 1
            failure_msg_all += failure_msg + "\n"
        video_coin = success_sum // 2 * 1
        video_view_stat = f"观看视频成功次数：{success_sum}，共获得N币：{video_coin}" if failure_sum == 0 else f"观看视频成功次数：{success_sum}，共获得N币：{video_coin}；\n观看视频失败次数：{failure_sum}；\n错误信息：{failure_msg_all}"
        return video_view_stat

    def view_video_for_adfree_24h(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "app_id": "1010",
            "__act": "video_view_task_counter_add_v2_for_adfree_sp1",
            "__lib": "mission",
            "__output": "11"
        }
        try:
            res = requests.post(self.url,
                                headers=self.headers,
                                data=data,
                                verify=False).content
            res = json.loads(res)
            # print(res)
            time.sleep(30)
            if str(res["data"][1][0]) == "{}":
                code = res["data"][1][1]["141"]["raw_stat"]["6"]
            else:
                code = res["data"][1][0]["141"]["raw_stat"]["6"]
            if code == 1:
                adfree_24h_stat = "已获得免广告状态：24h"
            else:
                adfree_24h_stat = "观看视频失败！"
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
            "__output": "11"
        }
        ids = ("142", "143", "144", "145")
        success_sum = 0
        failure_sum = 0
        failure_msg = ""
        failure_msg_all = ""
        code = {}
        for i in range(len(ids)):
            try:
                res = requests.post(self.url,
                                    headers=self.headers,
                                    data=data,
                                    verify=False).content
                res = json.loads(res)
                time.sleep(30)
                code[i] = res["data"][1][0][ids[i]]["raw_stat"]["6"]
                if code[i] == 1:
                    success_sum += 1
                else:
                    failure_sum += 1
            except Exception as e:
                failure_msg = str(e)
                failure_sum += 1
            failure_msg_all += failure_msg + "\n"
        adfree_time = success_sum * 6
        adfree_stat = f"观看视频成功次数：{success_sum}，共获得免广告时长：{adfree_time}h" if failure_sum == 0 else f"观看视频成功次数：{success_sum}，共获得免广告时长：{adfree_time}h；\n观看视频失败次数：{failure_sum}；\n错误信息：{failure_msg_all}"
        return adfree_stat

    def get_signin_stat(self, token, uid):
        data = {
            "access_token": token,
            "t": round(time.time()),
            "access_uid": uid,
            "sign": "",
            "app_id": "1010",
            "__act": "get_stat",
            "__lib": "check_in",
            "__output": "14"
        }
        res = requests.post(self.url,
                            headers=self.headers,
                            data=data,
                            verify=False).content
        res = json.loads(res)
        result = res["result"][0]
        continued = result["continued"]
        total = result["sum"]
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
            "__output": "12"
        }
        req = requests.post(self.url,
                            headers=self.headers,
                            data=data,
                            verify=False).content
        req = json.loads(req)["result"]["username"]
        return req

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            token = check_item.get("token")
            uid = check_item.get("uid")
            signin_res = self.signin(token=token, uid=uid)
            try:
                continued, total = self.get_signin_stat(token=token, uid=uid)
                username = self.get_user(token=token, uid=uid)
                if signin_res["code"] == 0:
                    signin_stat = f"用户：{username}\n统计信息：签到成功，连续签到{continued}天，累计签到{total}天"
                elif signin_res["code"] == 1:
                    signin_stat = f"用户：{username}\n统计信息：今日已签，连续签到{continued}天，累计签到{total}天"
                time.sleep(1)
                silver_coin_get_stat = self.silver_coin_get(token=token,
                                                            uid=uid)
                N_coin_get_stat = self.N_coin_get(token=token, uid=uid)
                video_view_stat = self.view_video(token=token, uid=uid)
                adfree_24h_stat = self.view_video_for_adfree_24h(token=token,
                                                                 uid=uid)
                # adfree_stat = self.view_video_for_adfree(token=token, uid=uid)
                msg = (
                    f"{signin_stat}\n"
                    f"------【每日签到得银币】------\n{silver_coin_get_stat}\n"
                    f"------【每日签到得N币】------\n{N_coin_get_stat}\n"
                    f"------【每天看两次视频】------\n{video_view_stat}\n"
                    f"------【看视频免广告(限时任务)】------\n{adfree_24h_stat}\n"
                )
            except Exception as e:
                msg = str(e)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("NGA", [])
    res = NGA(check_items=_check_items).main()
    print(res)
    send("NGA", res)
