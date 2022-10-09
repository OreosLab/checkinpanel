# -*- encoding: utf-8 -*-
"""
cron: 22 6-22/2 * * *
new Env('RSS 订阅');
"""

from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser

from notify_mtr import send
from utils_models import History, Rss, db


class RssRobot:
    def main(self):
        self.remove_old_history()

        rss_list = Rss.select()
        post_url_list = [
            rss_history.url
            for rss_history in History.select().where(
                History.publish_at == datetime.now().strftime("%Y-%m-%d")
            )
        ]

        no = 0
        msg = ""
        for rss in rss_list:
            rss_history_list = []
            feed = feedparser.parse(rss.feed)
            title = True
            c_no = 1
            for entry in feed.entries:
                pub_t = datetime.fromtimestamp(mktime(entry["published_parsed"]))

                # 此网站单独处理
                if rss.url == "https://www.foreverblog.cn":
                    pub_t = pub_t.replace(
                        year=datetime.now(timezone.utc).year
                    ) + timedelta(hours=8)

                elif rss.url == "https://www.zhihu.com":
                    entry.link = entry.link.split("/answer")[0]

                if (
                    entry.link not in post_url_list
                    and (
                        datetime.timestamp(datetime.now(timezone.utc))
                        - datetime.timestamp(pub_t)
                    )
                    < rss.before * 86400
                ):
                    if title:
                        msg += f"<b>{rss.title.strip()}</b>\n"
                        title = False
                    msg = f'{msg}{c_no}. <a href="{entry.link}">{entry.title}</a>\n'
                    no += 1
                    c_no += 1
                    if no % 20 == 0:
                        send("RSS 订阅", msg)
                        msg = ""
                        title = False
                    rss_history_list.append(History(url=entry.link))
            with db.atomic():
                History.bulk_create(rss_history_list, batch_size=10)

        if no % 20 != 0 and msg:
            send("RSS 订阅", msg)

    @staticmethod
    def remove_old_history():
        # 只保留最近一周的记录
        week_date_range = datetime.now() + timedelta(days=-7)
        History.delete().where(
            History.publish_at < week_date_range.strftime("%Y-%m-%d")
        ).execute()


if __name__ == "__main__":
    RssRobot().main()
