#!/bin/env python3
"""
:author @night-raise  from github
cron: 0 0 */7 * *
new Env('随机定时');
"""

import json
import os
import random
import re
import time

from notify_mtr import send
from utils import get_data


def change_db():
    lines = []
    first = True
    with open("/ql/db/crontab.db", "r", encoding="UTF-8") as f:
        for i in f.readlines():
            if i.find("Oreomeow_checkinpanel_master") != -1:
                record = json.loads(i)
                if record.get("isDisabled") == 0:
                    if i.find("motto") != -1 or i.find("leetcode") != -1 or i.find("weather") != -1:
                        record["schedule"] = change_time(record["schedule"], True)
                    else:
                        record["schedule"] = change_time(record["schedule"], first)
                if first:
                    first = False
                lines.append(json.dumps(record, ensure_ascii=False) + "\n")
            else:
                lines.append(i)

    time_str = time.strftime("%Y-%m-%d", time.localtime())
    os.system(f"copy /ql/db/crontab.db /ql/db/crontab.db.{time_str}.back")

    with open("/ql/db/crontab.db", "w", encoding="UTF-8") as f:
        f.writelines(lines)


def change_time(time_str: str, first: bool):
    words = re.sub("\\s+", " ", time_str).split()
    if first:
        words[0] = str(random.randrange(0, 60, step=5))
        words[1] = str(random.randrange(8, 9))
    else:
        words[0] = str(random.randrange(60))
        words[1] = str(random.randrange(22))
    return " ".join(words)


data = get_data()
ran_t = data.get("QL_RANDOM_TIME")
if ran_t:
    change_db()
    os.system("ql check")
    send("随机定时", "处于启动状态的任务定时修改成功！")
