# -*- coding: utf-8 -*-
"""
cron: 21 */6 * * *
new Env('Hax');
"""

from random import choice

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data


class Hax:
    @staticmethod
    def get_ua(brower_name):
        url = "https://ghproxy.com/https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/user-agent.json"
        useragent = choice(requests.get(url).json()[brower_name])
        return useragent

    def check(self, url):
        headers = {
            "User-Agent": self.get_ua("Safari"),
            "Content-type": "application/json",
        }
        datas = requests.get(url, headers=headers).text
        return datas

    def get_server_info(self):
        html_text = self.check("https://hax.co.id/server")
        soup = BeautifulSoup(html_text, "html.parser")
        zone_tags = soup("h5", class_="card-title mb-4")
        sum_tags = soup("h1", class_="card-text")
        vps_dict = dict(map(lambda x, y: [x.text, y.text], zone_tags, sum_tags))
        return vps_dict

    def check_data_center(self, data_center):
        html_text = self.check("https://hax.co.id/create-vps")
        soup = BeautifulSoup(html_text, "html.parser")
        if soup.find("option", value=data_center):
            return True
        else:
            return None

    def main(self):
        msg = ""
        vps_dict = self.get_server_info()
        for k, v in vps_dict.items():
            msg += str(k) + "\t" + str(v) + "\n"
        has_eu_mid1 = self.check_data_center("EU Middle Specs")
        msg += (
            "EU Middle Specs (KVM + SSD) are NOT available now.\t暂时没有库存。"
            if not has_eu_mid1
            else "CHECK https://hax.co.id/create-vps NOW!!! EU Middle Specs (KVM + SSD) are available now.\t有库存！。"
        )
        return msg


if __name__ == "__main__":
    data = get_data()
    hax = data.get("HAX")
    if hax:
        res = Hax().main()
        send("Hax", res)
