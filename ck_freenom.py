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
    re.I)

# 登录状态正则
login_status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)


class FreeNom:
    def __init__(self, check_items: dict):
        self.check_items = check_items
        self._s = requests.Session()
        self._s.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/79.0.3945.130 Safari/537.36"
        })

    def _login(self, usr: str, pwd: str) -> bool:
        self._s.headers.update({
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://my.freenom.com/clientarea.php"
        })
        r = self._s.post(LOGIN_URL, data={"username": usr, "password": pwd})
        return r.status_code == 200

    def main(self) -> str:
        msg_all = ""
        i = 1

        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")

            # login
            ok = self._login(usr=username, pwd=password)
            if not ok:
                msg = f"account{i} login failed\n"

            # check domain status
            self._s.headers.update({"referer": "https://my.freenom.com/clientarea.php"})
            r = self._s.get(DOMAIN_STATUS_URL)

            # login status check
            if not re.search(login_status_ptn, r.text):
                msg = f"account{i} get login status failed\n"

            # page token
            match = re.search(token_ptn, r.text)
            if not match:
                msg = f"account{i} get page token failed\n"
            token = match.group(1)

            # domains
            domains = re.findall(domain_info_ptn, r.text)

            # renew domains
            result = ""
            for domain, days, renewal_id in domains:
                days = int(days)
                if days < 14:
                    self._s.headers.update({
                        "referer": f"https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}",
                        "content-type": "application/x-www-form-urlencoded"
                    })
                    r = self._s.post(RENEW_DOMAIN_URL, data={
                        "token": token,
                        "renewalid": renewal_id,
                        f"renewalperiod[{renewal_id}]": "12M",
                        "paymentmethod": "credit"
                    })
                    result += f"{domain} 续期成功\n" if r.text.find("Order Confirmation") != -1 else f"{domain} 续期失败"
                result += f"{domain} 还有 {days} 天续期\n"
                msg = f"账号{i}\n" + result
            i += 1
            msg_all += msg + "\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("FREENOM", [])
    res = FreeNom(check_items=_check_items).main()
    print(res)
    send("FreeNom", res)
