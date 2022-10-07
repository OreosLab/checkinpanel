# -*- coding: utf-8 -*-

import os
import platform

# 缓存全局的环境
ENV = ""


def get_env_str() -> str:
    """
    尝试获取当前系统的环境，返回字符。

    :return: Windows / Linux / Darwin / github / v2p / ql_new / ql /空
    """
    global ENV
    if ENV:
        return ENV

    v2p_file = "/usr/local/app/script/Lists/task.list"
    ql_new_file = "/ql/data/config/env.sh"
    ql_file = "/ql/config/env.sh"

    print("尝试检查运行环境...")
    if os.getenv("GITHUB_ACTIONS"):
        print("成功，当前环境为: github action 面板。")
        env = "github"
    elif os.path.exists(v2p_file):
        print("成功，当前环境为: elecV2P 面板。")
        env = "v2p"
    elif os.path.exists(ql_new_file):
        print("成功，当前环境为: 青龙面板(v2.12.0+)。")
        env = "ql_new"
    elif os.path.exists(ql_file):
        print("成功，当前环境为: 青龙面板。")
        env = "ql"

    # 面板判断优先于系统判断
    elif (e := platform.system()) == "Windows" or "Linux" or "Darwin":
        print(f"成功，当前环境为 {e}。")
        env = e
    else:
        print("失败！请检查环境。")
        env = ""

    ENV = env
    print("环境检查结束。\n")
    return env


def get_env_int() -> int:
    """
    尝试获取当前系统的环境，返回数字。

    :return: 空: -1 / Windows: 0 / Linux: 1 / Darwin: 2 / github: 3 / v2p: 4 / ql_new: 5 / ql: 6
    """
    env = get_env_str()
    if env == "Windows":
        return 0
    if env == "Linux":
        return 1
    if env == "Darwin":
        return 2
    if env == "github":
        return 3
    if env == "v2p":
        return 4
    if env == "ql_new":
        return 5
    return 6 if env == "ql" else -1


def get_file_path(file_name: str) -> str:
    """
    根据文件名返回对应环境中位置。

    :param file_name: 文件名，不含任何 "/" (即目录)
    :return: 如果有面板，返回面板默认配置文件夹，否则返回当前目录下文件。 <br/> 如果路径下文件不存在，返回空串。
    """
    env_i = get_env_int()
    print(f"配置文件 ({file_name}) 检查开始...")
    paths = [
        file_name,
        file_name,
        file_name,
        file_name,
        f"/usr/local/app/script/Lists/{file_name}",
        f"/ql/data/config/{file_name}",
        f"/ql/config/{file_name}",
    ]

    if env_i < 0:
        print("无法判断环境，选择当前目录为配置文件夹目录。")
        env_i = 0
    if not os.path.exists(paths[env_i]):
        print(f"未找到配置文件（不一定是错误），路径为: {paths[env_i]}。")
        print("配置文件检查结束。\n")
        return ""
    print(f"在 {paths[env_i]} 发现配置文件。")
    print("配置文件检查结束。\n")
    return paths[env_i]
