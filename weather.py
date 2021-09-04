# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('天气预报');
"""

import json, os, shutil, requests
from datetime import datetime
from getENV import getdata
from checksendNotify import send


class Weather:
    def __init__(self, city_name_list):
        self.city_name_list = city_name_list

    def main(self):
        """
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :return:
        """
        try:
            with open(os.path.join(os.path.dirname(__file__), "city.json"), "r", encoding="utf-8") as city_file:
                city_map = json.loads(city_file.read())
        except:
            with open("/ql/repo/Oreomeow_checkinpanel/city.json", "r", encoding="utf-8") as city_file:
                city_map = json.loads(city_file.read())
        msg_all = ""
        for city_name in self.city_name_list:
            city_code = city_map.get(city_name, "101020100")
            weather_url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
            today_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            resp = requests.get(url=weather_url)
            if resp.status_code == 200 and resp.json().get("status") == 200:
                weather_json = resp.json()
                today_weather = weather_json.get("data").get("forecast")[1]
                notice = today_weather.get("notice")
                high = today_weather.get("high")
                low = today_weather.get("low")
                temperature = f"温度: {low[low.find(' ') + 1:]}/{high[high.find(' ') + 1:]}"
                wind = f"{today_weather.get('fx')}: {today_weather.get('fl')}"
                aqi = f"空气: {today_weather.get('aqi')}"
                msg = f"城市: {city_name}\n时间: {today_time}\n{notice}\n{temperature}\n{wind}\n{aqi}\n"
            else:
                msg = f"城市: {city_name}\n时间: {today_time}天气情况: 获取失败"
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == "__main__":
    data = getdata()
    _city_name_list = data.get("CITY_NAME_LIST", [])
    res = Weather(city_name_list=_city_name_list).main()
    print(res)
    send('天气预报', res)