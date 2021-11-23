#!/usr/bin/env bash

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# 初始化变量
V2P_FILE='/usr/local/app/script/Lists/task.list'
QL_FILE='/ql/config/env.sh'
IS_DISPLAY_CONTEXT=1

# 检查环境：面板先于系统
# shellcheck disable=SC2034
check_env() {
    if [ -f "${V2P_FILE}" ]; then
        pannel="elecv2p"
    elif [ -f "${QL_FILE}" ]; then
        pannel="qinglong"
    else
        CMD=(
            "$(grep -i pretty_name /etc/os-release 2>/dev/null | cut -d \" -f2)"
            "$(hostnamectl 2>/dev/null | grep -i system | cut -d : -f2)"
            "$(lsb_release -ds 2>/dev/null)"
            "$(grep -i description /etc/lsb-release 2>/dev/null | cut -d \" -f2)"
            "$(grep . /etc/redhat-release 2>/dev/null)"
            "$(grep . /etc/issue 2>/dev/null | cut -d \\ -f1 | sed '/^[ ]*$/d')"
            "$(uname 2>/dev/null | grep -i darwin)"
            "$(uname -a 2>/dev/null | grep NAS)"
        )

        REGEX=(
            "debian"
            "ubuntu"
            "centos|kernel|'oracle linux'|alma|rocky"
            "'amazon linux'"
            "alpine"
            "darwin"
            "nas"
        )
        RELEASE=("debian" "ubuntu" "centos" "centos" "alpine" "macos" "nas")
        CO=("" "" "" "amazon" "" "" "")

        for i in "${CMD[@]}"; do
            sys="$i" && [[ -n $sys ]] && break
        done

        for ((i = 0; i < ${#REGEX[@]}; i++)); do
            echo "$sys" | grep -Eiq "${REGEX[i]}" && system="${RELEASE[i]}" && COMPANY="${CO[i]}" && [[ -n $system ]] && break
        done
    fi
}

# 获取配置
# shellcheck disable=SC2034
source_config() {
    check_env
    if [ "${ENV_PATH}" ]; then
        . "$ENV_PATH"
    elif [ "${pannel}" = "elecv2p" ]; then
        . "/usr/local/app/script/Lists/.env"
    elif [ "${pannel}" = "qinglong" ]; then
        . "/ql/config/.env"
    else
        . env
    fi
    # 是否显示上下文 默认是
    if [ "${DISPLAY_CONTEXT}" -eq 0 ]; then
        IS_DISPLAY_CONTEXT=0
    fi
}

# 检查账户权限
check_root() {
    if [ "$(id -u)" -eq 0 ]; then
        printf "当前用户是 ROOT 用户，可以继续操作" && sleep 1
    else
        printf "当前非 ROOT 账号(或没有 ROOT 权限)，无法继续操作，请更换 ROOT 账号或使用 su 命令获取临时 ROOT 权限" && exit 1
    fi
}

# 检查 jq 依赖
check_jq_installed_status() {
    if [ -z "$(command -v jq)" ]; then
        printf "jq 依赖没有安装，开始安装..."
        check_root
        if [ "${pannel}" ]; then
            apk add --no-cache jq
        elif [ "${system}" = "centos" ]; then
            yum update && yum install jq -y
        elif [ "${system}" = "macos" ]; then
            brew install jq
        else
            apt-get update && apt-get install jq -y
        fi
        if [ -z "$(command -v jq)" ]; then
            printf "jq 依赖安装失败，请检查！" && exit 1
        else
            printf "jq 依赖安装成功！"
        fi
    fi
}

# 检查 Java 依赖
check_java_installed_status() {
    if [ -z "$(command -v java)" ]; then
        printf "Java 依赖没有安装，开始安装..."
        check_root
        if [ "${pannel}" ]; then
            apk add --no-cache openjdk8
        fi
        if [ -z "$(command -v java)" ]; then
            printf "Java 依赖安装失败，请检查！" && exit 1
        else
            printf "Java 依赖安装成功！"
        fi
    fi
}
