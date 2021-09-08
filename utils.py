import os, json


def getdata():
    v2p_new = '/usr/local/app/script/Lists/task.list'
    ql_new = '/ql/config/env.sh'
    v2p_config_file = '/usr/local/app/script/Shell/check.json'
    ql_config_file = '/ql/config/check.json'
    print('尝试检查环境\n')
    if os.path.exists(v2p_new):
        print('成功，当前环境为 v2p 面板继续执行')
        if os.path.exists(v2p_config_file):
            print('已找到配置文件')
            try:
                with open("/usr/local/app/script/Shell/check.json", "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
                return data
            except json.JSONDecodeError:
                print('错误！请复制整个 check.json 内容到 https://www.json.cn/json/jsononline.html 中检查 JSON 格式')
                exit(1)
        else:
            print('错误！未找到配置文件\n请添加 ./script/Shell/check.json')
            exit(1)
    elif os.path.exists(ql_new):
        print('成功，当前环境为青龙面板继续执行')
        if os.path.exists(ql_config_file):
            print('已找到配置文件')
            try:
                with open("/ql/config/check.json", "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
                return data
            except json.JSONDecodeError:
                print('错误！请复制整个 check.json 内容到 https://www.json.cn/json/jsononline.html 中检查 JSON 格式')
                exit(1)            
        else:
            print('错误！未找到配置文件\n请添加 /ql/config/check.json')
            exit(1)
    else:
        print('失败！请检查环境')
        exit(0)