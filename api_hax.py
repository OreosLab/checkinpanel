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
    @staticmethod
    def check(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Content-type": "application/json",
        }
        return requests.get(url, headers=headers).text

    def get_server_info(self, url):
        html_text = self.check(url)
        soup = BeautifulSoup(html_text, "html.parser")
        zone_list = [x.text for x in soup("h5", class_="card-title mb-4")]
        sum_list = [x.text for x in soup("h1", class_="card-text")]
        vps_list = []
        vps_dict = {}
        for k, v in zip(zone_list, sum_list):
            zone = k.split("-", 1)[0].lstrip("./")
            sum_ = (
                k.split("-", 1)[1] + "(" + v.rstrip(" VPS") + "♝)"
                if len(k.split("-", 1)) > 1
                else v
            )
            vps_list.append((zone, sum_))
        for k_v in vps_list:
            k, v = k_v
            vps_dict.setdefault(k, []).append(v)
        return "".join(f">>{k}-" + ", ".join(v) + "\n" for k, v in vps_dict.items())

    def get_data_center(self, url, vir=False):
        html_text = self.check(url)
        soup = BeautifulSoup(html_text, "html.parser")
        ctr_list = [x.text for x in soup("option", value=re.compile(r"^[A-Z]{2,}-"))]
        ctr_str = "\n".join(ctr_list)
        if vir:
            ctr_list = [
                (c.split(" (")[1].rstrip(")"), c.split(" (")[0]) for c in ctr_list
            ]
            ctr_dict = {}
            for k_v in ctr_list:
                k, v = k_v
                ctr_dict.setdefault(k, []).append(v)
            ctr_str = "".join(
                f"★{k}★ " + ", ".join(v) + "\n" for k, v in ctr_dict.items()
            )
        return ctr_str

    def main(self):
        hax_str = self.get_server_info("https://hax.co.id/data-center")
        hax_stat = f"[🛰Hax Stats / Hax 开通数据]\n{hax_str}\n"
        vir_str = self.get_data_center("https://hax.co.id/create-vps", True)
        woiden_str = self.get_data_center("https://woiden.id/create-vps")
        data_center = (
            f"[🚩Available Centers / 可开通区域]\n"
            f'---------- <a href="https://hax.co.id/create-vps">Hax</a> ----------\n'
            f"{vir_str}"
            f'---------- <a href="https://woiden.id/create-vps">Woiden</a> ----------\n'
            f"{woiden_str}\n"
        )
        return hax_stat + data_center


if __name__ == "__main__":
    _data = get_data()
    hax = _data.get("HAX")
    if hax:
        result = Hax().main()
        send("Hax", result)
