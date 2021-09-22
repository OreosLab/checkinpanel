#!/bin/bash

PATH="/usr/local/bin:/usr/bin:/bin"

# 初始化变量
V2P_FILE='/usr/local/app/script/Lists/task.list'
QL_FILE='/ql/config/env.sh'
IS_MACOS=$(uname | grep -c 'Darwin')
IS_DISPLAY_CONTEXT=1

# 检查环境：面板先于系统
check_env() {
    if [[ -f "${V2P_FILE}" ]]; then
        pannel="elecv2p"
    elif [[ -f "${QL_FILE}" ]]; then
        pannel="qinglong"
    elif [[ -f /etc/redhat-release ]]; then
        release="centos"
    elif [ "${IS_MACOS}" -eq 1 ]; then
        release="macos"
    elif < /etc/issue grep -q -E -i "debian"; then
        release="debian"
    elif < /etc/issue grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif < /etc/issue grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    elif < /proc/version grep -q -E -i "debian"; then
        release="debian"
    elif < /proc/version grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif < /proc/version grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    fi
}

# 获取配置
source_config() {
    check_env
    if [ "${ENV_PATH}" ]; then
        source "${ENV_PATH}"
    elif [ "${pannel}" == "elecv2p" ]; then
        source "/usr/local/app/script/Lists/.env"
    elif [ "${pannel}" == "qinglong" ]; then
        source "/ql/config/.env"
    else
        source "$(dirname "$0")/.env"
    fi
    # 是否显示上下文 默认是
    if [ "${DISPLAY_CONTEXT}" == "0" ]; then
        IS_DISPLAY_CONTEXT=0
    fi
}

# 检查账户权限
check_root() {
    if [ 0 == $UID ]; then
        echo -e "当前用户是 ROOT 用户，可以继续操作" && sleep 1
    else
        echo -e "当前非 ROOT 账号(或没有 ROOT 权限)，无法继续操作，请更换 ROOT 账号或使用 su 命令获取临时 ROOT 权限" && exit 1
    fi
}

# 检查 jq 依赖
check_jq_installed_status() {
    if [ -z "$(command -v jq)" ]; then
        echo -e "jq 依赖没有安装，开始安装..."
        check_root
        if [ ${pannel} ]; then
            apk add --no-cache jq
        elif [[ ${release} == "centos" ]]; then
            yum update && yum install jq -y
        elif [[ ${release} == "macos" ]]; then
            brew install jq
        else
            apt-get update && apt-get install jq -y
        fi
        if [ -z "$(command -v jq)" ]; then
            echo -e "jq 依赖安装失败，请检查！" && exit 1
        else
            echo -e "jq 依赖安装成功！"
        fi
    fi
}
