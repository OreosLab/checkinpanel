# -*- coding: utf-8 -*-
"""
cron: 55 15 * * *
new Env('MEIZU 社区');
"""

import time

import requests

from notify_mtr import send
from utils import get_data


class Meizu:
    def __init__(self, check_items):
        self.check_items = check_items
        self.url = "https://bbs-act.meizu.cn/index.php"

    def sign(self, cookie):
        headers = {
            "authority": "bbs-act.meizu.cn",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
            "origin": "https://bbs.meizu.cn",
            "referer": "https://bbs.meizu.cn/",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cookie": cookie,
        }
        params = (("mod", "signin"), ("action", "sign"))
        res = requests.get(self.url, headers=headers, params=params).json()
        return res.get("message")

    def draw(self, cookie, count=0):
        headers = {
            "authority": "bbs-act.meizu.cn",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://bbs-act.meizu.cn",
            "referer": "https://bbs-act.meizu.cn/2/index.html",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": cookie,
        }
        data = {"mod": "index", "action": "draw", "id": "2"}
        award_list = []
        if count:
            success_count = 0
            for i in range(count):
                try:
                    res = requests.post(self.url, data, headers=headers).json()
                    if res["code"] == 200:
                        one_msg = res.get("data", {}).get("award_name")
                        award_list.append(one_msg)
                        success_count += 1
                    else:
                        print(res.get("code"), res.get("message"))
                        one_msg = "抽奖失败"
                except Exception as e:
                    one_msg = f"抽奖失败: {e}"
                print(f"第 {i + 1} 次抽奖结果: {str(one_msg)}")
                time.sleep(5)
            msg = f"成功抽奖 {success_count} 次"
            draw_msg = f"抽奖状态: {str(msg)}"
            draw_msg += f"\n抽奖结果: {';'.join(award_list)}"
        else:
            draw_msg = "抽奖结果: 未开启抽奖"
        data = {"mod": "index", "action": "get_user_count", "id": "2"}
        user_info = requests.post(self.url, data, headers=headers).json()
        uid = user_info.get("data", {}).get("uid")
        return draw_msg, uid

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            try:
                draw_count = int(check_item.get("draw_count", 0))
            except Exception as e:
                print("初始化抽奖次数失败: 重置为 0 ", e)
                draw_count = 0
            sign_msg = self.sign(cookie)
            draw_msg, uid = self.draw(cookie, draw_count)
            msg = f"帐号信息: {uid}\n签到信息: {sign_msg}\n{draw_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("MEIZU", [])
    result = Meizu(check_items=_check_items).main()
    send("MEIZU 社区", result)
