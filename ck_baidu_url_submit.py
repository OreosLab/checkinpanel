# -*- coding: utf-8 -*-
"""
cron: 32 7 * * *
new Env('百度搜索资源平台');
"""

from urllib import parse

import requests

from notify_mtr import send
from utils import get_data


class BaiduUrlSubmit:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def url_submit(data_url: str, submit_url: str, times: int = 100) -> str:
        site = parse.parse_qs(parse.urlsplit(submit_url).query).get("site")[0]
        urls_data = requests.get(url=data_url)
        remian = 100000
        success_count = 0
        error_count = 0
        for one in range(times):
            try:
                response = requests.post(url=submit_url, data=urls_data)
                if response.json().get("success"):
                    remian = response.json().get("remain")
                    success_count += response.json().get("success")
                else:
                    error_count += 1
            except Exception as e:
                print(e)
                error_count += 1
        msg = (
            f"站点地址: {site}\n当天剩余的可推送 url 条数: {remian}\n成功推送的 url 条数: {success_count}\n"
            f"成功推送的 url 次数: {times - error_count}\n失败推送的 url 次数: {error_count}"
        )
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            data_url = check_item.get("data_url")
            submit_url = check_item.get("submit_url")
            times = int(check_item.get("times", 100))
            if data_url and submit_url:
                msg = self.url_submit(
                    data_url=data_url, submit_url=submit_url, times=times)
            else:
                msg = "配置错误"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("BAIDU", [])
    res = BaiduUrlSubmit(check_items=_check_items).main()
    print(res)
    send("百度搜索资源平台", res)
