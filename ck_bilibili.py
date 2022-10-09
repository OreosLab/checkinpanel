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
    def __init__(self, check_items: dict):
        self.check_items = check_items

    @staticmethod
    def get_nav(session: requests.Session) -> tuple:
        url = "https://api.bilibili.com/x/web-interface/nav"
        _data = session.get(url=url).json().get("data", {})
        uname = _data.get("uname")
        uid = _data.get("mid")
        is_login = _data.get("isLogin")
        coin = _data.get("money")
        vip_type = _data.get("vipType")
        current_exp = _data.get("level_info", {}).get("current_exp")
        return uname, uid, is_login, coin, vip_type, current_exp

    @staticmethod
    def reward(session: requests.Session) -> list:
        """取 B站经验信息"""
        url = "https://api.bilibili.com/x/member/web/exp/log?jsonp=jsonp"
        today = time.strftime("%Y-%m-%d", time.localtime())
        return list(
            filter(
                lambda x: x["time"].split()[0] == today,
                session.get(url=url).json().get("data").get("list"),
            )
        )

    @staticmethod
    def live_sign(session: requests.Session) -> str:
        """B站直播签到"""
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
    def manga_sign(session: requests.Session, platform: str = "android") -> str:
        """模拟 B站漫画客户端签到"""
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
    def vip_privilege_receive(
        session: requests.Session, bili_jct: str, receive_type: int = 1
    ) -> dict:
        """领取 B站大会员权益
        receive_type int 权益类型，1 为 B币劵，2 为优惠券
        """
        url = "https://api.bilibili.com/x/vip/privilege/receive"
        post_data = {"type": receive_type, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def vip_manga_reward(session: requests.Session) -> dict:
        """获取漫画大会员福利"""
        url = "https://manga.bilibili.com/twirp/user.v1.User/GetVipReward"
        return session.post(url=url, json={"reason_id": 1}).json()

    @staticmethod
    def report_task(
        session: requests.Session, bili_jct: str, aid: int, cid: int, progres: int = 300
    ) -> dict:
        """B站上报视频观看进度
        aid int 视频 av 号
        cid int 视频 cid 号
        progres int 观看秒数
        """
        url = "http://api.bilibili.com/x/v2/history/report"
        post_data = {"aid": aid, "cid": cid, "progres": progres, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def share_task(session: requests.Session, bili_jct: str, aid: int) -> dict:
        """分享指定 av 号视频
        aid int 视频 av 号
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
        """获取指定用户关注的 up 主
        uid int 账户 uid，默认为本账户，非登录账户只能获取 20 个 * 5 页
        pn int 页码，默认第一页
        ps int 每页数量，默认 50
        order str 排序方式，默认 desc
        order_type 排序类型，默认 attention
        """
        params = {
            "vmid": uid,
            "pn": pn,
            "ps": ps,
            "order": order,
            "order_type": order_type,
        }
        url = "https://api.bilibili.com/x/relation/followings"
        return session.get(url=url, params=params).json()

    @staticmethod
    def space_arc_search(
        session: requests.Session,
        uid: int,
        pn: int = 1,
        ps: int = 100,
        tid: int = 0,
        order: str = "pubdate",
        keyword: str = "",
    ):
        """获取指定 up 主空间视频投稿信息
        uid int 账户 uid，默认为本账户
        pn int 页码，默认第一页
        ps int 每页数量，默认 50
        tid int 分区 默认为 0(所有分区)
        order str 排序方式，默认 pubdate
        keyword str 关键字，默认为空
        """
        params = {
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
    def elec_pay(
        session: requests.Session, bili_jct: str, uid: int, num: int = 50
    ) -> dict:
        """用 B 币给 up 主充电
        uid int up 主 uid
        num int 充电电池数量
        """
        url = "https://api.bilibili.com/x/ugcpay/trade/elec/pay/quick"
        post_data = {
            "elec_num": num,
            "up_mid": uid,
            "otype": "up",
            "oid": uid,
            "csrf": bili_jct,
        }
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def coin_add(
        session: requests.Session,
        bili_jct: str,
        aid: int,
        num: int = 1,
        select_like: int = 1,
    ) -> dict:
        """给指定 av 号视频投币
        aid int 视频av号
        num int 投币数量
        select_like int 是否点赞
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
    def live_status(session: requests.Session) -> str:
        """B站直播获取金银瓜子状态"""
        url = "https://api.live.bilibili.com/pay/v1/Exchange/getStatus"
        res = session.get(url=url).json()
        _data = res.get("data")
        silver = _data.get("silver", 0)
        gold = _data.get("gold", 0)
        coin = _data.get("coin", 0)
        return f"银瓜子数量: {silver}\n金瓜子数量: {gold}\n硬币数量: {coin}"

    @staticmethod
    def silver2coin(session: requests.Session, bili_jct: str) -> dict:
        """银瓜子兑换硬币"""
        url = "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin"
        post_data = {"csrf_token": bili_jct, "csrf": bili_jct}
        return session.post(url=url, data=post_data).json()

    @staticmethod
    def get_region(session: requests.Session, rid: int = 1, num: int = 6):
        """获取 B站分区视频信息
        rid int 分区号
        num int 获取视频数量
        """
        url = (
            "https://api.bilibili.com/x/web-interface/dynamic/region?ps="
            + str(num)
            + "&rid="
            + str(rid)
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
            bili_jct = cookie.get("bili_jct")
            coin_num = check_item.get("coin_num", 0)
            coin_type = check_item.get("coin_type", 1)
            silver2coin = check_item.get("silver2coin", True)
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
            uname, uid, is_login, coin, vip_type, current_exp = self.get_nav(
                session=session
            )
            if is_login:
                manhua_msg = self.manga_sign(session=session)
                live_msg = self.live_sign(session=session)
                aid_list = self.get_region(session=session)
                coins_av_count = len(
                    list(
                        filter(
                            lambda x: x["reason"] == "视频投币奖励",
                            self.reward(session=session),
                        )
                    )
                )
                coin_num = coin_num - coins_av_count
                coin_num = coin_num if coin_num < coin else coin
                if coin_type == 1 and coin_num:
                    following_list = self.get_followings(session=session, uid=uid)
                    for following in following_list.get("data", {}).get("list"):
                        mid = following.get("mid")
                        if mid:
                            aid_list += self.space_arc_search(session=session, uid=mid)
                success_count = 0
                if coin_num > 0:
                    for aid in aid_list[::-1]:
                        res = self.coin_add(
                            session=session, aid=aid.get("aid"), bili_jct=bili_jct
                        )
                        if res["code"] == 0:
                            coin_num -= 1
                            print(f'成功给 {aid.get("title")} 投一个币')
                            success_count += 1
                        elif res["code"] == 34005:
                            print(f'投币 {aid.get("title")} 失败，原因为 {res["message"]}')
                            continue
                            # -104 硬币不够了 -111 csrf 失败 34005 投币达到上限
                        else:
                            print(f'投币 {aid.get("title")} 失败，原因为 {res["message"]}，跳过投币')
                            break
                        if coin_num <= 0:
                            break
                    coin_msg = f"今日成功投币 {success_count + coins_av_count}/{check_item.get('coin_num', 5)} 个"
                else:
                    coin_msg = (
                        f"今日成功投币 {coins_av_count}/{check_item.get('coin_num', 5)} 个"
                    )
                aid = aid_list[0].get("aid")
                cid = aid_list[0].get("cid")
                title = aid_list[0].get("title")
                report_res = self.report_task(
                    session=session, bili_jct=bili_jct, aid=aid, cid=cid
                )
                if report_res.get("code") == 0:
                    report_msg = f"观看《{title}》 300 秒"
                else:
                    report_msg = "任务失败"
                    print(report_msg)
                share_res = self.share_task(session=session, bili_jct=bili_jct, aid=aid)
                if share_res.get("code") == 0:
                    share_msg = f"分享《{title}》成功"
                else:
                    share_msg = "分享失败"
                    print(share_msg)
                if silver2coin:
                    silver2coin_res = self.silver2coin(
                        session=session, bili_jct=bili_jct
                    )
                    if silver2coin_res["code"] == 0:
                        silver2coin_msg = "成功将银瓜子兑换为 1 个硬币"
                    else:
                        silver2coin_msg = silver2coin_res["message"]
                else:
                    silver2coin_msg = "未开启银瓜子兑换硬币功能"
                live_stats = self.live_status(session=session)
                (
                    uname,
                    uid,
                    is_login,
                    new_coin,
                    vip_type,
                    new_current_exp,
                ) = self.get_nav(session=session)
                today_exp = sum(map(lambda x: x["delta"], self.reward(session=session)))
                update_data = (28800 - new_current_exp) // (today_exp or 1)
                msg = (
                    f"帐号信息: {uname}\n漫画签到: {manhua_msg}\n直播签到: {live_msg}\n"
                    f"登陆任务: 今日已登陆\n观看视频: {report_msg}\n分享任务: {share_msg}\n投币任务: {coin_msg}\n"
                    f"银瓜子兑换硬币: {silver2coin_msg}\n今日获得经验: {today_exp}\n当前经验: {new_current_exp}\n"
                    f"按当前速度升级还需: {update_data}天\n{live_stats}"
                )
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("BILIBILI", [])
    result = BiliBili(check_items=_check_items).main()
    send("Bilibili", result)
