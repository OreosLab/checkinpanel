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
    def get_obj_key_value(self, data: dict, obj_name: str) -> str:
        if data.get(obj_name) != {}:
            msg = ""
            need_obj = data.get(obj_name)
            items = need_obj.items()
            for key, value in items:
                if key == "content":
                    for i in value:
                        msg += str(i)
                    msg += "\n"
                elif (
                    type(value) is not bool
                    and len(value) != 0
                    and not bool(re.search("[a-z]", str(value)))
                ):
                    msg += str(value) + "\n"
            return msg

    def main(self):
        msg = ""
        try:
            res = requests.get(url=f"https://news.topurl.cn/api").json()
            if res.get("code") == 200:
                data = res.get("data", {})
                if data.get("newsList") != []:
                    msg += "\n📮 每日新闻 📮\n"
                    no = 1
                    for news in data.get("newsList", []):
                        msg += f'{str(no).zfill(2)}. {news.get("title", "")}\n'
                        no += 1
                if data.get("historyList") != []:
                    msg += "\n🎬 历史上的今天 🎬\n"
                    for history in data.get("historyList", []):
                        msg += f'{history.get("event", "")}\n'
                msg += "\n🧩 天天成语 🧩\n" + self.get_obj_key_value(data, "phrase")
                msg += "\n🎻 慧语香风 🎻\n" + self.get_obj_key_value(data, "sentence")
                msg += "\n🎑 诗歌天地 🎑\n" + self.get_obj_key_value(data, "poem")
        except Exception:
            msg += f"每日新闻: 异常 {traceback.format_exc()}"
        return msg


if __name__ == "__main__":
    data = get_data()
    news = data.get("NEWS")
    if news:
        res = News().main()
        send("每日新闻", res)
