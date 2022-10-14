# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('每日一句');
"""

import requests

from notify_mtr import send
from utils import get_data


class Motto:
    @staticmethod
    def main():
        """从词霸中获取每日一句，带英文

        :return: str
        """
        response = requests.get("http://open.iciba.com/dsapi")
        if response.status_code != 200:
            return ""
        res = response.json()
        return f'{res["content"]}\n{res["note"]}\n'


if __name__ == "__main__":
    _data = get_data()
    motto = _data.get("MOTTO")
    if motto:
        result = Motto().main()
        send("每日一句", result)
