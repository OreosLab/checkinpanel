# -*- coding: utf-8 -*-
"""
cron: 12 16 * * *
new Env('百度贴吧');
"""

import hashlib
import re

import requests

from notify_mtr import send
from utils import get_data


class Tieba:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def login_info(session):
        return session.get("https://zhidao.baidu.com/api/loginInfo").json()

    def valid(self, session):
        try:
            res = session.get("http://tieba.baidu.com/dc/common/tbs").json()
        except Exception as e:
            return False, f"登录验证异常，错误信息: {e}"
        if res["is_login"] == 0:
            return False, "登录失败，cookie 异常"
        tbs = res["tbs"]
        user_name = self.login_info(session=session)["userName"]
        return tbs, user_name

    @staticmethod
    def tieba_list_more(session):
        res = session.get(
            "https://tieba.baidu.com/f/like/mylike?&pn=1",
            timeout=(5, 20),
            allow_redirects=False,
        ).text
        try:
            pn = int(
                re.match(r".*/f/like/mylike\?&pn=(.*?)\">尾页.*", res, re.S | re.I)[1]
            )

        except Exception:
            pn = 1
        pattern = re.compile(r".*?<a href=\"/f\?kw=.*?title=\"(.*?)\">")
        for next_page in range(2, pn + 2):
            yield from pattern.findall(res)
            res = session.get(
                f"https://tieba.baidu.com/f/like/mylike?&pn={next_page}",
                timeout=(5, 20),
                allow_redirects=False,
            ).text

    def get_tieba_list(self, session):
        return list(self.tieba_list_more(session))

    @staticmethod
    def sign(session, tb_name_list, tbs):
        success_count, error_count, exist_count, shield_count = 0, 0, 0, 0
        for tb_name in tb_name_list:
            md5 = hashlib.md5(
                f"kw={tb_name}tbs={tbs}tiebaclient!!!".encode("utf-8")
            ).hexdigest()
            data = {"kw": tb_name, "tbs": tbs, "sign": md5}
            try:
                res = session.post(
                    url="http://c.tieba.baidu.com/c/c/forum/sign", data=data
                ).json()
                if res["error_code"] == "0":
                    success_count += 1
                elif res["error_code"] == "160002":
                    exist_count += 1
                elif res["error_code"] == "340006":
                    shield_count += 1
                else:
                    error_count += 1
            except Exception as e:
                print(f"贴吧 {tb_name} 签到异常，原因{str(e)}")
        return (
            f"贴吧总数: {len(tb_name_list)}\n"
            f"签到成功: {success_count}\n"
            f"已经签到: {exist_count}\n"
            f"被屏蔽的: {shield_count}\n"
            f"签到失败: {error_count}"
        )

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }
            session = requests.session()
            session.cookies.update(cookie)
            session.headers.update({"Referer": "https://www.baidu.com/"})
            tbs, user_name = self.valid(session)
            if tbs:
                tb_name_list = self.get_tieba_list(session)
                msg = f"帐号信息: {user_name}\n{self.sign(session, tb_name_list, tbs)}"
            else:
                msg = f"帐号信息: {user_name}\n签到状态: Cookie 可能过期"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("TIEBA", [])
    result = Tieba(check_items=_check_items).main()
    send("百度贴吧", result)
