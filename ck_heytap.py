# -*- coding: utf-8 -*-
"""
:author @yyzhou94
cron: 19 5,21 * * *
new Env('欢太商城');
"""

import json
import os
import re
import time

import requests

import utils_tmp

try:
    from notify_mtr import send
except ModuleNotFoundError:
    import notify_mtr_json

    send = notify_mtr_json.send
try:
    from utils import get_data
except ModuleNotFoundError:
    pass


class Heytap:
    def __init__(self, config):
        self.client = None
        self.session = requests.session()
        self.login = config["HEYTAP"]
        self.log = ""
        self.config = config
        self.cookies = "cookie"
        self.user_agent = "ua"
        self.s_channel = "oppostore"
        self.source_type = "505"  # 初始化设置为505，会从cookie获取实际数据
        self.sa_distinct_id = ""
        self.sa_device_id = ""
        self.s_version = ""
        self.brand = "iPhone"  # 初始化设置为iPhone，会从cookie获取实际机型
        self.act_task = utils_tmp.act_list  # 修改为从文件获取，避免更新代码后丢失原有活动配置
        self.if_draw = False  # 初始化设置为False，会从配置文件获取实际设置

        self.accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.accept_encoding1 = "gzip, deflate, br"
        self.accept_encoding2 = "gzip, deflate"
        self.client_package = "com.oppo.store"
        self.content_type1 = "application/x-www-form-urlencoded"
        self.content_type2 = "application/x-www-form-urlencoded;charset=UTF-8"
        self.host1 = "store.oppo.com"
        self.host2 = "msec.opposhop.cn"
        self.user_agent2 = "okhttp/3.12.12.200sp1"

        self.point_got = "任务完成！积分领取+"
        self.point_err = "领取积分奖励出错！\n"
        self.done_msg = "任务已完成\n"
        self.err_msg = "错误，原因为: "
        self.amount = "amount="

    # 获取cookie里的一些参数，部分请求需要使用到  hss修改
    def get_cookie_data(self):
        try:
            app_param = re.findall("app_param=(.*?)}", self.cookies)[0] + "}"
            app_param = json.loads(app_param)
            self.sa_device_id = app_param["sa_device_id"]
            self.brand = app_param["brand"]
            self.sa_distinct_id = re.findall("sa_distinct_id=(.*?);", self.cookies)[0]
            self.source_type = re.findall("source_type=(.*?);", self.cookies)[0]
            self.s_version = re.findall("s_version=(.*?);", self.cookies)[0]
            self.s_channel = re.findall("s_channel=(.*?);", self.cookies)[0]
        except Exception as e:
            print(
                "获取Cookie部分数据失败，将采用默认设置，请检查Cookie是否包含s_channel，s_version，source_type，sa_distinct_id\n",
                e,
            )
            self.s_channel = "ios_oppostore"
            self.source_type = "505"

    # 获取个人信息，判断登录状态
    def get_user_info(self):
        flag = False
        headers = {
            "Host": "www.heytap.com",
            "Accept": self.accept,
            "Content-Type": self.content_type1,
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": self.accept_encoding1,
            "cookie": self.cookies,
        }
        response = self.session.get(
            "https://www.heytap.com/cn/oapi/users/web/member/info", headers=headers
        )
        response.encoding = "utf-8"
        try:
            result = response.json()
            if result["code"] == 200:
                self.log += f'======== {result["data"]["realName"]} ========\n'
                self.log += (
                    "【登录成功】："
                    + result["data"]["realName"]
                    + f"\n【抽奖开关】：{self.if_draw}\n"
                )
                flag = True
            else:
                self.log += "【登录失败】：" + result["errorMessage"] + "\n"
        except Exception as e:
            self.log += "【登录】：错误，原因为: " + str(e) + "\n"

        if flag:
            self.get_cookie_data()
            return self.session
        else:
            return False

    # 任务中心列表，获取任务及任务状态
    def taskCenter(self):
        headers = {
            "Host": self.host1,
            "Accept": self.accept,
            "Content-Type": self.content_type1,
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": self.accept_encoding1,
            "cookie": self.cookies,
            "referer": "https://store.oppo.com/cn/app/taskCenter/index",
        }
        res1 = self.client.get(
            "https://store.oppo.com/cn/oapi/credits/web/credits/show", headers=headers
        )
        res1 = res1.json()
        return res1

    # 每日签到
    # 位置: APP → 我的 → 签到
    def daily_bonus(self):
        try:
            dated = time.strftime("%Y-%m-%d")
            headers = {
                "Host": self.host1,
                "Accept": self.accept,
                "Content-Type": self.content_type1,
                "Connection": "keep-alive",
                "User-Agent": self.user_agent,
                "Accept-Language": "zh-cn",
                "Accept-Encoding": self.accept_encoding1,
                "cookie": self.cookies,
                "referer": "https://store.oppo.com/cn/app/taskCenter/index",
            }
            res = self.taskCenter()
            status = res["data"]["userReportInfoForm"]["status"]
            if status == 0:
                res = res["data"]["userReportInfoForm"]["gifts"]
                for data in res:
                    if data["date"] == dated:
                        qd = data
                        if not qd["today"]:
                            data = self.amount + str(qd["credits"])
                            res1 = self.client.post(
                                "https://store.oppo.com/cn/oapi/credits/web/report/immediately",
                                headers=headers,
                                data=data,
                            )
                            res1 = res1.json()
                            if res1["code"] == 200:
                                self.log += "【每日签到成功】：" + res1["data"]["message"] + "\n"
                            else:
                                self.log += "【每日签到失败】：" + res1 + "\n"
                        else:
                            # print(str(qd["credits"]), str(qd["type"]), str(qd["gift"]))
                            if not qd["type"]:
                                data = self.amount + str(qd["credits"])
                            else:
                                data = (
                                    self.amount
                                    + str(qd["credits"])
                                    + "&type="
                                    + str(qd["type"])
                                    + "&gift="
                                    + str(qd["gift"])
                                )
                            res1 = self.client.post(
                                "https://store.oppo.com/cn/oapi/credits/web/report/immediately",
                                headers=headers,
                                data=data,
                            )
                            res1 = res1.json()
                            if res1["code"] == 200:
                                self.log += "【每日签到成功】：" + res1["data"]["message"] + "\n"
                            else:
                                self.log += "【每日签到失败】：" + str(res1) + "\n"
            else:
                self.log += "【每日签到】：已经签到过了！\n"
            time.sleep(1)
        except Exception as e:
            self.log += "【每日签到】：错误，原因为: " + str(e) + "\n"

    # 浏览商品 10个sku +20 分
    # 位置: APP → 我的 → 签到 → 每日任务 → 浏览商品
    def daily_viewgoods(self):
        self.log += "【每日浏览商品】\n"
        try:
            headers = {
                "clientPackage": self.client_package,
                "Host": self.host2,
                "Accept": self.accept,
                "Content-Type": self.content_type1,
                "Connection": "keep-alive",
                "User-Agent": self.user_agent2,
                "Accept-Encoding": "gzip",
                "cookie": self.cookies,
            }
            res = self.taskCenter()
            res = res["data"]["everydayList"]
            for data in res:
                if data["name"] == "浏览商品":
                    if data["completeStatus"] == 0:
                        # 原链接貌似获取不到商品id，更换一个 原链接https://msec.opposhop.cn/goods/v1/SeckillRound/goods/3016?pageSize=12&currentPage=1
                        shoplist = self.client.get(
                            "https://msec.opposhop.cn/goods/v1/products/010239"
                        )
                        res = shoplist.json()
                        if res["meta"]["code"] == 200:
                            i = 0
                            for skuinfo in res["details"][0]["infos"]:
                                skuid = skuinfo["skuId"]
                                self.client.get(
                                    "https://msec.opposhop.cn/goods/v1/info/sku?skuId="
                                    + str(skuid),
                                    headers=headers,
                                )
                                i += 1
                                if i > 10:
                                    break
                                time.sleep(5)
                            res2 = self.cashingCredits(
                                data["marking"], data["type"], data["credits"]
                            )
                            if res2:
                                self.log += self.point_got + str(data["credits"]) + "\n"
                            else:
                                self.log += self.point_err
                        else:
                            self.log += "错误，获取商品列表失败\n"
                    elif data["completeStatus"] == 1:
                        res2 = self.cashingCredits(
                            data["marking"], data["type"], data["credits"]
                        )
                        if res2:
                            self.log += self.point_got + str(data["credits"]) + "\n"
                        else:
                            self.log += self.point_err
                    else:
                        self.log += self.done_msg
        except Exception as e:
            self.log += self.err_msg + str(e) + "\n"

    def daily_sharegoods(self):
        self.log += "【每日分享商品】\n"
        try:
            headers = {
                "clientPackage": self.client_package,
                "Host": self.host2,
                "Accept": self.accept,
                "Content-Type": self.content_type1,
                "Connection": "keep-alive",
                "User-Agent": self.user_agent2,
                "Accept-Encoding": "gzip",
                "cookie": self.cookies,
            }
            daysignlist = self.taskCenter()
            res = daysignlist
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
                        headers=headers,
                    )
                    count += 1
                res2 = self.cashingCredits(qd["marking"], qd["type"], qd["credits"])
                if res2:
                    self.log += self.point_got + str(qd["credits"]) + "\n"
                else:
                    self.log += self.point_err
            elif qd["completeStatus"] == 1:
                res2 = self.cashingCredits(qd["marking"], qd["type"], qd["credits"])
                if res2:
                    self.log += self.point_got + str(qd["credits"]) + "\n"
                else:
                    self.log += self.point_err
            else:
                self.log += self.done_msg
        except Exception as e:
            self.log += self.err_msg + str(e) + "\n"

    def daily_viewpush(self):
        self.log += "【每日点推送】\n"
        try:
            headers = {
                "clientPackage": self.client_package,
                "Host": self.host2,
                "Accept": self.accept,
                "Content-Type": self.content_type1,
                "Connection": "keep-alive",
                "User-Agent": self.user_agent2,
                "Accept-Encoding": "gzip",
                "cookie": self.cookies,
            }
            daysignlist = self.taskCenter()
            res = daysignlist
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
                        headers=headers,
                    )
                    count += 1
                res2 = self.cashingCredits(qd["marking"], qd["type"], qd["credits"])
                if res2:
                    self.log += self.point_got + str(qd["credits"]) + "\n"
                else:
                    self.log += self.point_err
            elif qd["completeStatus"] == 1:
                res2 = self.cashingCredits(qd["marking"], qd["type"], qd["credits"])
                if res2:
                    self.log += self.point_got + str(qd["credits"]) + "\n"
                else:
                    self.log += self.point_err
            else:
                self.log += self.done_msg
        except Exception as e:
            self.log += self.err_msg + str(e) + "\n"

    # 执行完成任务领取奖励
    def cashingCredits(self, info_marking, info_type, info_credits):
        headers = {
            "Host": self.host1,
            "clientPackage": self.client_package,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": self.content_type1,
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": self.accept_encoding1,
            "cookie": self.cookies,
            "Origin": "https://store.oppo.com",
            "X-Requested-With": self.client_package,
            "referer": "https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin",
        }

        data = (
            "marking="
            + str(info_marking)
            + "&type="
            + str(info_type)
            + "&amount="
            + str(info_credits)
        )

        res = self.client.post(
            "https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits",
            data=data,
            headers=headers,
        )

        res = res.json()

        if res["code"] == 200:
            return True
        else:
            return False

    # 活动平台抽奖通用接口
    def lottery(self, datas, referer="", extra_draw_cookie=""):

        headers = {
            "Host": "hd.oppo.com",
            "User-Agent": self.user_agent,
            "Cookie": extra_draw_cookie + self.cookies,
            "Referer": referer,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "br, gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        res = self.client.get("https://hd.oppo.com/user/login", headers=headers).json()
        if res["no"] == "200":
            res = self.client.post(
                "https://hd.oppo.com/platform/lottery", data=datas, headers=headers
            )
            res = res.json()
            return res
        else:
            return res

    # 活动平台完成任务接口
    def task_finish(self, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": self.content_type2,
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "Accept-Encoding": self.accept_encoding2,
            "cookie": self.cookies,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest",
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = self.client.post(
            "https://hd.oppo.com/task/finish", data=datas, headers=headers
        )
        res = res.json()
        return res

    # 活动平台领取任务奖励接口
    def task_award(self, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": self.content_type2,
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "Accept-Encoding": self.accept_encoding2,
            "cookie": self.cookies,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest",
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = self.client.post(
            "https://hd.oppo.com/task/award", data=datas, headers=headers
        )
        res = res.json()
        return res

    # 做活动任务和抽奖通用接口  hss修改
    def do_task_and_draw(self):
        try:

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
                    "User-Agent": self.user_agent,
                    "Accept-Encoding": self.accept_encoding2,
                    "cookie": self.cookies,
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": referer,
                }
                dated = int(time.time())
                end_time = time.mktime(
                    time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                )  # 设置活动结束日期

                if dated < end_time and if_task:
                    res = self.client.get(
                        f"https://hd.oppo.com/task/list?aid={aid}", headers=headers
                    )
                    tasklist = res.json()
                    self.log += f"【{act_name}-任务】\n"
                    for i, jobs in enumerate(tasklist["data"]):
                        title = jobs["title"]
                        t_index = jobs["t_index"]
                        aid = t_index[: t_index.index("i")]
                        if jobs["t_status"] == 0:
                            finishmsg = self.task_finish(aid, t_index)
                            if finishmsg["no"] == "200":
                                time.sleep(1)
                                awardmsg = self.task_award(aid, t_index)
                                msg = awardmsg["msg"]
                                self.log += f"{title}：{msg}\n"
                                time.sleep(3)
                        elif jobs["t_status"] == 1:
                            awardmsg = self.task_award(aid, t_index)
                            msg = awardmsg["msg"]
                            self.log += f"{title}：{msg}\n"
                            time.sleep(3)
                        else:
                            self.log += f"{title}：任务已完成\n"
                if self.if_draw and if_draw:  # 判断当前用户是否抽奖 和 判断当前活动是否抽奖
                    lid = act_list["lid"]
                    extra_draw_cookie = act_list["extra_draw_cookie"]
                    draw_times = act_list["draw_times"]
                    self.log += f"【{act_name}-抽奖】："
                    x = 0
                    while x < draw_times:
                        data = f"aid={aid}&lid={lid}&mobile=&authcode=&captcha=&isCheck=0&source_type={self.source_type}&s_channel={self.s_channel}&sku=&spu="
                        res = self.lottery(data, referer, extra_draw_cookie)
                        msg = res["msg"]
                        if "次数已用完" in msg:
                            self.log += "  第" + str(x + 1) + "抽奖：抽奖次数已用完\n"
                            break
                        if "活动已结束" in msg:
                            self.log += "  第" + str(x + 1) + "抽奖：活动已结束，终止抽奖\n"
                            break
                        goods_name = res["data"]["goods_name"]
                        if goods_name:
                            self.log += (
                                "  第" + str(x + 1) + "次抽奖：" + str(goods_name) + "\n"
                            )
                        elif "提交成功" in msg:
                            self.log += "  第" + str(x + 1) + "次抽奖：未中奖\n"
                        x += 1
                        time.sleep(5)
                else:
                    self.log += f"【{act_name}】：活动已结束，不再执行\n"
        except Exception as e:
            self.log += "【执行任务和抽奖】：错误，原因为: " + str(e) + "\n"

    # 早睡打卡
    def zaoshui_task(self):
        try:
            headers = {
                "Host": self.host1,
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
                "clientPackage": self.client_package,
                "Cache-Control": "no-cache",
                "um": "hudongleyuan",
                "User-Agent": self.user_agent,
                "ouid": "",
                "Accept": "application/json, text/plain, */*",
                "source_type": self.source_type,
                "utm_medium": "direct",
                "brand": "iPhone",
                "appId": "",
                "s_version": self.s_version,
                "us": "gerenzhongxin",
                "appKey": "",
                "X-Requested-With": self.client_package,
                "Referer": "https://store.oppo.com/cn/app/cardingActivities?utm_source=opposhop&utm_medium=task",
                "Accept-Encoding": self.accept_encoding2,
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cookie": self.cookies,
            }
            res = self.client.get(
                "https://store.oppo.com/cn/oapi/credits/web/clockin/applyOrClockIn",
                headers=headers,
            ).json()
            if "余额不足" in str(res):
                self.log += "【早睡打卡】：申请失败，积分余额不足\n"
            else:
                applyStatus = res["data"]["applyStatus"]
                # 2 19:30打卡成功 0 8：00打卡成功
                if applyStatus == 1:
                    self.log += "【早睡打卡】：报名成功，请当天19:30-22:00留意打卡状态\n"
                if applyStatus == 0:
                    self.log += "【早睡打卡】：申请失败，积分不足或报名时间已过\n"
                if applyStatus == 2:
                    self.log += "【早睡打卡】：已报名成功，请当天19:30-22:00留意打卡状态\n"
                if res["data"]["clockInStatus"] == 1:
                    self.log += "【早睡打卡】：打卡成功，积分将于24:00前到账\n"
                if res["data"]["clockInStatus"] == 2:
                    self.log += "【早睡打卡】：打卡成功，积分将于24:00前到账\n"
            # 打卡记录
            res = self.client.get(
                "https://store.oppo.com/cn/oapi/credits/web/clockin/getMyRecord",
                headers=headers,
            ).json()
            if res["code"] == 200:
                record = res["data"]["everydayRecordForms"]
                self.log += "【早睡打卡记录】\n"
                i = 0
                for data in record:
                    self.log += (
                        data["everydayDate"]
                        + "-"
                        + data["applyClockInStatus"]
                        + "："
                        + data["credits"]
                        + "\n"
                    )
                    i += 1
                    if i == 4:  # 最多显示最近4条记录
                        break

        except Exception as e:
            self.log += "【早睡打卡】：错误，原因为: " + str(e) + "\n"

    # 集卡活动 活动已结束
    def collect_cards(self):
        try:
            # 初始化活动
            headers = {
                "Referer": "https://store.oppo.com/cn/app/collectCard/index?activityId=JP6BEV78&us=shouye&um=chaping&uc=all",
                "User-Agent": self.user_agent,
                "cookie": self.cookies,
                "Content-Type": self.content_type2,
            }

            # 助力
            mid = [
                "bce3e0ae99e39c7b17db589857e36f01",
                "2d92651041497960f85880c699a5674b",
                "8675bdfa84f88f6efee026af8db2cba5",
                "766d3d50f9d256b11728f09ef241accc",
            ]
            self.log += f"【集卡-助力】："
            for mid in mid:
                url = f"https://msec.opposhop.cn/credits/web/ccv2/shareActivity?activityId=JP6BEV78&mid={mid}"
                res = requests.get(url, headers=headers).json()
                if res["code"] == 200 and res["data"] == True:
                    self.log += f"助力{mid}：成功\n"
                else:
                    self.log += f"助力{mid}：失败\n"
                time.sleep(3)

            # 获取任务列表 #抽奖
            url = "https://store.oppo.com/cn/oapi/credits/web/ccv2/getLottery"
            data = "activityId=JP6BEV78"
            res = requests.post(url, data=data, headers=headers).json()
            self.log += f"【集卡-做任务】："
            if res["code"] == 200:
                tasklist = res["data"]
                for task in tasklist:
                    taskId = task["taskId"]
                    status = task["status"]
                    name = task["name"]
                    # 0 未完成 2 已完成
                    if status == 0:
                        if taskId == "daily_share_collectCard":
                            self.log += f'{name}：助力码为{task["mid"]}\n'
                            continue
                        if taskId == "once_buy_parts":
                            self.log += f"{name}：不花钱也想做任务？\n"
                            continue
                        if taskId == "once_buy_phone":
                            self.log += f"{name}：不花钱也想做任务？\n"
                            continue
                        if taskId == "once_join_pinggo":
                            self.log += f"{name}：不花钱也想做任务？\n"
                            continue
                        if taskId == "daily_send_friend":
                            self.log += f"{name}：请手动完成送卡\n"
                            continue

                        url = f"https://store.oppo.com/cn/oapi/credits/web/ccv2/ReportedTask?activityId=JP6BEV78&taskType={taskId}"
                        res = requests.get(url, headers=headers).json()
                        if res["code"] == 200 and res["data"]:
                            self.log += f"{name}：做任务成功\n"
                        else:
                            self.log += f"{name}：做任务失败\n"
                        time.sleep(5)
                    elif status == 2:
                        self.log += f"{name}：任务已完成\n"

                # 获取抽卡次数
                url = "https://store.oppo.com/cn/oapi/credits/web/ccv2/playerPage?activityId=JP6BEV78"
                res = requests.get(url, headers=headers).json()
                if res["code"] == 200:
                    self.log += f"【集卡-抽卡】："
                    chanceCount = res["data"]["chanceCount"]
                    for i in range(int(chanceCount)):
                        # 抽卡
                        url = "https://store.oppo.com/cn/oapi/credits/web/ccv2/collect"
                        data = "activityId=JP6BEV78"
                        res = requests.post(url, data=data, headers=headers).json()
                        if res["code"] == 200:
                            self.log += f'第{i + 1}次抽奖：{res["data"]["collectCard"]["cardName"]}\n'
                            time.sleep(5)
                # 翻牌
                url = "https://store.oppo.com/cn/oapi/credits/web/ccv2/playerPage?activityId=JP6BEV78"
                res = requests.get(url, headers=headers).json()
                if res["code"] == 200:
                    self.log += f"【集卡-翻牌抽奖】："
                    collectCardPlayerInfoList = res["data"]["collectCardPlayerInfoList"]
                    for cardlist in collectCardPlayerInfoList:
                        cardName = cardlist["cardName"]
                        num = cardlist["num"]
                        self.log += f"{cardName}：{num}张\n"
                        if int(num) > 0:

                            for userCard in cardlist["userCardList"]:
                                if userCard["giftId"] != None:
                                    self.log += f'{cardName}-卡片代码{userCard["cardCode"]}-卡片已抽过-{userCard["giftDesc"]}\n'
                                else:
                                    url = "https://store.oppo.com/cn/oapi/credits/web/ccv2/backGifts"
                                    data = f'cardCode={userCard["cardCode"]}&activityId=JP6BEV78'
                                    res = requests.post(
                                        url, data=data, headers=headers
                                    ).json()
                                    if res["code"] == 200:
                                        self.log += f'{cardName}-卡片代码{userCard["cardCode"]}-{res["data"]["giftDesc"]}\n'
                                    time.sleep(5)

        except Exception as e:
            self.log += "【集卡】：错误，原因为: " + str(e) + "\n"

    # 主程序
    def main(self):
        i = 1
        for config in self.login:
            self.cookies = config["cookie"]
            self.user_agent = config["useragent"]
            self.if_draw = config["draw"]
            self.client = self.get_user_info()
            if self.client:
                try:
                    self.daily_bonus()  # 执行每日签到
                    self.daily_viewgoods()  # 执行每日商品浏览任务
                    self.daily_sharegoods()  # 执行每日商品分享任务
                    # self.daily_viewpush()  # 执行每日点推送任务  任务下线
                    self.do_task_and_draw()  # 自己修改的接口，针对活动任务及抽奖，新增及删除活动请修改act_list.py
                    self.zaoshui_task()  # 早睡报名 由于自己不能及时更新cookie，就关闭了打卡
                    # self.collect_cards()  # 集卡活动  #活动结束，奖励都不太好，新一期不再更新
                except Exception as e:
                    self.log += f"账号{i}执行出错：{e}\n"
            else:
                self.log += f"账号{i}已失效，请及时更新cookies\n"
            i += 1
            self.log += "\n\n"
        return self.log


# 腾讯云函数入口
def main_handler(event, context):
    try:
        cf = get_data()
    except Exception:
        # 读取 src 目录下 check.json 配置文件
        with open(
            os.path.join(os.path.dirname(__file__), "check.json"), "r", encoding="utf-8"
        ) as f:
            cf = json.loads(f.read())
    res = Heytap(cf).main()
    send("欢太商城", res)


# 主函数入口
if __name__ == "__main__":
    main_handler("", "")
