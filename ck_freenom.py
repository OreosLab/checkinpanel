# -*- coding: utf-8 -*-
"""
cron: 25 7 */10 * *
new Env('FreeNom');
"""

import re

import requests

from notify_mtr import send
from utils import get_data

# 登录地址
LOGIN_URL = "https://my.freenom.com/dologin.php"

# 域名状态地址
DOMAIN_STATUS_URL = "https://my.freenom.com/domains.php?a=renewals"

# 域名续期地址
RENEW_DOMAIN_URL = "https://my.freenom.com/domains.php?submitrenewals=true"

# token 正则
token_ptn = re.compile('name="token" value="(.*?)"', re.I)

# 域名信息正则
domain_info_ptn = re.compile(
    r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>',
    re.I,
)

# 登录状态正则
login_status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)


class FreeNom:
    def __init__(self, check_items: list):
        self.check_items = check_items
        self._s = requests.Session()
        self._s.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/79.0.3945.130 Safari/537.36"
            }
        )

    def _login(self, usr: str, pwd: str) -> bool:
        self._s.headers.update(
            {
                "content-type": "application/x-www-form-urlencoded",
                "referer": "https://my.freenom.com/clientarea.php",
            }
        )
        r = self._s.post(LOGIN_URL, data={"username": usr, "password": pwd})
        return r.status_code == 200

    def main(self) -> str:
        msg = ""
        msg_all = ""

        for i, check_item in enumerate(self.check_items, start=1):
            username = check_item.get("username")
            password = check_item.get("password")

            # login
            if not self._login(usr=username, pwd=password):
                msg_all += f"account{i} login failed\n\n"
                continue

            # check domain status
            self._s.headers.update({"referer": "https://my.freenom.com/clientarea.php"})
            r = self._s.get(DOMAIN_STATUS_URL)

            # login status check
            if not re.search(login_status_ptn, r.text):
                msg_all += f"account{i} get login status failed\n\n"
                continue

            # page token
            match = re.search(token_ptn, r.text)
            if not match:
                msg_all += f"account{i} get page token failed\n\n"
                continue
            token = match[1]

            # domains
            domains = re.findall(domain_info_ptn, r.text)

            # renew domains
            res = ""
            for domain, days, renewal_id in domains:
                if int(days) < 14:
                    self._s.headers.update(
                        {
                            "referer": f"https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}",
                            "content-type": "application/x-www-form-urlencoded",
                        }
                    )
                    r = self._s.post(
                        RENEW_DOMAIN_URL,
                        data={
                            "token": token,
                            "renewalid": renewal_id,
                            f"renewalperiod[{renewal_id}]": "12M",
                            "paymentmethod": "credit",
                        },
                    )
                    res += (
                        f"{domain} 续期成功\n"
                        if r.text.find("Order Confirmation") != -1
                        else f"{domain} 续期失败"
                    )
                res += f"{domain} 还有 {days} 天续期\n"
                msg = f"账号{i}\n{res}"
            msg_all += msg + "\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("FREENOM", [])
    result = FreeNom(check_items=_check_items).main()
    send("FreeNom", result)
