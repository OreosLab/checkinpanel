# -*- coding: utf-8 -*-
"""
cron: 3 0 * * *
new Env('一加手机社区官方论坛');
"""

import re
import time
from urllib import parse

import requests

from notify_mtr import send
from utils import get_data


class OnePlusBBS:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        headers = {
            "Origin": "https://www.oneplusbbs.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57",
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "https://www.oneplusbbs.com/plugin-dsu_paulsign:sign.html",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,pl;q=0.4",
            "cookie": cookie
        }
        params = (
            ("id", "dsu_paulsign:sign"),
            ("operation", "qiandao"),
            ("infloat", "1"),
            ("inajax", "1"),
        )
        formhash = re.findall(r"bbs_formhash=(.*?);", cookie)[0]
        data = {
            "formhash": formhash,
            "qdxq": "kx",
            "qdmode": "1",
            "todaysay": "努力奋斗"
        }
        response = requests.post(url="https://www.oneplusbbs.com/plugin.php",
                                 headers=headers,
                                 params=params,
                                 data=data).text
        msg = re.findall(r'<div class="c">(.*?)</div>', response, re.S)
        msg = msg[0].strip() if msg else "Cookie 可能过期"
        return msg

    @staticmethod
    def draw(cookie):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.oneplusbbs.com",
            "Referer": "https://www.oneplusbbs.com/plugin-choujiang.html",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,pl;q=0.4",
            "cookie": cookie
        }
        params = (
            ("id", "choujiang"),
            ("do", "draw"),
        )
        sum_list = []
        success_count = 0
        error_count = 0
        for i in range(10):
            try:
                data = requests.post(
                    url="https://www.oneplusbbs.com/plugin.php",
                    headers=headers,
                    params=params).json()
                if data["ret"] != "":
                    ret_map = {
                        "2": 18,
                        "4": 188,
                        "5": 88,
                        "7": 8,
                    }
                    ret = data["ret"]
                    sum_list.append(ret_map.get(ret, 0))
                    one_msg = data["msg"]
                    if str(ret) in ["-1", "-6", "-7"]:
                        break
                    else:
                        success_count += 1
                else:
                    error_count += 1
                    one_msg = "抽奖失败"
            except Exception as e:
                one_msg = f"抽奖失败: {e}"
                error_count += 1
            print(f"第{i + 1}次抽奖结果：" + str(one_msg))
            time.sleep(5)
        msg = f"成功抽奖 {success_count} 次"
        draw_msg = "抽奖状态: " + str(msg)
        draw_msg += f"\n抽奖结果: 获得 {sum(sum_list) - success_count * 10} 加油"
        print(draw_msg)
        return draw_msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            bbs_uname = re.findall(r"bbs_uname=(.*?);", cookie)
            bbs_uname = bbs_uname[0].split("%7C")[0] \
                if bbs_uname else "未获取到用户信息"
            try:
                bbs_uname = parse.unquote(bbs_uname)
            except Exception as e:
                print(f"bbs_uname 转换失败: {e}")
                bbs_uname = bbs_uname
            sign_msg = self.sign(cookie=cookie)
            draw_msg = self.draw(cookie=cookie)
            msg = f"帐号信息: {bbs_uname}\n签到信息: {sign_msg}\n{draw_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("ONEPLUSBBS", [])
    res = OnePlusBBS(check_items=_check_items).main()
    print(res)
    send("一加手机社区官方论坛", res)
