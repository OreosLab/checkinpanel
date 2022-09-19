# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('每日一句');
"""

import json

import requests

from notify_mtr import send
from utils import get_data


class Motto:
    @staticmethod
    def main():
        """
        从词霸中获取每日一句，带英文。
        :return:
        """
        response = requests.get(url="http://open.iciba.com/dsapi")
        if response.status_code != 200:
            return ""
        res = json.loads(response.content.decode("utf-8"))
        content = res["content"]
        note = res["note"]
        return f"{content}\n{note}\n"


if __name__ == "__main__":
    data = get_data()
    if motto := data.get("MOTTO"):
        res = Motto().main()
        send("每日一句", res)
