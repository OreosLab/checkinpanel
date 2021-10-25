# -*- coding: utf-8 -*-
"""
cron: 10 6 * * *
new Env('联想乐云');
"""

import requests

from notify_mtr import send
from utils import get_data


class LECloud:
    def __init__(self, check_items):
        self.check_items = check_items
        self.total_size = ""

    def userinfo(self, cookie):
        url = "https://pimapi.lenovomm.com/userspaceapi/storage/userinfo"
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Linux; Android 11; PCAM00 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 com.lenovo.leos.cloud.sync/6.3.0.99",
        }
        res = requests.post(url=url, headers=headers)
        if "error" in res.text:
            print("cookie 失效")
        else:
            self.total_size = res.json().get("data", {}).get("totalSize") // 1048576

    # 签到
    def addspace(self, cookie):
        url = "https://pim.lenovo.com/lesynch5/userspaceapi/v4/addspace"
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Linux; Android 11; PCAM00 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 com.lenovo.leos.cloud.sync/6.3.0.99",
        }
        res = requests.get(url=url, headers=headers)
        if "spaceadd" in res.text:
            data = res.json()
            if "lastspaceadd" in res.text:
                msg = f'今日以获{data.get("lastspaceadd")}M, 总空间{self.total_size}M'
            else:
                msg = f'获得{data.get("spaceadd")}M, 总空间{self.total_size + data.get("spaceadd")}M'
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            self.usrinfo(cookie)
            msg = self.addspace(cookie)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("LECLOUD", [])
    res = LECloud(check_items=_check_items).main()
    send("联想乐云", res)
