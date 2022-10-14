# -*- coding: utf-8 -*-
"""
cron: 30 8 * * *
new Env('Bilibili');
"""

import time

import requests

from notify_mtr import send
from utils import get_data


class BiliBili:
    def __init__(self, check_items: list):
        self.check_items = check_items

    @staticmethod
    def get_nav(session: requests.Session) -> tuple:
        """GET 登录基本信息-导航栏用户信息

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/login/login_info.md

        :param requests.Session session:
        :return (str, int, int, bool, int, int):
        (用户昵称, 用户 mid, 登录状态, 硬币数, 会员类型, 当前经验)
        """
        url = "https://api.bilibili.com/x/web-interface/nav"
        data = session.get(url=url).json().get("data", {})
        uname = data.get("uname")
        uid = data.get("mid")
        is_login = data.get("isLogin")
        coin = data.get("money")
        vip_type = data.get("vipType")
        current_exp = data.get("level_info", {}).get("current_exp")
        return uname, uid, is_login, coin, vip_type, current_exp

    @staticmethod
    def get_today_exp(session: requests.Session) -> list:
        """GET 获取今日经验信息

        :param requests.Session session:
        :return list: 今日经验信息列表
        """
        url = "https://api.bilibili.com/x/member/web/exp/log?jsonp=jsonp"
        today = time.strftime("%Y-%m-%d", time.localtime())
        return list(
            filter(
                lambda x: x["time"].split()[0] == today,
                session.get(url=url).json().get("data").get("list"),
            )
        )

    @staticmethod
    def sign_live(session: requests.Session) -> str:
        """GET 直播间用户实用 API-直播签到

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/live/user.md

        :param requests.Session session:
        :return str: 直播签到结果，成功/已签/失败/异常
        """
        try:
            url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
            res = session.get(url=url).json()
            if res["code"] == 0:
                msg = (
                    f'签到成功，{res["data"]["text"]}，'
                    f'特别信息：{res["data"]["specialText"]}，'
                    f'本月已签到 {res["data"]["hadSignDays"]} 天'
                )
            elif res["code"] == 1011040:
                msg = "今日已签到过，无法重复签到"
            else:
                msg = f'签到失败，信息为：{res["message"]}'
        except Exception as e:
            msg = f"签到异常，原因为 {str(e)}"
            print(msg)
        return msg

    @staticmethod
    def clockin_manga(session: requests.Session, platform: str = "android") -> str:
        """POST 模拟漫画客户端签到

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/manga/ClockIn.md

        :param requests.Session session:
        :param str platform: 签到平台, defaults to "android"
        :return str: 漫画客户端签到结果，成功/已签/失败/异常
        """
        try:
            url = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
            post_data = {"platform": platform}
            res = session.post(url=url, data=post_data).json()
            if res["code"] == 0:
                msg = "签到成功"
            elif res["msg"] == "clockin clockin is duplicate":
                msg = "今天已经签到过了"
            else:
                msg = f'签到失败，信息为 {res["msg"]}'
                print(msg)
        except Exception as e:
            msg = f"签到异常，原因为：{str(e)}"
            print(msg)
        return msg

    @staticmethod
    def receive_vip_privilege(
        session: requests.Session, bili_jct: str, receive_type: int = 1
    ) -> dict:
        """POST 大会员兑换福利-兑换卡券

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/user/vip.md

        :param requests.Session session:
        :param str bili_jct: Cookie bili_jct 字段
        :param int receive_type: 1~5: B币券 会员购优惠券 漫画福利券 会员购包邮券 漫画商城优惠券, defaults to 1
        :return dict: {"code": 0, "message": "0", "ttl": 1}
        """
        url = "https://api.bilibili.com/x/vip/privilege/receive"
        post_data = {"type": receive_type, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def get_manga_vip_reward(session: requests.Session) -> dict:
        """POST 获取漫画大会员福利

        :param requests.Session session:
        :return dict: json 回复
        """
        url = "https://manga.bilibili.com/twirp/user.v1.User/GetVipReward"
        return session.post(url=url, json={"reason_id": 1}).json()

    @staticmethod
    def report_video_history(
        session: requests.Session,
        bili_jct: str,
        aid: int,
        cid: int,
        progress: int = 300,
    ) -> dict:
        """POST 视频观看数据上报-上报观看进度（双端）

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/video/report.md

        :param requests.Session session:
        :param str bili_jct: Cookie bili_jct 字段
        :param int aid: 稿件 avid
        :param int cid: 视频 cid
        :param int progress: 观看进度(s), defaults to 300
        :return dict: {"code": 0, "message": "0", "ttl": 1}
        """
        url = "http://api.bilibili.com/x/v2/history/report"
        post_data = {"aid": aid, "cid": cid, "progress": progress, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def share(session: requests.Session, bili_jct: str, aid: int) -> dict:
        """POST 分享指定 av 号视频（web 端）

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/video/like_coin_fav.md

        :param requests.Session session:
        :param str bili_jct: Cookie bili_jct 字段
        :param int aid: 稿件 avid
        :return dict: {"code": 0, "message": "0", "ttl": 1, "data":19}
        """
        url = "https://api.bilibili.com/x/web-interface/share/add"
        post_data = {"aid": aid, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def get_followings(
        session: requests.Session,
        uid: int,
        pn: int = 1,
        ps: int = 50,
        order: str = "desc",
        order_type: str = "attention",
    ) -> dict:
        """GET 用户关系相关-查询用户关注明细

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/user/relation.md

        :param requests.Session session:
        :param int uid: 目标用户 mid
        :param int pn: 页码, defaults to 1
        :param int ps: 每页项数, defaults to 50
        :param str order: defaults to "desc"
        :param str order_type: 排序方式, 按照关注顺序排列: 留空 按照最常访问排列: attention, defaults to "attention"
        :return dict: {"code": 0, "message": "0", "ttl": 1, "data": {"list": [], re_version: 3228575555, "total": 699}}
        """
        params: dict = {
            "vmid": uid,
            "pn": pn,
            "ps": ps,
            "order": order,
            "order_type": order_type,
        }
        url = "https://api.bilibili.com/x/relation/followings"
        return session.get(url=url, params=params).json()

    @staticmethod
    def search_space_arc(
        session: requests.Session,
        uid: int,
        pn: int = 1,
        ps: int = 100,
        tid: int = 0,
        order: str = "pubdate",
        keyword: str = "",
    ) -> list:
        """GET 获取指定 up 主空间视频投稿信息

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/user/space.md

        :param requests.Session session:
        :param int uid: 目标用户 mid
        :param int pn: 页码, defaults to 1
        :param int ps: 每页项数, defaults to 100
        :param int tid: 筛选目标分区, 0-不进行分区筛选, defaults to 0
        :param str order: 排序方式, 最新发布-pubdate, 最多播放-click, 最多收藏-stow, defaults to "pubdate"
        :param str keyword: 关键词筛选, 用于使用关键词搜索该 UP 主视频稿件, defaults to ""
        :return list: [{"aid": 585275804, "cid": 0, "title": "*", "owner": "apple"}, ...]
        """
        params: dict = {
            "mid": uid,
            "pn": pn,
            "ps": ps,
            "tid": tid,
            "order": order,
            "keyword": keyword,
        }
        url = "https://api.bilibili.com/x/space/arc/search"
        res = session.get(url=url, params=params).json()
        return [
            {
                "aid": one.get("aid"),
                "cid": 0,
                "title": one.get("title"),
                "owner": one.get("author"),
            }
            for one in res.get("data", {}).get("list", {}).get("vlist", [])
        ]

    @staticmethod
    def pay_elec_new(
        session: requests.Session, bili_jct: str, uid: int, num: int = 50
    ) -> dict:
        """POST B 币方式充电-新版本 B 币充电

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/electric/Bcoin.md

        :param requests.Session session:
        :param str bili_jct: Cookie bili_jct 字段
        :param int uid: 充电对象用户 mid
        :param int num: 贝壳数量, 必须在 2-9999 之间, defaults to 50
        :return dict: {"code": 0,"message": "0", "ttl": 1, "data":{...}}
        """
        url = "https://api.bilibili.com/x/ugcpay/trade/elec/pay/quick"
        post_data = {
            "bp_num": num,
            "is_bp_remains_prior": True,  # 是否优先扣除 B 币余额, B 币充电 true
            "up_mid": uid,
            "otype": "up",  # 充电来源, up-空间充电 archive-视频充电
            "oid": uid,
            "csrf": bili_jct,
        }
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def add_coin(
        session: requests.Session,
        bili_jct: str,
        aid: int,
        num: int = 1,
        select_like: int = 1,
    ) -> dict:
        """POST 给指定 av 号视频投币

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/article/like_coin_fav.md

        :param requests.Session session:
        :param str bili_jct: Cookie bili_jct 字段
        :param int aid: 稿件 avid
        :param int num: 投币数量, 上限为 2, defaults to 1
        :param int select_like: 是否附加点赞, 0-不点赞 1-同时点赞, defaults to 1
        :return dict: {"code": 0, "message": "0", "ttl": 1, "data": {"like": true}}
        """
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        post_data = {
            "aid": aid,
            "multiply": num,
            "select_like": select_like,
            "cross_domain": "true",
            "csrf": bili_jct,
        }
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def get_live_status(session: requests.Session) -> str:
        """GET 直播获取金银瓜子硬币数量

        :param requests.Session session:
        :return str: "银瓜子数量 金瓜子数量 硬币数量"
        """
        url = "https://api.live.bilibili.com/pay/v1/Exchange/getStatus"
        res = session.get(url=url).json()
        data = res.get("data")
        silver = data.get("silver", 0)
        gold = data.get("gold", 0)
        coin = data.get("coin", 0)
        return f"银瓜子数量: {silver}\n金瓜子数量: {gold}\n硬币数量: {coin}"

    @staticmethod
    def silver2coin(session: requests.Session, bili_jct: str) -> dict:
        """POST 银瓜子兑换硬币

        :param requests.Session session:
        :param str bili_jct: Cookie bili_jct 字段
        :return dict: json 返回
        """
        url = "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin"
        post_data = {"csrf_token": bili_jct, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def get_dynamic_videos(
        session: requests.Session, rid: int = 1, ps: int = 6
    ) -> list:
        """GET 分区最新视频-获取分区最新视频列表

        https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/ranking&dynamic/dynamic.md

        :param requests.Session session:
        :param int rid: 目标分区 tid, defaults to 1
        :param int ps: 每页项数, defaults to 6
        :return list: [{"aid": 56998612, "cid": 99548502, "title": "abc", "owner": "abc"}, ...]
        """
        url = (
            f"https://api.bilibili.com/x/web-interface/dynamic/region?ps={ps}&rid={rid}"
        )
        res = session.get(url=url).json()
        return [
            {
                "aid": one.get("aid"),
                "cid": one.get("cid"),
                "title": one.get("title"),
                "owner": one.get("owner", {}).get("name"),
            }
            for one in res.get("data", {}).get("archives", [])
        ]

    def main(self) -> str:
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }

            # csrf_token
            bili_jct = cookie.get("bili_jct", "")
            if not bili_jct:
                msg_all += "未获取到 bili_jct, 请检查 cookie 是否有效"
                continue
            # Config
            expected_coin = check_item.get("coin_num", 0)
            coin_type = check_item.get("coin_type", 1)
            silver2coin = check_item.get("silver2coin", True)

            # generate session
            session = requests.session()
            session.cookies.update(cookie)
            session.headers.update(
                {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64",
                    "Referer": "https://www.bilibili.com/",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "Connection": "keep-alive",
                }
            )

            # GET 导航栏用户信息 1/2
            uname, uid, is_login, coin, _, _ = self.get_nav(session=session)
            if not is_login:
                msg_all += "非登录状态，请检查\n\n"
                continue

            # POST 模拟漫画客户端签到
            manga_msg = self.clockin_manga(session=session)
            # GET 直播签到
            live_msg = self.sign_live(session=session)

            # GET 获取分区最新视频列表
            aid_list = self.get_dynamic_videos(session=session)

            # 今日已投币数量信息
            coins_av_count = len(
                list(
                    filter(
                        lambda x: x["reason"] == "视频投币奖励",
                        self.get_today_exp(session=session),
                    )
                )
            )
            coin_num = min(expected_coin - coins_av_count, coin)
            if coin_type == 1:
                following_list = self.get_followings(session=session, uid=uid)
                for following in following_list.get("data", {}).get("list", []):
                    mid = following.get("mid")
                    if mid:
                        aid_list += self.search_space_arc(session=session, uid=mid)

            if coin_num > 0:
                success_count = 0
                for aid in aid_list[::-1]:
                    res = self.add_coin(
                        session=session, aid=aid.get("aid"), bili_jct=bili_jct
                    )
                    if res["code"] == 0:
                        coin_num -= 1
                        print(f'成功给 {aid.get("title")} 投一个币')
                        success_count += 1
                    # -104 硬币不够了 -111 csrf 失败 34005 投币达到上限
                    elif res["code"] == 34005:
                        print(f'投币 {aid.get("title")} 失败，原因为 {res["message"]}')
                        continue
                    else:
                        print(f'投币 {aid.get("title")} 失败，原因为 {res["message"]}，跳过投币')
                        break
                    if coin_num <= 0:
                        break
                coin_msg = f"今日成功投币 {success_count + coins_av_count}/{expected_coin} 个"
            else:
                coin_msg = f"今日成功投币 {coins_av_count}/{expected_coin} 个"

            # POST 上报观看进度（双端）
            aid = aid_list[0].get("aid")
            cid = aid_list[0].get("cid")
            title = aid_list[0].get("title")
            report_res = self.report_video_history(
                session=session, bili_jct=bili_jct, aid=aid, cid=cid
            )
            if report_res.get("code") == 0:
                report_msg = f"观看《{title}》 300 秒"
            else:
                report_msg = "任务失败"
                print(report_msg)

            # POST 分享指定 av 号视频（web 端）
            share_res = self.share(session=session, bili_jct=bili_jct, aid=aid)
            if share_res.get("code") == 0:
                share_msg = f"分享《{title}》成功"
            else:
                share_msg = "分享失败"
                print(share_msg)

            # POST 银瓜子兑换硬币
            if silver2coin:
                silver2coin_res = self.silver2coin(session=session, bili_jct=bili_jct)
                if silver2coin_res["code"] == 0:
                    silver2coin_msg = "成功将银瓜子兑换为 1 个硬币"
                else:
                    silver2coin_msg = silver2coin_res["message"]
            else:
                silver2coin_msg = "未开启银瓜子兑换硬币功能"

            # GET 直播获取金银瓜子硬币数量
            live_stats = self.get_live_status(session=session)

            # GET 导航栏用户信息 2/2
            uname, uid, is_login, _, _, new_current_exp = self.get_nav(session=session)

            # 今日获得经验
            today_exp = sum(
                map(lambda x: x["delta"], self.get_today_exp(session=session))
            )
            # 预测升级天数
            update_data = (28800 - new_current_exp) // (today_exp or 1)

            msg = (
                f"帐号信息: {uname}\n"
                f"漫画签到: {manga_msg}\n"
                f"直播签到: {live_msg}\n"
                f"观看视频: {report_msg}\n"
                f"分享任务: {share_msg}\n"
                f"投币任务: {coin_msg}\n"
                f"银瓜子兑换硬币: {silver2coin_msg}\n"
                f"今日获得经验: {today_exp}\n"
                f"当前经验: {new_current_exp}\n"
                f"按当前速度升级还需: {update_data} 天\n"
                f"{live_stats}"
            )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("BILIBILI", [])
    result = BiliBili(check_items=_check_items).main()
    send("Bilibili", result)
