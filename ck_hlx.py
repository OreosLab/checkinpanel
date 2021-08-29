# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('葫芦侠签到');
"""

import json, os, requests
from getENV import getENv
from checksendNotify import send


r = requests.Session()

class HLXCheckin:
    def __init__(self, hlx_account_list):
        self.hlx_account_list = hlx_account_list

    @staticmethod
    def login(user, passwd):
        url = 'http://floor.huluxia.com/account/login/ANDROID/4.0?platform=2&gkey=000000&app_version=4.0.0.6.2' \
              '&versioncode=20141433&market_id=floor_baidu&_key=&device_code=%5Bw%5D02%3A00%3A00%3A00%3A00%3A00 '
        params = {
            'account': user,
            'login_type': '2',
            'password': passwd
        }
        login_res = r.post(url=url, data=params)
        login_res = login_res.json()
        nick = login_res['user']['nick']
        key = login_res['_key']
        s_key = login_res['session_key']
        return nick, key, s_key

    @staticmethod
    def check(key):
        url1 = 'http://floor.huluxia.com/user/status/ANDROID/2.1'
        params = {
            'platform': '2',
            'gkey': '000000',
            'app_version': '4.0.0.6.3',
            'versioncode': '20141434',
            'market_id': 'floor_baidu',
            '_key': key,
            'device_code': '%5Bw%5D02%3A00%3A00%3A00%3A00%3A00',
        }
        check_req = r.get(url=url1, params=params)
        check_req = check_req.json()
        status = check_req['status']
        if status == 0:
            raise Exception("令牌验证失败")
        elif status == 1:
            pass
        return status

    @staticmethod
    def category(key):
        global experienceVal
        titles = []
        categoryIDs = []
        category_url = 'http://floor.huluxia.com/category/list/ANDROID/2.0'
        params = {
            'platform': '2',
            'gkey': '000000',
            'app_version': '4.0.0.6.3',
            'versioncode': '20141434',
            'market_id': 'floor_huluxia',
            '_key': key,
            'device_code': '%5Bw%5D02%3A00%3A00%3A00%3A00%3A00',
            'is_hidden': '1'
        }
        category_res = r.get(url=category_url, params=params)
        category_res = category_res.json()
        category_res = category_res["categories"]
        for i in range(3, len(category_res)):
            res = category_res[i]
            titles.append(res['title'])
            categoryIDs.append(res['categoryID'])
            # print(res)
        url = f'http://floor.huluxia.com/user/signin/ANDROID/4.0'
        all_experienceVal = 0
        for i in range(0, len(categoryIDs)):
            IDS = str(categoryIDs[i])
            params = {
                'platform': '2',
                'gkey': '000000',
                'app_version': '4.0.0.6.3',
                'versioncode': '20141434',
                'market_id': 'floor_baidu',
                '_key': key,
                'device_code': '%5Bw%5D02%3A00%3A00%3A00%3A00%3A00',
                'cat_id': IDS
            }
            try:
                experienceVal = r.get(url=url, params=params).json()['experienceVal']
            except:
                experienceVal = 0
            finally:
                all_experienceVal = all_experienceVal + experienceVal
        return '签到成功 共获得{}点经验'.format(all_experienceVal)

    def main(self):
        msg_all = ""
        for hlx_account in self.hlx_account_list: 
            user = hlx_account.get('user')
            passwd = hlx_account.get('password')
            nick, key, s_key = self.login(user, passwd)
            self.check(key)
            msg = "用户名：" + nick + self.category(key)
            msg_all += msg + '\n\n'
        return msg_all


def start():
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    _hlx_account_list = datas.get("HLX_ACCOUNT_LIST", [])
    res = HLXCheckin(hlx_account_list=_hlx_account_list).main()
    print(res)
    send('葫芦侠', res)


if __name__ == '__main__':
    start()