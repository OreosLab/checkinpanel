# -*- coding: utf-8 -*-
"""
cron: 21 */6 * * *
new Env('Hax');
"""

import re

import requests
from bs4 import BeautifulSoup

from notify_mtr import send
from utils import get_data


class Hax:
    def check(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
            "Content-type": "application/json",
        }
        datas = requests.get(url, headers=headers).text
        return datas

    def get_server_info(self):
        html_text = self.check("https://hax.co.id/data-center")
        soup = BeautifulSoup(html_text, "html.parser")
        zone_list = [x.text for x in soup("h5", class_="card-title mb-4")]
        sum_list = [x.text for x in soup("h1", class_="card-text")]
        vps_list = []
        vps_dict = {}
        vps_str = ""
        for k, v in zip(zone_list, sum_list):
            zone = k.split("-", 1)[0].lstrip("./")
            sum = (
                k.split("-", 1)[1] + "(" + v.rstrip(" VPS") + "♝)"
                if len(k.split("-", 1)) > 1
                else v
            )
            vps_list.append((zone, sum))
        for k_v in vps_list:
            k, v = k_v
            vps_dict.setdefault(k, []).append(v)
        for k, v in vps_dict.items():
            vps_str += ">>" + k + "-" + ", ".join(v) + "\n"
        return vps_str

    def get_data_center(self):
        html_text = self.check("https://hax.co.id/create-vps")
        soup = BeautifulSoup(html_text, "html.parser")
        ctr_list = [x.text for x in soup("option", value=re.compile(r"^[A-Z]{2,}-"))]
        vir_list = [(c.split(" (")[1].rstrip(")"), c.split(" (")[0]) for c in ctr_list]
        vir_dict = {}
        vir_str = ""
        for k_v in vir_list:
            k, v = k_v
            vir_dict.setdefault(k, []).append(v)
        for k, v in vir_dict.items():
            vir_str += "★" + k + "★ " + ", ".join(v) + "\n"
        return vir_str

    def main(self):
        vps_str = self.get_server_info()
        srv_stat = f"[🛰Server Stats / 已开通数据]\n{vps_str}\n"
        vir_str = self.get_data_center()
        data_center = f"[🚩Available Centers / 可开通区域]\n{vir_str}\n"
        FOCUS = "[♨Special Focus / 特别关注]\n"
        eu_mid1 = (
            f"{FOCUS}EU Middle Specs (KVM + SSD) are NOT available now. 暂时没有库存。"
            if "EU Middle Specs" not in vir_str
            else f"{FOCUS}CHECK https://hax.co.id/create-vps NOW!!! EU Middle Specs (KVM + SSD) are available now. 有库存！"
        )
        msg = srv_stat + data_center + eu_mid1
        return msg


if __name__ == "__main__":
    data = get_data()
    hax = data.get("HAX")
    if hax:
        res = Hax().main()
        send("Hax", res)
