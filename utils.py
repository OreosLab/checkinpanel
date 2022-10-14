# -*- coding: utf-8 -*-

import os
import sys
import traceback

import tomli

import utils_env
from utils_ver import print_ver

# 缓存全局的环境
DATA: dict = {}


def get_data() -> dict:
    """
    获取签到的配置文件。

    :return: 签到配置文件对象
    """
    print_ver()
    global DATA
    if DATA:
        return DATA

    if check_config := os.getenv("CHECK_CONFIG"):
        if not os.path.exists(check_config):
            print(f"错误：环境变量 CHECK_CONFIG 指定的配置文件 {check_config} 不存在！")
            sys.exit(1)
    else:
        check_config = utils_env.get_file_path("check.toml")
        if not check_config:
            print("错误：未检查到签到配置文件，请在指定位置创建文件或设置 CHECK_CONFIG 指定你的文件。")
            sys.exit(1)

    try:
        DATA = tomli.load(open(check_config, "rb"))
        return DATA
    except tomli.TOMLDecodeError:
        print(
            f"错误：配置文件 {check_config} 格式不对，请学习 https://toml.io/cn/v1.0.0\n错误信息：\n{traceback.format_exc()}"
        )
        sys.exit(1)
