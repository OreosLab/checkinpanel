# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('天气预报');
"""

import json
import os

import requests

from notify_mtr import send
from utils import get_data


class Weather:
    def __init__(self, check_items):
        self.check_items = check_items

    def main(self):
        """
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :return:
        """
        try:
            with open(
                os.path.join(os.path.dirname(__file__), "city.json"),
                "r",
                encoding="utf-8",
            ) as city_file:
                city_map = json.loads(city_file.read())
                if not city_map:
                    raise FileNotFoundError
        except FileNotFoundError:
            r = requests.get(
                "https://fastly.jsdelivr.net/gh/Oreomeow/checkinpanel@master/city.json"
            )
            if r.status_code == 200:
                city_map = r.json()
                with open(
                    os.path.join(os.path.dirname(__file__), "city.json"),
                    "w",
                    encoding="utf-8",
                ) as city_file:
                    json.dump(city_map, city_file, ensure_ascii=False)
            else:
                return "下载 city.json 失败！"
        msg_all = ""
        for city_name in self.check_items:
            city_code = city_map.get(city_name, "101020100")
            weather_url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
            r = requests.get(url=weather_url)
            if r.status_code == 200 and r.json().get("status") == 200:
                d = r.json()
                msg = (
                    "城市："
                    + d["cityInfo"]["parent"]
                    + " "
                    + d["cityInfo"]["city"]
                    + "\n日期："
                    + d["data"]["forecast"][0]["ymd"]
                    + " "
                    + d["data"]["forecast"][0]["week"]
                    + "\n天气："
                    + d["data"]["forecast"][0]["type"]
                    + "\n温度："
                    + d["data"]["forecast"][0]["high"]
                    + " "
                    + d["data"]["forecast"][0]["low"]
                    + "\n湿度："
                    + d["data"]["shidu"]
                    + "\n空气质量："
                    + d["data"]["quality"]
                    + "\nPM2.5："
                    + str(d["data"]["pm25"])
                    + "\nPM10："
                    + str(d["data"]["pm10"])
                    + "\n风力风向："
                    + d["data"]["forecast"][0]["fx"]
                    + " "
                    + d["data"]["forecast"][0]["fl"]
                    + "\n感冒指数："
                    + d["data"]["ganmao"]
                    + "\n温馨提示："
                    + d["data"]["forecast"][0]["notice"]
                    + "\n更新时间："
                    + d["time"]
                )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("CITY", [])
    res = Weather(check_items=_check_items).main()
    send("天气预报", res)
