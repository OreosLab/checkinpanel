#!/usr/bin/env python3
"""
:author @night-raise  from github
cron: 0 0 */7 * *
new Env('随机定时');
"""

from abc import ABC
from random import randrange
from typing import Dict, List

import requests

from notify_mtr import send
from utils import get_data
from utils_env import get_env_int


class ClientApi(ABC):
    def __init__(self):
        self.cid = ""
        self.sct = ""
        self.url = "http://localhost:5700/"
        self.twice = False
        self.token = ""
        self.cron: List[Dict] = []

    def init_cron(self):
        raise NotImplementedError

    def shuffle_cron(self):
        raise NotImplementedError

    def run(self):
        self.init_cron()
        self.shuffle_cron()

    @staticmethod
    def get_ran_min() -> str:
        return str(randrange(0, 60))

    def get_ran_hour(self, is_api: bool = False) -> str:
        if is_api:
            return str(randrange(7, 9))
        if self.twice:
            start = randrange(0, 12)
            return f"{start},{start + randrange(6, 12)}"
        return str(randrange(0, 24))

    def random_time(self, origin_time: str, command: str):
        if command.find("ran_time") != -1:
            return origin_time
        if command.find("rssbot") != -1 or command.find("hax") != -1:
            return ClientApi.get_ran_min() + " " + " ".join(origin_time.split(" ")[1:])
        if command.find("api") != -1:
            return (
                ClientApi.get_ran_min()
                + " "
                + self.get_ran_hour(True)
                + " "
                + " ".join(origin_time.split(" ")[2:])
            )
        return (
            ClientApi.get_ran_min()
            + " "
            + self.get_ran_hour()
            + " "
            + " ".join(origin_time.split(" ")[2:])
        )


class QLClient(ClientApi):
    def __init__(self, client_info: Dict):
        super().__init__()
        if (
            not client_info
            or not (cid := client_info.get("client_id"))
            or not (sct := client_info.get("client_secret"))
        ):
            raise ValueError("无法获取 client 相关参数！")
        else:
            self.cid = cid
            self.sct = sct
        self.url = client_info.get("url", "http://localhost:5700").rstrip("/") + "/"
        self.twice = client_info.get("twice", False)
        self.token = requests.get(
            url=self.url + "open/auth/token",
            params={"client_id": self.cid, "client_secret": self.sct},
        ).json()["data"]["token"]
        if not self.token:
            raise ValueError("无法获取 token！")

    def init_cron(self):
        self.cron: List[Dict] = list(
            filter(
                lambda x: not x.get("isDisabled", 1)
                and x.get("command", "").find("Oreomeow_checkinpanel_master") != -1,
                requests.get(
                    url=self.url + "open/crons",
                    headers={"Authorization": f"Bearer {self.token}"},
                ).json()["data"],
            )
        )

    def shuffle_cron(self):
        for c in self.cron:
            json = {
                "labels": c.get("labels", None),
                "command": c["command"],
                "schedule": self.random_time(c["schedule"], c["command"]),
                "name": c["name"],
                "id": c["id"],
            }
            requests.put(
                url=self.url + "open/crons",
                json=json,
                headers={"Authorization": f"Bearer {self.token}"},
            )


def get_client():
    env_type = get_env_int()
    if env_type == 5 or env_type == 6:
        check_data = get_data()
        return QLClient(check_data.get("RANDOM", [[]])[0])


try:
    get_client().run()
    send("随机定时", "处于启动状态的任务定时修改成功！")
except ValueError as e:
    send("随机定时", f"配置错误，{e},请检查你的配置文件！")
except AttributeError:
    send("随机定时", "你的系统不支持运行随机定时！")
