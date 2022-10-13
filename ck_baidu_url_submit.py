# -*- coding: utf-8 -*-
"""
cron: 32 7 * * *
new Env('百度搜索资源平台');
"""

from urllib.parse import parse_qs, urlsplit

import requests

from notify_mtr import send
from utils import get_data


class BaiduUrlSubmit:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def url_submit(data_url: str, submit_url: str, times: int = 100) -> str:
        site = parse_qs(urlsplit(submit_url).query).get("site", [])[0]
        urls_data = requests.get(data_url)
        remain = 100000
        success_count = 0
        error_count = 0
        for _ in range(times):
            try:
                res = requests.post(submit_url, data=urls_data).json()
                if res.get("success"):
                    remain = res.get("remain")
                    success_count += res.get("success")
                else:
                    error_count += 1
            except Exception as e:
                print(e)
                error_count += 1
        return (
            f"站点地址: {site}\n"
            f"当天剩余的可推送 url 条数: {remain}\n"
            f"成功推送的 url 条数: {success_count}\n"
            f"成功推送的 url 次数: {times - error_count}\n"
            f"失败推送的 url 次数: {error_count}"
        )

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            data_url = check_item.get("data_url")
            submit_url = check_item.get("submit_url")
            times = int(check_item.get("times", 100))
            if data_url and submit_url:
                msg = self.url_submit(data_url, submit_url, times)
            else:
                msg = "配置错误"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("BAIDU", [])
    result = BaiduUrlSubmit(check_items=_check_items).main()
    send("百度搜索资源平台", result)
