# -*- coding: utf-8 -*-
"""
cron: 55 14 * * *
new Env('全民K歌');
"""

import requests

from notify_mtr import send
from utils import get_data


class KGQQ:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def get_t_uuid(cookie):
        uid = cookie.split("; ")
        t_uuid = ""
        for i in uid:
            if i.find("uid=") >= 0:
                t_uuid = i.split("=")[1]
        return t_uuid

    @staticmethod
    def sign(headers, t_uuid):
        url_list = (
            [
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.getLottery&ns_inbuf=&"
                "mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIyJTNBJTIyTG"
                "90dGVyeVJlcSUyMiUyQyUyMnduc0NvbmZpZyUyMiUzQSU3QiUyMmFwcGlkJTIyJTNBMTAwMDU1NyU"
                "3RCUyQyUyMmw1YXBpJTIyJTNBJTdCJTIybW9kaWQlMjIlM0E1MDM5MzclMkMlMjJjbWQlMjIlM0E1"
                "ODk4MjQlN0QlN0Q%3D&"
                f"t_uid={t_uuid}&t_iShowEntry=1&t_type={one}"
                for one in ["1", "2"]
            ]
            + [
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.signinGetAward&"
                "mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIyJTNB"
                "JTIyR2V0U2lnbkluQXdhcmRSZXElMjIlMkMlMjJ3bnNDb25maWclMjIlM0ElN0IlMjJhcHB"
                "pZCUyMiUzQTEwMDA2MjYlN0QlMkMlMjJsNWFwaSUyMiUzQSU3QiUyMm1vZGlkJTIyJTNBNT"
                "AzOTM3JTJDJTIyY21kJTIyJTNBNTg5ODI0JTdEJTdE&"
                f"t_uid={t_uuid}&t_iShowEntry={one}"
                for one in ["1", "2", "4", "16", "128", "512"]
            ]
            + [
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.getLottery&"
                "mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIy"
                "JTNBJTIyTG90dGVyeVJlcSUyMiUyQyUyMnduc0NvbmZpZyUyMiUzQSU3QiUyMmFwcGl"
                "kJTIyJTNBMTAwMDU1NyU3RCUyQyUyMmw1YXBpJTIyJTNBJTdCJTIybW9kaWQlMjIlM0"
                "E1MDM5MzclMkMlMjJjbWQlMjIlM0E1ODk4MjQlN0QlN0Q&"
                f"t_uid={t_uuid}&t_iShowEntry=4&t_type=104",
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.getLottery&"
                "mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIy"
                "JTNBJTIyTG90dGVyeVJlcSUyMiUyQyUyMmw1YXBpJTIyJTNBJTdCJTIybW9kaWQlMjI"
                "lM0E1MDM5MzclMkMlMjJjbWQlMjIlM0E1ODk4MjQlN0QlMkMlMjJsNWFwaV9leHAxJT"
                "IyJTNBJTdCJTIybW9kaWQlMjIlM0E4MTcwODklMkMlMjJjbWQlMjIlM0EzODAxMDg4JTdEJTdE&"
                f"t_uid={t_uuid}&t_type=103",
            ]
        )

        proto_music_station_url = (
            "https://node.kg.qq.com/webapp/proxy?"
            "ns=proto_music_station&cmd=message.batch_get_music_cards&"
            "mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldEJhdGNoTXVzaWNDYX"
            "Jkc1JlcSUyMiUyQyUyMmZpbGUlMjIlM0ElMjJwcm90b19tdXNpY19zdGF"
            "0aW9uSmNlJTIyJTJDJTIyd25zRGlzcGF0Y2hlciUyMiUzQXRydWUlN0Q&"
            f"t_uUid={t_uuid}&g_tk_openkey="
        )

        url_10 = (
            "https://node.kg.qq.com/webapp/proxy?"
            "t_stReward%3Aobject=%7B%22uInteractiveType%22%3A1%2C%22uRewardType%22%3A0%2C%22u"
            "FlowerNum%22%3A15%7D&ns=proto_music_station&cmd=message.get_reward&"
            "mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldFJld2FyZFJlcSUyMiUyQyUyMmZp"
            "bGUlMjIlM0ElMjJwcm90b19tdXNpY19zdGF0aW9uSmNlJTIyJTJDJTIyd25zRGlzcGF"
            "0Y2hlciUyMiUzQXRydWUlN0Q&"
            f"t_uUid={t_uuid}&t_strUgcId="
        )

        url_15 = (
            "https://node.kg.qq.com/webapp/proxy?"
            "t_stReward%3Aobject=%7B%22uInteractiveType%22%3A0%2C%22uRewardType%22%3A0%2C%22u"
            "FlowerNum%22%3A10%7D&ns=proto_music_station&cmd=message.get_reward&"
            "mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldFJld2FyZFJlcSUyMiUyQyUyMmZp"
            "bGUlMjIlM0ElMjJwcm90b19tdXNpY19zdGF0aW9uSmNlJTIyJTJDJTIyd25zRGlzcGF"
            "0Y2hlciUyMiUzQXRydWUlN0Q&"
            f"t_uUid={t_uuid}&t_strUgcId="
        )

        proto_profile_url = (
            "https://node.kg.qq.com/webapp/proxy?"
            "ns=proto_profile&cmd=profile.getProfile&"
            "mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnByb2ZpbGVfd2ViYXBwSmNlJTIyJTJDJTIyY21kTmFtZSUyM"
            "iUzQSUyMlByb2ZpbGVHZXQlMjIlMkMlMjJhcHBpZCUyMiUzQTEwMDA2MjYlMkMlMjJkY2FwaSUyMiUzQ"
            "SU3QiUyMmludGVyZmFjZUlkJTIyJTNBMjA1MzU5NTk3JTdEJTJDJTIybDVhcGklMjIlM0ElN0IlMjJtb"
            "2RpZCUyMiUzQTI5NDAxNyUyQyUyMmNtZCUyMiUzQTI2MjE0NCU3RCUyQyUyMmlwJTIyJTNBJTIyMTAwL"
            "jExMy4xNjIuMTc4JTIyJTJDJTIycG9ydCUyMiUzQSUyMjEyNDA2JTIyJTdE&"
            f"t_uUid={t_uuid}"
        )

        try:
            old_proto_profile = requests.get(proto_profile_url, headers=headers).json()[
                "data"
            ]["profile.getProfile"]
            old_num = old_proto_profile["uFlowerNum"]
            nickname = old_proto_profile["stPersonInfo"]["sKgNick"]

            for url in url_list:
                try:
                    requests.get(url, headers=headers)
                except Exception as e:
                    print(e)

            for g_tk_openkey in range(16):
                try:
                    proto_music_station_res = requests.get(
                        f"{proto_music_station_url}{g_tk_openkey}", headers=headers
                    ).json()
                    if proto_music_station_res.get("code") == 1000:
                        return proto_music_station_res.get("msg")
                    vct_music_cards = proto_music_station_res["data"][
                        "message.batch_get_music_cards"
                    ]["vctMusicCards"]
                    vct_music_cards_list = sorted(
                        vct_music_cards,
                        key=lambda x: x["stReward"]["uFlowerNum"],
                        reverse=True,
                    )[0]
                    str_ugc_id = vct_music_cards_list["strUgcId"]
                    str_key = vct_music_cards_list["strKey"]
                    url = f"{str_ugc_id}&t_strKey={str_key}"
                    u_flower_num = vct_music_cards_list["stReward"]["uFlowerNum"]
                    if u_flower_num > 10:
                        requests.get(url_10 + url, headers=headers)
                    elif 1 < u_flower_num < 10:
                        requests.get(url_15 + url, headers=headers)
                except Exception as e:
                    print(e)

            new_proto_profile = requests.get(proto_profile_url, headers=headers).json()[
                "data"
            ]["profile.getProfile"]
            new_num = new_proto_profile["uFlowerNum"]
            get_num = int(new_num) - int(old_num)
            kg_message = (
                f"帐号信息: {nickname}\n" f"获取鲜花: {get_num} 朵\n" f"当前鲜花: {new_num} 朵"
            )
        except Exception as e:
            kg_message = str(e)
        return kg_message

    @staticmethod
    def sign_vip(headers, t_uuid):
        try:
            get_vip_info_url = (
                f"https://node.kg.qq.com/webapp/proxy?"
                f"ns=proto_vip_webapp&cmd=vip.get_vip_info&"
                f"t_uUid={t_uuid}&t_uWebReq=1&t_uGetDataFromC4B=1"
            )
            info_res = requests.get(get_vip_info_url, headers=headers).json()
            vip_status = info_res["data"]["vip.get_vip_info"]["stVipCoreInfo"][
                "uStatus"
            ]

            if vip_status == 1:
                vip_url = (
                    "https://node.kg.qq.com/webapp/proxy?"
                    f"t_uUid={t_uuid}&ns=proto_vip_webapp&"
                    "cmd=vip.get_vip_day_reward&ns_inbuf=&nocache=1613719349184&"
                    "mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldFZpcERheVJld2FyZCUyMiU3RA%3D%3D&"
                    "g_tk_openkey=642424811"
                )
                vip_day_reward = requests.get(vip_url, headers=headers).json()["data"][
                    "vip.get_vip_day_reward"
                ]
                str_tips = vip_day_reward["strTips"]
                u_cur_reward_num = vip_day_reward["uCurRewardNum"]
                vip_message = f"{str_tips} 获取 VIP 福利道具：{u_cur_reward_num}个"
            else:
                vip_message = "非 VIP 用户"

        except Exception as e:
            print(e)
            vip_message = "VIP 签到失败"

        return vip_message

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            t_uuid = self.get_t_uuid(cookie)
            headers = {"Cookie": cookie}
            msg = (
                f"{self.sign(headers, t_uuid)}\n"
                f"VIP 签到: {self.sign_vip(headers, t_uuid)}"
            )
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("KGQQ", [])
    result = KGQQ(check_items=_check_items).main()
    send("全民K歌", result)
