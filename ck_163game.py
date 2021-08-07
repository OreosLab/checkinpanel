import requests
import json
from getENV import getENv
from checksendNotify import send

"""
建议cron: 20 8 * * *
new Env('网易云游戏');
"""

def game163(Authorization):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36',
        ##    下面填抓包来的参数########
        'Authorization': Authorization
    }
    url = 'http://n.cg.163.com/api/v2/sign-today'
    r = requests.post(url, headers=headers).text
    if r[0] == "{":
        return "cookie已失效"
    else:
        return "签到成功"


def start():
    getENv()
    with open("/ql/config/check.json", "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("163game", [])
    res = game163(_check_item.get('Authorization'))
    print(res)
    send("网易云游戏", res)
