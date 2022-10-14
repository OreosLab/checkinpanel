# -*- coding: utf-8 -*-
"""
cron: 40 7 * * *
new Env('每日新闻');
"""

import re
import traceback

import requests

from notify_mtr import send
from utils import get_data


class News:
    @staticmethod
    def parse_data(data, topic):
        if not data.get(topic):
            return ""
        msg = ""
        for key, value in data.get(topic).items():
            if key == "content":
                for i in value:
                    msg += str(i)
                msg += "\n"
            elif (
                value
                and type(value) is not bool
                and not bool(re.search("[a-z]", str(value)))
            ):
                msg += str(value) + "\n"
        return msg

    def main(self):
        msg = ""
        try:
            res = requests.get("https://news.topurl.cn/api").json()
            if res.get("code") == 200:
                data = res.get("data")
                if data.get("newsList"):
                    msg += "📮 每日新闻 📮\n"
                    for no, news_ in enumerate(data.get("newsList"), start=1):
                        msg += f'{str(no).zfill(2)}. <a href="{news_.get("url")}">{news_.get("title")}</a>\n'
                if data.get("historyList"):
                    msg += "\n🎬 历史上的今天 🎬\n"
                    for history in data.get("historyList"):
                        msg += f'{history.get("event", "")}\n'
                msg += "\n🧩 天天成语 🧩\n" + self.parse_data(data, "phrase")
                msg += "\n🎻 慧语香风 🎻\n" + self.parse_data(data, "sentence")
                msg += "\n🎑 诗歌天地 🎑\n" + self.parse_data(data, "poem")
        except Exception:
            msg += f"每日新闻: 异常 {traceback.format_exc()}"
        return msg


if __name__ == "__main__":
    _data = get_data()
    news = _data.get("NEWS")
    if news:
        result = News().main()
        send("每日新闻", result)
