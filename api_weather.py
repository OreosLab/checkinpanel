# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('天气预报');
"""

import json
from os.path import dirname, join

import requests

from notify_mtr import send
from utils import get_data


class Weather:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def city_map():
        cur_dir = dirname(__file__)
        try:
            with open(join(cur_dir, "city.json"), "r", encoding="utf-8") as city_file:
                city_map = json.load(city_file)
                if not city_map:
                    raise FileNotFoundError
        except FileNotFoundError as e:
            r = requests.get(
                "https://fastly.jsdelivr.net/gh/Oreomeow/checkinpanel@master/city.json"
            )
            if r.status_code != 200:
                raise ConnectionError("下载 city.json 失败！") from e
            city_map = r.json()
            with open(join(cur_dir, "city.json"), "w", encoding="utf-8") as city_file:
                json.dump(city_map, city_file, ensure_ascii=False)
        return city_map

    def main(self):
        msg_all = ""
        for city_name in self.check_items:
            city_code = self.city_map().get(city_name, "101020100")
            weather_url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
            r = requests.get(weather_url)
            if r.status_code == 200 and r.json().get("status") == 200:
                d = r.json()
                msg = (
                    f'城市：{d["cityInfo"]["parent"]} {d["cityInfo"]["city"]}\n'
                    f'日期：{d["data"]["forecast"][0]["ymd"]} {d["data"]["forecast"][0]["week"]}\n'
                    f'天气：{d["data"]["forecast"][0]["type"]}\n'
                    f'温度：{d["data"]["forecast"][0]["high"]} {d["data"]["forecast"][0]["low"]}\n'
                    f'湿度：{d["data"]["shidu"]}\n'
                    f'空气质量：{d["data"]["quality"]}\n'
                    f'PM2.5：{d["data"]["pm25"]}\n'
                    f'PM10：{d["data"]["pm10"]}\n'
                    f'风力风向 {d["data"]["forecast"][0]["fx"]} {d["data"]["forecast"][0]["fl"]}\n'
                    f'感冒指数：{d["data"]["ganmao"]}\n'
                    f'温馨提示：{d["data"]["forecast"][0]["notice"]}\n'
                    f'更新时间：{d["time"]}'
                )
            else:
                msg = f"{city_name} 天气查询失败！"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("CITY", [])
    result = Weather(check_items=_check_items).main()
    send("天气预报", result)
