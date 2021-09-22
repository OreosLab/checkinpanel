# -*- coding: utf-8 -*-
"""
cron: 19 5,21 * * *
new Env('欢太商城');
"""

import json
import os
import re
import time
import traceback

import requests

import utils_tmp
from notify_mtr import send  # 云函数采用青龙 notify.py，改为 import notify
from utils import get_data  # 云函数删除该行


class Heytap:
    def __init__(self, config):
        self.client = None
        self.session = requests.session()
        self.login = config["HEYTAP"]
        self.log = ""
        self.config = config
        self.HT_cookies = "cookie"
        self.HT_UserAgent = "ua"
        self.s_channel = "oppostore"
        self.source_type = "505"  # 初始化设置为505，会从cookie获取实际数据
        self.sa_distinct_id = ""
        self.sa_device_id = ""
        self.s_version = ""
        self.brand = "iPhone"  # 初始化设置为iPhone，会从cookie获取实际机型
        self.act_task = utils_tmp.act_list  # 修改为从文件获取，避免更新代码后丢失原有活动配置
        self.if_draw = False  # 初始化设置为False，会从配置文件获取实际设置

    # 获取cookie里的一些参数，部分请求需要使用到————hss修改
    def get_cookie_data(self):
        try:
            app_param = re.findall("app_param=(.*?)}", self.HT_cookies)[0] + "}"
            app_param = json.loads(app_param)
            self.sa_device_id = app_param["sa_device_id"]
            self.brand = app_param["brand"]
            self.sa_distinct_id = re.findall(
                "sa_distinct_id=(.*?);", self.HT_cookies)[0]
            self.source_type = re.findall(
                "source_type=(.*?);", self.HT_cookies)[0]
            self.s_version = re.findall("s_version=(.*?);", self.HT_cookies)[0]
            self.s_channel = re.findall("s_channel=(.*?);", self.HT_cookies)[0]
        except Exception as e:
            print(
                "获取Cookie部分数据失败，将采用默认设置，请检查Cookie是否包含s_channel，s_version，source_type，sa_distinct_id\n",
                e
            )
            self.s_channel = "ios_oppostore"
            self.source_type = "505"

    # 获取个人信息，判断登录状态
    def get_user_info(self):
        flag = False
        url = "https://www.heytap.com/cn/oapi/users/web/member/info"
        headers = {
            'Host': 'www.heytap.com',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': self.HT_UserAgent,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'cookie': self.HT_cookies
        }
        response = self.session.get(url=url, headers=headers)
        response.encoding = "utf-8"
        try:
            result = response.json()
            if result["code"] == 200:
                self.log += f"======== {result['data']['realName']} ========\n"
                self.log += "【登录成功】：" + result["data"][
                    "realName"] + f"\n【抽奖开关】：{self.if_draw}\n"
                print("【登录成功】：" + result["data"]["realName"] +
                      f"\n【抽奖开关】：{self.if_draw}\n")
                flag = True
            else:
                self.log += "【登录失败】: " + result["errorMessage"] + "\n"
                print("【登录失败】: " + result["errorMessage"] + "\n")
        except Exception as e:
            print(traceback.format_exc())
            self.log += "【登录】: 发生错误，原因为: " + str(e) + "\n"
            print("【登录】: 发生错误，原因为: " + str(e) + "\n")

        if flag:
            self.get_cookie_data()
            return self.session
        else:
            return False

    # 任务中心列表，获取任务及任务状态
    def taskCenter(self):
        url = "https://store.oppo.com/cn/oapi/credits/web/credits/show"
        headers = {
            'Host': 'store.oppo.com',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': self.HT_UserAgent,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'cookie': self.HT_cookies,
            'referer': 'https://store.oppo.com/cn/app/taskCenter/index'
        }
        res1 = self.client.get(url=url, headers=headers)
        res1 = res1.json()
        return res1

    # 每日签到
    # 位置: APP → 我的 → 签到
    def daily_bonus(self):
        url = "https://store.oppo.com/cn/oapi/credits/web/report/immediately"
        try:
            dated = time.strftime("%Y-%m-%d")
            headers = {
                'Host': 'store.oppo.com',
                'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive',
                'User-Agent': self.HT_UserAgent,
                'Accept-Language': 'zh-cn',
                'Accept-Encoding': 'gzip, deflate, br',
                'cookie': self.HT_cookies,
                'referer': 'https://store.oppo.com/cn/app/taskCenter/index'
            }
            res = self.taskCenter()
            status = res["data"]["userReportInfoForm"]["status"]
            if status == 0:
                res = res["data"]["userReportInfoForm"]["gifts"]
                for data in res:
                    if data["date"] == dated:
                        qd = data
                        if not qd["today"]:
                            data = "amount=" + str(qd["credits"])
                            res1 = self.client.post(
                                url=url, data=data, headers=headers)
                            res1 = res1.json()
                            if res1["code"] == 200:
                                self.log += "【每日签到成功】: " + \
                                    res1["data"]["message"] + "\n"
                                print("【每日签到成功】: " +
                                      res1["data"]["message"] + "\n")
                            else:
                                self.log += "【每日签到失败】: " + res1 + "\n"
                                print("【每日签到失败】: " + res1 + "\n")
                        else:
                            # print(str(qd["credits"]),str(qd["type"]),str(qd["gift"]))
                            if not qd["type"]:
                                data = "amount=" + str(qd["credits"])
                            else:
                                data = "amount=" + str(qd['credits']) + \
                                       "&type=" + str(qd['type']) + \
                                       "&gift=" + str(qd['gift'])
                            res1 = self.client.post(
                                'https://store.oppo.com/cn/oapi/credits/web/report/immediately',
                                headers=headers,
                                data=data)
                            res1 = res1.json()
                            if res1["code"] == 200:
                                self.log += "【每日签到成功】: " + \
                                            res1["data"]["message"] + "\n"
                                print("【每日签到成功】: " +
                                      res1["data"]["message"] + "\n")
                            else:
                                self.log += "【每日签到失败】: " + str(res1) + "\n"
                                print("【每日签到失败】: " + str(res1) + "\n")
            else:
                self.log += "【每日签到】：已经签到过了！\n"
                print("【每日签到】：已经签到过了！\n")
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            self.log += "【每日签到】：错误，原因为: " + str(e) + "\n"
            print("【每日签到】：错误，原因为: " + str(e) + "\n")

    # 浏览商品 10个sku +20 分
    # 位置: APP → 我的 → 签到 → 每日任务 → 浏览商品
    def daily_viewgoods(self):
        try:
            headers = {
                'self.clientPackage': 'com.oppo.store',
                'Host': 'msec.opposhop.cn',
                'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive',
                'User-Agent': 'okhttp/3.12.12.200sp1',
                'Accept-Encoding': 'gzip',
                'cookie': self.HT_cookies
            }
            res = self.taskCenter()
            res = res["data"]["everydayList"]
            for data in res:
                if data["name"] == "浏览商品":
                    if data["completeStatus"] == 0:
                        # 原链接貌似获取不到商品id，更换一个 原链接https://msec.opposhop.cn/goods/v1/SeckillRound/goods/3016?pageSize=12&currentPage=1
                        shopList = self.client.get(
                            "https://msec.opposhop.cn/goods/v1/products/010239")
                        res = shopList.json()
                        if res["meta"]["code"] == 200:
                            i = 0
                            for skuinfo in res["details"][0]["infos"]:
                                skuid = skuinfo["skuId"]
                                print("正在浏览商品ID：", skuid)
                                self.client.get(
                                    "https://msec.opposhop.cn/goods/v1/info/sku?skuId=" +
                                    str(skuid),
                                    headers=headers
                                )
                                i += 1
                                if i > 10:
                                    break
                                time.sleep(5)
                            res2 = self.cashingCredits(
                                data["marking"], data["type"], data["credits"]
                            )
                            if res2:
                                self.log += "【每日浏览商品】：" + "任务完成！积分领取+" + \
                                            str(data["credits"]) + "\n"
                                print("【每日浏览商品】：" + "任务完成！积分领取+" +
                                      str(data["credits"]) + "\n")
                            else:
                                self.log += "【每日浏览商品】：" + "领取积分奖励出错！\n"
                                print("【每日浏览商品】：" + "领取积分奖励出错！\n")
                        else:
                            self.log += "【每日浏览商品】：错误，获取商品列表失败\n"
                            print("【每日浏览商品】：错误，获取商品列表失败\n")
                    elif data["completeStatus"] == 1:
                        res2 = self.cashingCredits(
                            data["marking"], data["type"], data["credits"]
                        )
                        if res2:
                            self.log += "【每日浏览商品】：" + "任务完成！积分领取+" + \
                                        str(data["credits"]) + "\n"
                            print("【每日浏览商品】：" + "任务完成！积分领取+" +
                                  str(data["credits"]) + "\n")
                        else:
                            self.log += "【每日浏览商品】：" + "领取积分奖励出错！\n"
                            print("【每日浏览商品】：" + "领取积分奖励出错！\n")
                    else:
                        self.log += "【每日浏览商品】：" + "任务已完成！\n"
                        print("【每日浏览商品】：" + "任务已完成！\n")
        except Exception as e:
            print(traceback.format_exc())
            self.log += "【每日浏览任务】: 错误，原因为: " + str(e) + "\n"
            print("【每日浏览任务】: 错误，原因为: " + str(e) + "\n")

    def daily_sharegoods(self):
        try:
            headers = {
                'self.clientPackage': 'com.oppo.store',
                'Host': 'msec.opposhop.cn',
                'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive',
                'User-Agent': 'okhttp/3.12.12.200sp1',
                'Accept-Encoding': 'gzip',
                'cookie': self.HT_cookies
            }
            daySignList = self.taskCenter()
            res = daySignList
            res = res["data"]["everydayList"]
            for data in res:
                if data["name"] == "分享商品到微信":
                    qd = data
            if qd["completeStatus"] == 0:
                count = qd["readCount"]
                endcount = qd["times"]
                while count <= endcount:
                    self.client.get(
                        "https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_sharegoods",
                        headers=headers)
                    count += 1
                res2 = self.cashingCredits(
                    qd["marking"], qd["type"], qd["credits"]
                )
                if res2:
                    self.log += "【每日分享商品】：" + "任务完成！积分领取+" + \
                                str(qd["credits"]) + "\n"
                    print("【每日分享商品】：" + "任务完成！积分领取+" +
                          str(qd["credits"]) + "\n")
                else:
                    self.log += "【每日分享商品】：" + "领取积分奖励出错！\n"
                    print("【每日分享商品】：" + "领取积分奖励出错！\n")
            elif qd["completeStatus"] == 1:
                res2 = self.cashingCredits(
                    qd["marking"], qd["type"], qd["credits"]
                )
                if res2:
                    self.log += "【每日分享商品】：" + "任务完成！积分领取+" + \
                                str(qd["credits"]) + "\n"
                    print("【每日分享商品】：" + "任务完成！积分领取+" +
                          str(qd["credits"]) + "\n")
                else:
                    self.log += "【每日分享商品】：" + "领取积分奖励出错！\n"
                    print("【每日分享商品】：" + "领取积分奖励出错！\n")
            else:
                self.log += "【每日分享商品】：" + "任务已完成！\n"
                print("【每日分享商品】：" + "任务已完成！\n")
        except Exception as e:
            print(traceback.format_exc())
            self.log += "【每日分享商品】：错误，原因为: " + str(e) + "\n"
            print("【每日分享商品】：错误，原因为: " + str(e) + "\n")

    def daily_viewpush(self):
        try:
            headers = {
                'self.clientPackage': 'com.oppo.store',
                'Host': 'msec.opposhop.cn',
                'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive',
                'User-Agent': 'okhttp/3.12.12.200sp1',
                'Accept-Encoding': 'gzip',
                'cookie': self.HT_cookies
            }
            daySignList = self.taskCenter()
            res = daySignList
            res = res["data"]["everydayList"]
            for data in res:
                if data["name"] == "点推送消息":
                    qd = data
            if qd["completeStatus"] == 0:
                count = qd["readCount"]
                endcount = qd["times"]
                while count <= endcount:
                    self.client.get(
                        "https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_viewpush",
                        headers=headers)
                    count += 1
                res2 = self.cashingCredits(
                    qd["marking"], qd["type"], qd["credits"]
                )
                if res2:
                    self.log += "【每日点推送】: " + "任务完成！积分领取+" + \
                                str(qd["credits"]) + "\n"
                    print("【每日点推送】: " + "任务完成！积分领取+" +
                          str(qd["credits"]) + "\n")
                else:
                    self.log += "【每日点推送】: " + "领取积分奖励出错！\n"
                    print("【每日点推送】: " + "领取积分奖励出错！\n")
            elif qd["completeStatus"] == 1:
                res2 = self.cashingCredits(
                    qd["marking"], qd["type"], qd["credits"]
                )
                if res2:
                    self.log += "【每日点推送】: " + "任务完成！积分领取+" + \
                                str(qd["credits"]) + "\n"
                    print("【每日点推送】: " + "任务完成！积分领取+" +
                          str(qd["credits"]) + "\n")
                else:
                    self.log += "【每日点推送】: " + "领取积分奖励出错！\n"
                    print("【每日点推送】: " + "领取积分奖励出错！\n")
            else:
                self.log += "【每日点推送】: " + "任务已完成！\n"
                print("【每日点推送】: " + "任务已完成！\n")
        except Exception as e:
            print(traceback.format_exc())
            self.log += "【每日推送消息】: 错误，原因为: " + str(e) + "\n"
            print("【每日推送消息】: 错误，原因为: " + str(e) + "\n")

    # 执行完成任务领取奖励
    def cashingCredits(self, info_marking, info_type, info_credits):
        headers = {
            "Host": "store.oppo.com",
            "self.clientPackage": "com.oppo.store",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": self.HT_UserAgent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
            "cookie": self.HT_cookies,
            "Origin": "https://store.oppo.com",
            "X-Requested-With": "com.oppo.store",
            "referer": "https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin"
        }
        data = "marking=" + str(info_marking) + \
            "&type=" + str(info_type) + \
            "&amount=" + str(info_credits)
        res = self.client.post(
            "https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits",
            data=data,
            headers=headers)
        res = res.json()
        if res["code"] == 200:
            return True
        else:
            return False

    # 活动平台抽奖通用接口
    def lottery(self, datas, referer="", extra_draw_cookie=""):
        headers = {
            "referer": referer,
            "User-Agent": self.HT_UserAgent,
            "cookie": extra_draw_cookie + self.HT_cookies,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://hd.oppo.com"
        }
        res = self.client.post(
            "https://hd.oppo.com/platform/lottery",
            data=datas,
            headers=headers)
        res = res.json()
        return res

    # 活动平台完成任务接口
    def task_finish(self, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Connection": "keep-alive",
            "User-Agent": self.HT_UserAgent,
            "Accept-Encoding": "gzip, deflate",
            "cookie": self.HT_cookies,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest"
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = self.client.post(
            "https://hd.oppo.com/task/finish",
            data=datas,
            headers=headers)
        res = res.json()
        return res

    # 活动平台领取任务奖励接口
    def task_award(self, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Connection": "keep-alive",
            "User-Agent": self.HT_UserAgent,
            "Accept-Encoding": "gzip, deflate",
            "cookie": self.HT_cookies,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest"
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = self.client.post(
            "https://hd.oppo.com/task/award",
            data=datas,
            headers=headers)
        res = res.json()
        return res

    # 做活动任务和抽奖通用接口————hss修改
    def doTask_and_draw(self):
        for act_list in self.act_task:
            act_name = act_list["act_name"]
            aid = act_list["aid"]
            referer = act_list["referer"]
            if_draw = act_list["if_draw"]
            if_task = act_list["if_task"]
            end_time = act_list["end_time"]
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Connection": "keep-alive",
                "User-Agent": self.HT_UserAgent,
                "Accept-Encoding": "gzip, deflate",
                "cookie": self.HT_cookies,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": referer
            }
            dated = int(time.time())
            end_time = time.mktime(time.strptime(
                end_time, "%Y-%m-%d %H:%M:%S"))  # 设置活动结束日期

            if dated < end_time:
                if if_task:
                    self.log += f"【{act_name}-任务】\n"
                    print(f"【{act_name}-任务】\n")
                    taskList = self.client.get(
                        f"https://hd.oppo.com/task/list?aid={aid}",
                        headers=headers)
                    taskList = taskList.json()
                    for i, jobs in enumerate(taskList["data"]):
                        title = jobs["title"]
                        t_index = jobs["t_index"]
                        aid = t_index[:t_index.index("i")]
                        if jobs["t_status"] == 0:
                            finishmsg = self.task_finish(aid, t_index)
                            if finishmsg["no"] == "200":
                                time.sleep(1)
                                awardmsg = self.task_award(aid, t_index)
                                msg = awardmsg["msg"]
                                self.log += f"{title}：{msg}\n"
                                print(f"{title}：{msg}\n")
                                time.sleep(3)
                        elif jobs["t_status"] == 1:
                            awardmsg = self.task_award(aid, t_index)
                            msg = awardmsg["msg"]
                            self.log += f"{title}：{msg}\n"
                            print(f"{title}：{msg}\n")
                            time.sleep(3)
                if self.if_draw:  # 判断当前用户是否抽奖
                    if if_draw:  # 判断当前活动是否抽奖
                        lid = act_list["lid"]
                        extra_draw_cookie = act_list["extra_draw_cookie"]
                        draw_times = act_list["draw_times"]
                        self.log += f"【{act_name}-抽奖】\n"
                        print(f"【{act_name}-抽奖】\n")
                        x = 0
                        while x < draw_times:
                            data = f"aid={aid}&lid={lid}&mobile=&authcode=&captcha=&isCheck=0&source_type={self.source_type}&s_channel={self.s_channel}&sku=&spu="
                            res = self.lottery(data, referer, extra_draw_cookie)
                            msg = res["msg"]
                            print(res)
                            if "次数已用完" in msg:
                                self.log += "  第" + str(x + 1) + "抽奖：抽奖次数已用完\n"
                                print("  第" + str(x + 1) + "抽奖：抽奖次数已用完\n")
                                break
                            goods_name = res["data"]["goods_name"]
                            if goods_name:
                                self.log += "  第" + str(x + 1) + "次抽奖：" + str(
                                    goods_name) + "\n"
                                print("  第" + str(x + 1) + "次抽奖：" +
                                      str(goods_name) + "\n")
                            elif "提交成功" in msg:
                                # tips_msg = res["data"]["tips_msg"]
                                self.log += "  第" + str(x + 1) + "次抽奖：未中奖\n"
                                print("  第" + str(x + 1) + "次抽奖：未中奖\n")
                            x += 1
                            time.sleep(5)
            else:
                self.log += f"【{act_name}】：活动已结束，不再执行\n"
                print(f"【{act_name}】：活动已结束，不再执行\n")

    # 暂时保留，aid和我抓取的不一致
    # realme宠粉计划-幸运抽奖-转盘
    def realme_lottery(self):
        data = "aid=1182&lid=1429&mobile=&authcode=&captcha=&isCheck=0&source_type=505&s_channel=ios_oppostore&sku=&spu="
        res = self.lottery(data)
        msg = res["msg"]
        print(res)
        if "次数已用完" in msg:
            self.log += "【realme宠粉计划转盘】获得：抽奖次数已用完\n"
            print("【realme宠粉计划转盘】获得：抽奖次数已用完\n")
        goods_name = res["data"]["goods_name"]
        self.log += "【realme宠粉计划转盘】获得：" + str(goods_name) + "\n"
        print("【realme宠粉计划转盘】获得：" + str(goods_name) + "\n")
        time.sleep(3)

    # 早睡打卡
    def zaoshui_task(self):
        try:
            headers = {
                "Host": "store.oppo.com",
                "Connection": "keep-alive",
                "s_channel": self.s_channel,
                "utm_term": "direct",
                "utm_campaign": "direct",
                "utm_source": "direct",
                "ut": "direct",
                "uc": "zaoshuidaka",
                "sa_device_id": self.sa_device_id,
                "guid": self.sa_device_id,
                "sa_distinct_id": self.sa_distinct_id,
                "clientPackage": "com.oppo.store",
                "Cache-Control": "no-cache",
                "um": "hudongleyuan",
                "User-Agent": self.HT_UserAgent,
                "ouid": "",
                "Accept": "application/json, text/plain, */*",
                "source_type": self.source_type,
                "utm_medium": "direct",
                "brand": "iPhone",
                "appId": "",
                "s_version": self.s_version,
                "us": "gerenzhongxin",
                "appKey": "",
                "X-Requested-With": "com.oppo.store",
                "Referer": "https://store.oppo.com/cn/app/cardingActivities?utm_source=opposhop&utm_medium=task",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cookie": self.HT_cookies
            }
            res = self.client.get(
                "https://store.oppo.com/cn/oapi/credits/web/clockin/applyOrClockIn",
                headers=headers).json()
            if "余额不足" in str(res):
                self.log += "【早睡打卡】\n申请失败，积分余额不足\n"
                print("【早睡打卡】\n申请失败，积分余额不足\n")
            else:
                applyStatus = res["data"]["applyStatus"]
                if applyStatus == 1:
                    self.log += "【早睡打卡】\n申请成功，请当天19:30-22:00手动打卡\n"
                    print("【早睡打卡】申请成功，请当天19:30-22:00手动打卡\n")
                if applyStatus == 0:
                    self.log += "【早睡打卡】\n申请失败，积分不足或报名时间已过\n"
                    print("【早睡打卡】申请失败，积分不足或报名时间已过\n")
                if applyStatus == 2:
                    self.log += "【早睡打卡】\n打卡成功，积分将于24:00前到账\n"
                    print("【早睡打卡】\n打卡成功，积分将于24:00前到账\n")
            # 打卡记录
            res = self.client.get(
                "https://store.oppo.com/cn/oapi/credits/web/clockin/getMyRecord",
                headers=headers).json()
            if res["code"] == 200:
                record = res["data"]["everydayRecordForms"]
                self.log += "【早睡打卡记录】\n"
                print("【早睡打卡记录】\n")
                i = 0
                for data in record:
                    self.log += data["everydayDate"] + "——" +\
                        data["applyClockInStatus"] + "——" +\
                        data["credits"] + "\n"
                    print(data["everydayDate"] + "——" +
                          data["applyClockInStatus"] + "——" +
                          data["credits"] + "\n")
                    i += 1
                    if i == 4:  # 最多显示最近2条记录
                        break
        except Exception as e:
            print(traceback.format_exc())
            self.log += "【早睡打卡】\n错误，原因为: " + str(e) + "\n"
            print("【早睡打卡】: 错误，原因为: " + str(e) + "\n")

    # 主程序
    def main(self):
        i = 1
        for config in self.login:
            self.HT_cookies = config["cookie"]
            self.HT_UserAgent = config["useragent"]
            self.if_draw = config["if_draw"]
            self.client = self.get_user_info()
            if self.client:
                try:
                    self.daily_bonus()  # 执行每日签到
                    self.daily_viewgoods()  # 执行每日商品浏览任务
                    self.daily_sharegoods()  # 执行每日商品分享任务
                    # self.daily_viewpush()  # 执行每日点推送任务（已下架）
                    self.doTask_and_draw()  # 自己修改的接口，针对活动任务及抽奖，新增及删除活动请修改self.act_task
                    self.zaoshui_task()  # 早睡报名
                except Exception as e:
                    self.log += f"账号{i}执行出错：{e}\n"
                    print(f"账号{i}执行出错：{e}\n")
            else:
                self.log += f"账号{i}已失效，请及时更新cookies\n"
                print(f"账号{i}已失效，请及时更新cookies\n")
            i += 1
            self.log += "\n\n"
        return self.log


def main_handler(event, context):
    # 读取 src 目录下 check.json 配置文件
    with open(os.path.join(os.path.dirname(__file__), "check.json"), "r", encoding="utf-8") as f:
        cf = json.loads(f.read())
    cf = get_data()
    res = Heytap(cf).main()
    print(res)
    notify.send("欢太商城", res)


if __name__ == "__main__":
    cf = get_data()
    res = Heytap(cf).main()
    print(res)
    send("欢太商城", res)
"""
# 云函数请将上方替换成下方代码，并将 py 改名为 index.py
if __name__ == "__main__":
    main_handler("", "")
"""
