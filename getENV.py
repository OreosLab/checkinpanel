import os


def getENv():
    v2p_new='./script/Lists/task.list'
    config_file = './script/Shell/check.json'
    print('尝试检查环境\n')
    if os.path.exists(v2p_new):
        print('成功 当前环境为 v2p 面板继续执行')
        if os.path.exists(config_file):
            print('已找到配置文件')
        else:
            print('未找到配置文件\n')
            print('请添加./script/JSFile/check.json')
            exit(1)
    else:
        print('失败 请检查环境')
        exit(0)