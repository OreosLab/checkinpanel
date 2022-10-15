#!/usr/bin/env sh

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# 初始化变量
V2P_FILE='/usr/local/app/script/Lists/task.list'
QL_FILE='/ql/config/env.sh'
QL_NEW_FILE='/ql/data/config/env.sh'
IS_DISPLAY_CONTEXT=1

# 检查环境：面板先于系统
# shellcheck disable=SC2034
check_env() {
    if [ -f "${V2P_FILE}" ]; then
        panel="elecv2p"
    elif [ -f "${QL_NEW_FILE}" ]; then
        panel="qinglong_new"
    elif [ -f "${QL_FILE}" ]; then
        panel="qinglong"
    else
        CMD="$(grep -i pretty_name /etc/os-release 2>/dev/null | cut -d \" -f2)
        $(hostnamectl 2>/dev/null | grep -i system | cut -d : -f2)
        $(lsb_release -ds 2>/dev/null)
        $(grep -i description /etc/lsb-release 2>/dev/null | cut -d \" -f2)
        $(grep . /etc/redhat-release 2>/dev/null)
        $(grep . /etc/issue 2>/dev/null | cut -d \\ -f1 | sed '/^[ ]*$/d')
        $(uname -a 2>/dev/null)"

        REGEX="debian ubuntu centos|kernel|oracle[[:space:]]*linux|alma|rocky amazon[[:space:]]*linux alpine darwin nas"
        RELEASE="debian ubuntu centos centos alpine macos nas"
        CO="0 0 0 amazon 0 0 0"

        for i in $(echo "$CMD" | tr -d ' ' | tr '\n' ' '); do
            sys="$i" && [ -n "$sys" ] && break
        done

        count1=0
        for a in $REGEX; do
            count1=$((count1 + 1))
            count2=0
            for b in $RELEASE; do
                count2=$((count2 + 1))
                [ $count2 -eq $count1 ] || continue
                count3=0
                for c in $CO; do
                    count3=$((count3 + 1))
                    [ $count3 -eq $count2 ] || continue
                    echo "$sys" | grep -Eiq "$a" && system="$b" && company="$c" && [ -n "$system" ] || break 2 && break 3
                done
            done
        done

    fi
}

# 获取配置
# shellcheck disable=SC2034
source_config() {
    check_env
    if [ "${ENV_PATH}" ]; then
        ENV_FILE=$ENV_PATH
    elif [ "${panel}" = "elecv2p" ]; then
        ENV_FILE="/usr/local/app/script/Lists/.env"
    elif [ "${panel}" = "qinglong_new" ]; then
        ENV_FILE="/ql/data/config/.env"
    elif [ "${panel}" = "qinglong" ]; then
        ENV_FILE="/ql/config/.env"
    else
        ENV_FILE=".env"
    fi

    if [ -f "${ENV_FILE}" ]; then
        . "${ENV_FILE}"
    else
        printf "%s 不存在，请检查，若配置过环境变量的可以忽略\n" "${ENV_FILE}" && return 1
    fi

    # 是否显示上下文 默认是
    if [ "${DISPLAY_CONTEXT}" -eq 0 ]; then
        IS_DISPLAY_CONTEXT=0
    fi
}

# 获取 config/script 目录路径
# shellcheck disable=SC2034
get_some_path() {
    check_env
    if [ "${panel}" = "elecv2p" ]; then
        SCR_PATH="/usr/local/app/script/Shell"
        CONF_PATH="/usr/local/app/script/Lists"
    elif [ "${panel}" = "qinglong_new" ]; then
        SCR_PATH="/ql/data/scripts"
        CONF_PATH="/ql/data/config"
        REPO_PATH="/ql/data/repo"
    elif [ "${panel}" = "qinglong" ]; then
        SCR_PATH="/ql/scripts"
        CONF_PATH="/ql/config"
        REPO_PATH="/ql/repo"
    else
        SCR_PATH="."
        CONF_PATH="."
    fi
}

# 检查账户权限
check_root() {
    if [ "$(id -u)" -eq 0 ]; then
        printf "当前用户是 ROOT 用户，可以继续操作\n" && sleep 1
    else
        printf "当前非 ROOT 账号(或没有 ROOT 权限)，无法继续操作，请更换 ROOT 账号或使用 su 命令获取临时 ROOT 权限\n" && exit 1
    fi
}

# 检查 jq 依赖
check_jq_installed_status() {
    if [ -z "$(command -v jq)" ]; then
        printf "jq 依赖没有安装，开始安装...\n"
        check_root
        if [ "${panel}" ]; then
            apk add --no-cache jq
        elif [ "${system}" = "centos" ]; then
            yum update && yum install jq -y
        elif [ "${system}" = "macos" ]; then
            brew install jq
        else
            apt-get update && apt-get install jq -y
        fi
        if [ -z "$(command -v jq)" ]; then
            printf "jq 依赖安装失败，请检查！\n" && exit 1
        else
            printf "jq 依赖安装成功！\n"
        fi
    fi
}

# 检查 Java 依赖
check_java_installed_status() {
    if [ -z "$(command -v java)" ]; then
        printf "Java 依赖没有安装，开始安装...\n"
        check_root
        if [ "${panel}" ]; then
            apk add --no-cache openjdk8
        fi
        if [ -z "$(command -v java)" ]; then
            printf "Java 依赖安装失败，请检查！\n" && exit 1
        else
            printf "Java 依赖安装成功！\n"
        fi
    fi
}
