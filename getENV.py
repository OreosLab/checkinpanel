import os


def getENv():
    v2p_new='/usr/local/app/script/Lists/task.list'
    ql_new = '/ql/config/env.sh'
    v2p_config_file = '/usr/local/app/script/Shell/check.json'
    ql_config_file = '/ql/config/check.json'
    print('尝试检查环境\n')
    if os.path.exists(v2p_new):
        print('成功 当前环境为 v2p 面板继续执行')
        if os.path.exists(v2p_config_file):
            print('已找到配置文件')
        else:
            print('未找到配置文件\n')
            print('请添加./script/Shell/check.json')
            exit(1)
    elif os.path.exists(ql_new):
        print('成功 当前环境为青龙面板继续执行')
        if os.path.exists(ql_config_file):
            print('已找到配置文件')
        else:
            print('未找到配置文件\n')
            print('请添加/ql/config/check.json')
            exit(1)
    else:
        print('失败 请检查环境')
        exit(0)