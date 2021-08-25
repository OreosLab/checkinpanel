# -*- coding: utf-8 -*-
"""
@Time: 2021/3/21 12:01
@Auth: Icrons
@IDE: PyCharm
@Modifier: Oreo
cron: 20 10 * * *
new Env('机场签到');
"""
import json
import os
import re
import requests
from getENV import getENv
from checksendNotify import send


requests.packages.urllib3.disable_warnings()

class SspanelQd(object):
    def __init__(self,check_item):
        self.check_item = check_item

    @staticmethod
    def checkin(url,email,password):
        email = email.split('@')
        email = email[0] + '%40' + email[1]
        session = requests.session()
        try:
            #以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            session.get(url, verify=False)  
        except requests.exceptions.ConnectionError:
            msg = url + '\n\n' + '网络不通'
            print(msg)
            return msg
        except requests.exceptions.ChunkedEncodingError:
            msg = url + '\n\n' + '分块编码错误'
            print(msg)
            return msg
        except:
            msg = url + '\n\n' + '未知错误'
            print(msg)
            return msg

        login_url = url + '/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        post_data = 'email=' + email + '&passwd=' + password + '&code='
        post_data = post_data.encode()
        session.post(login_url, post_data, headers=headers, verify=False)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': url + '/user'
        }

        response = session.post(url + '/user/checkin', headers=headers, verify=False)
        # print(response.text)
        msg = (response.json()).get('msg')
        print(msg)

        info_url = url + '/user'
        response = session.get(info_url, verify=False)
        """
        以下只适配了editXY主题
        """
        try:
            level = re.findall(r'\["Class", "(.*?)"],', response.text)[0]
            day = re.findall(r'\["Class_Expire", "(.*)"],', response.text)[0]
            rest = re.findall(r'\["Unused_Traffic", "(.*?)"]', response.text)[0]
            msg = "- 今日签到信息：" + str(msg) + "\n- 用户等级：" + str(level) + "\n- 到期时间：" + str(day) + "\n- 剩余流量：" + str(rest)
            print(msg)
            return msg
        except:
            return msg
        
    def main(self):
        # 机场地址
        url = str(self.check_item.get("airport_url"))
        # 登录信息
        email = str(self.check_item.get("airport_email"))
        password = str(self.check_item.get("airport_password"))
        msg = self.checkin(url,email,password)
        return msg

def start():
    getENv()
    with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("AIRPORT_ACCOUNT_LIST", [])[0]
    res=SspanelQd(check_item=_check_item).main()
    print(res)
    send('机场签到', res)

if __name__ == "__main__":
    start()