"""

建议cron: 30 7 * * *  python3 ck_hlx.py
new Env('葫芦侠签到');

"""
import requests
import os
from getENV import getENv
from checksendNotify import send
import json
r = requests.Session()


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


def hlx(user, passwd):
    nick, key, s_key = login(user, passwd)
    check(key)
    return "用户名：" + nick + category(key)


def start():
    getENv()
    try:
        with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        with open("/ql/config/check.json", "r", encoding="utf-8") as f:
            datas = json.loads(f.read())
    else:
        print('加载配置文件失败，请检查！')
        exit(1)
    _check_item = datas.get("HLX", [])
    res = hlx(user=_check_item.get('user'),passwd=_check_item.get('password'))
    print(res)
    send('葫芦侠', res)


if __name__ == '__main__':
    start()