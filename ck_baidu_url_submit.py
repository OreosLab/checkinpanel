# -*- coding: utf-8 -*-
"""
cron: 32 7 * * *
new Env('百度搜索资源平台');
"""

import json, os, requests
from urllib import parse
from getENV import getENv
from checksendNotify import send


class BaiduUrlSubmit:
    def __init__(self, baidu_url_submit_list: list):
        self.baidu_url_submit_list = baidu_url_submit_list

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
        for baidu_url_submit in self.baidu_url_submit_list:
            data_url = baidu_url_submit.get("data_url")
            submit_url = baidu_url_submit.get("submit_url")
            times = int(baidu_url_submit.get("times", 100))
            if data_url and submit_url:
                msg = self.url_submit(data_url=data_url, submit_url=submit_url, times=times)
            else:
                msg = "配置错误"
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == "__main__":
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
    _baidu_url_submit_list = data.get("BAIDU_URL_SUBMIT_LIST", [])
    res = BaiduUrlSubmit(baidu_url_submit_list=_baidu_url_submit_list).main()
    print(res)
    send("百度搜索资源平台", res)