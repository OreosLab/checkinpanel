#!/bin/bash

<<'COMMENT'
cron: 26 10 * * *
new Env('SSPanel 签到');
环境变量说明
SS_USERS: https://abc.com----abc@abc.com----abc123456;   用户组，格式为 签到站点----用户名----密码，多个站点或用户使用 ; 分隔
PUSH_KEY: SCxxxxxxxxxxxxx                                微信推送，填写自己申请 Server 酱(http://sc.ftqq.com/?c=code) 的 SCKEY         
PUSH_TURBO_KEY: xxxxxxxxxxxxxxx                          企业微信推送，填写自己申请 Server 酱 Turbo(https://sct.ftqq.com/sendkey) 的 SendKey
QMSG_KEY: e6fxxxxxxxxxxxx                                QQ 推送，填写自己申请 Qmsg 酱(https://qmsg.zendee.cn/me.html#/) 的 QMSG_KEY
DD_BOT_TOKEN: a1bxxxxxxxxxxxx                            钉钉机器人推送，填写申请自定义机器人接入申请的回调地址中 access_token 的值
TG_BOT_TOKEN: 123456:ABC-DEF1234xxx-xxx123ew11           TGBot 推送，填写自己向 @BotFather(https://t.me/BotFather) 申请的 Bot Token
TG_USER_ID: 11xxxxxx03                                   TGBot 推送，填写 @getuseridbot(https://t.me/getuseridbot) 私聊获取到的纯数字 ID
PUSH_PLUS_TOKEN: xxxxxxxxxxxxxxxx                        PUSHPLUS 推送，填写申请的 pushplus(https://pushplus.hxtrip.com/) TOKEN
CORPID: xxxxxx                                           企业微信 ID，填写注册的企业微信 ID
AGENTID: 100001                                          企业微信应用 ID，填写申请应用的 ID
CORPSECRET: xxxxxxxxxxxxxxx                              企业微信对应的 SECRET
DISPLAY_CONTEXT: 1                                       任务执行时是否显示详细信息，1 显示 0 关闭，默认值 1
COMMENT

PATH="/usr/local/bin:/usr/bin:/bin"

#版本、初始化变量
VERSION="2.2.2"
ENV_PATH="$(dirname $0)/.env"
IS_MACOS=$(uname | grep 'Darwin' | wc -l)
IS_DISPLAY_CONTEXT=1
TITLE="🚀SSPanel Auto Checkin v${VERSION}"
users_array=""
log_text=""
COOKIE_PATH="./.ss-autocheckin.cook"
PUSH_TMP_PATH="./.ss-autocheckin.tmp"

# 本地模式
if [ -f ${ENV_PATH} ]; then
    source ${ENV_PATH}
fi

# 加载用户组配置
users_array=($(echo ${SS_USERS} | tr ';' ' '))

# 是否显示上下文 默认是
if [ "${DISPLAY_CONTEXT}" == "0" ]; then
    IS_DISPLAY_CONTEXT=0
fi

#检查账户权限
check_root() {
    if [ 0 == $UID ]; then
        echo -e "当前用户是 ROOT 用户，可以继续操作" && sleep 1
    else
        echo -e "当前非 ROOT 账号(或没有 ROOT 权限)，无法继续操作，请更换 ROOT 账号或使用 su命令获取临时 ROOT 权限" && exit 1
    fi
}

#检查系统
check_sys() {
    if [[ -f /etc/redhat-release ]]; then
        release="centos"
    elif [ ${IS_MACOS} -eq 1 ]; then
        release="macos"
    elif cat /etc/issue | grep -q -E -i "debian"; then
        release="debian"
    elif cat /etc/issue | grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    elif cat /proc/version | grep -q -E -i "debian"; then
        release="debian"
    elif cat /proc/version | grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    fi
}

#检查 jq 依赖
check_jq_installed_status() {
    if [ -z $(command -v jq) ]; then
        echo -e "jq 依赖没有安装，开始安装..."
        check_root
        if [[ ${release} == "centos" ]]; then
            yum update && yum install jq -y
        elif [[ ${release} == "macos" ]]; then
            brew install jq
        else
            apt-get update && apt-get install jq -y
        fi
        if [ -z $(command -v jq) ]; then
            echo -e "jq 依赖安装失败，请检查！" && exit 1
        else
            echo -e "jq 依赖安装成功！"
        fi
    fi
}

#消息推送
send_message() {
    echo -e "\n通知结果:"
    # Server 酱通知
    if [ "${PUSH_KEY}" ]; then
        echo -e "text=${TITLE}&desp=${log_text}" >${PUSH_TMP_PATH}
        push=$(curl -k -s --data-binary @${PUSH_TMP_PATH} "https://sc.ftqq.com/${PUSH_KEY}.send")
        push_code=$(echo ${push} | jq -r ".errno" 2>&1)
        if [ ${push_code} -eq 0 ]; then
            echo -e "Server 酱推送结果: 成功"
        else
            echo -e "Server 酱推送结果: 失败"
        fi
    fi

    # Server 酱 Turbo 通知
    if [ "${PUSH_TURBO_KEY}" ]; then
        echo -e "text=${TITLE}&desp=${log_text}" >${PUSH_TMP_PATH}
        push=$(curl -k -s -X POST --data-binary @${PUSH_TMP_PATH} "https://sctapi.ftqq.com/${PUSH_TURBO_KEY}.send")
        ###
        # push 成功后，获取相关查询参数
        ### 

        push_code=$(echo ${push} | jq -r ".data.errno" 2>&1)
        push_id=$(echo ${push} | jq -r ".data.pushid" 2>&1)
        push_readkey=$(echo ${push} | jq -r ".data.readkey" 2>&1)
        
        ###
        # 企业微信推送逻辑修改
        # 先放入队列，push_code 为 0 代表放入队列成功不代表推送成功
        ###

        if [ "${push_code} -eq 0" ]; then
            echo -e "Server 酱Turbo 队列结果: 成功"
            
            ###
            # 推送结果需要异步查询
            # 目前每隔两秒查询一次，轮询 10 次检查推送结果
            ###

            i=1
            while [ $i -le 10 ]; do
                wx_status=$(curl -s "https://sctapi.ftqq.com/push?id=${push_id}&readkey=${push_readkey}")
                wx_result=$(echo ${wx_status} | jq -r ".data.wxstatus" 2>&1 | sed 's/\"{/{/g'| sed 's/\}"/}/g' | sed 's/\\"/"/g') 
                if [ "${wx_result}" ]; then
                    wx_errcode=$(echo ${wx_result} | jq -r ".errcode" 2>&1)
                    if [ "${wx_errcode} -eq 0" ]; then
                        echo -e "Server 酱Turbo 推送结果: 成功"
                    else
                        echo -e "Server 酱Turbo 推送结果: 失败，错误码:"${wx_errcode}",more info at https:\\open.work.weixin.qq.com\devtool"
                    fi
                    break
                else
                    if [ $i -lt 10 ]; then
                        let 'i++'
                        Sleep 2s
                    else
                        echo -e "Server 酱Turbo 推送结果: 检查超时，请自行确认结果"
                    fi

                fi

            done
        else
            echo -e "Server 酱Turbo 队列结果: 失败"
        fi
    fi

    # 钉钉群机器人通知
    if [ "${DD_BOT_TOKEN}" ]; then
        push=$(curl -k -s "https://oapi.dingtalk.com/robot/send?access_token=${DD_BOT_TOKEN}" \
        -H 'Content-Type: application/json' \
        -d "{
            \"msgtype\": \"markdown\",
            \"markdown\": {
                \"title\":\"${TITLE}\",
                \"text\": \"${log_text}\"
            }
        }")
        push_code=$(echo ${push} | jq -r ".errcode" 2>&1)
        if [ "${push_code}" -eq 0 ]; then
            echo -e "钉钉机器人推送结果: 成功"
        else
            echo -e "钉钉机器人推送结果: 失败"
        fi
    fi


    # Qmsg 酱通知
    if [ "${QMSG_KEY}" ]; then
        result_qmsg_log_text="${TITLE}${log_text}"
        echo -e "msg=${result_qmsg_log_text}" >${PUSH_TMP_PATH}
        push=$(curl -k -s --data-binary @${PUSH_TMP_PATH} "https://qmsg.zendee.cn/send/${QMSG_KEY}")
        push_code=$(echo ${push} | jq -r ".success" 2>&1)
        if [ "${push_code}" == "true" ]; then
            echo -e "Qmsg 酱推送结果: 成功"
        else
            echo -e "Qmsg 酱推送结果: 失败"
        fi
    fi

    # TelegramBot 通知
    if [ "${TG_BOT_TOKEN}" ] && [ "${TG_USER_ID}" ]; then
        result_tgbot_log_text="${TITLE}${log_text}"
        echo -e "chat_id=${TG_USER_ID}&parse_mode=Markdown&text=${result_tgbot_log_text}" >${PUSH_TMP_PATH}
        push=$(curl -k -s --data-binary @${PUSH_TMP_PATH} "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage")
        push_code=$(echo ${push} | grep -o '"ok":true')
        if [ ${push_code} ]; then
            echo -e "TelegramBot 推送结果: 成功"
        else
            echo -e "TelegramBot 推送结果: 失败"
        fi
    fi

    # PushPlus 通知
    if [ "${PUSH_PLUS_TOKEN}" ]; then
        echo -e "token=${PUSH_PLUS_TOKEN}&title=${TITLE}&content=${log_text}" >${PUSH_TMP_PATH}
        push=$(curl -k -s --data-binary @${PUSH_TMP_PATH} "http://pushplus.hxtrip.com/send")
        push_code=$(echo ${push} | jq -r ".code" 2>&1)
        if [ ${push_code} -eq 200 ]; then
            echo -e "PushPlus 推送结果: 成功"
        else
            echo -e "PushPlus 推送结果: 失败"
        fi
    fi

    # 企业微信通知
    if [ "${CORPID}" ] && [ "${AGENTID}" ] && [ "${CORPSECRET}" ]; then
        # 获取 token
        token=$(curl -k -s -G "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${CORPID}&corpsecret=${CORPSECRET}")
        access_token=$(echo ${token} | jq -r ".access_token" 2>&1)

        if [ "${access_token}" ]; then
            result_wework_log_text="${TITLE}${log_text}"
            push=$(curl -k -s "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${access_token}" \
            -H 'Content-Type: application/json' \
            -d "{
                \"touser\": \"@all\",
                \"msgtype\": \"text\",
                \"agentid\": \"${AGENTID}\",
                \"text\": {
                    \"content\":\"${result_wework_log_text}\"
                }
            }")
            push_code=$(echo ${push} | jq -r ".errcode" 2>&1)
            if [ "${push_code}" -eq 0 ]; then
                echo -e "企业微信推送结果: 成功"
            else
                echo -e "企业微信推送结果: 失败"
            fi
        else
            echo -e "企业微信推送结果: 失败 原因: token 获取失败"
        fi
    fi
}

#签到
ssp_autochenkin() {
    echo -e "${TITLE}"
    if [ "${users_array}" ]; then
        user_count=1
        for user in ${users_array[@]}; do
            domain=$(echo ${user} | awk -F'----' '{print $1}')
            username=$(echo ${user} | awk -F'----' '{print $2}')
            passwd=$(echo ${user} | awk -F'----' '{print $3}')

            # 邮箱、域名脱敏处理
            username_prefix="${username%%@*}"
            username_suffix="${username#*@}"
            username_root="${username_suffix#*.}"
            username_text="${username_prefix:0:2}🙈@${username_suffix:0:2}🙈.${username_root}"

            domain_protocol="${domain%%://*}"
            domain_context="${domain##*//}"
            domain_root="${domain##*.}"
            domain_text="${domain_protocol}://${domain_context:0:2}🙈.${domain_root}"

            if [ -z "${domain}" ] || [ -z "${username}" ] || [ -z "${passwd}" ]; then
                echo "账号信息配置异常，请检查配置" && exit 1
            fi

            login=$(curl "${domain}/auth/login" -d "email=${username}&passwd=${passwd}&code=" -c ${COOKIE_PATH} -L -k -s)

            start_time=$(date '+%Y-%m-%d %H:%M:%S')
            login_code=$(echo ${login} | jq -r '.ret' 2>&1)
            login_status=$(echo ${login} | jq -r '.msg' 2>&1)

            login_log_text="\n用户 ${user_count}\n"
            login_log_text="${login_log_text}签到站点: ${domain_text}\n"
            login_log_text="${login_log_text}签到用户: ${username_text}\n"
            login_log_text="${login_log_text}签到时间: ${start_time}\n"

            if [ "${login_code}" == "1" ]; then
                userinfo=$(curl -k -s -G -b ${COOKIE_PATH} "${domain}/getuserinfo")
                user=$(echo ${userinfo} | tr '\r\n' ' ' | jq -r ".info.user" 2>&1)

                if [ "${user}" ]; then
                    # 用户等级
                    clasx=$(echo ${user} | jq -r ".class" 2>&1)
                    # 等级过期时间
                    class_expire=$(echo ${user} | jq -r ".class_expire" 2>&1)
                    # 账户过期时间
                    expire_in=$(echo ${user} | jq -r ".expire_in" 2>&1)
                    # 上次签到时间
                    last_check_in_time=$(echo ${user} | jq -r ".last_check_in_time" 2>&1)
                    # 用户余额
                    money=$(echo ${user} | jq -r ".money" 2>&1)
                    # 用户限速
                    node_speedlimit=$(echo ${user} | jq -r ".node_speedlimit" 2>&1)
                    # 总流量
                    transfer_enable=$(echo ${user} | jq -r ".transfer_enable" 2>&1)
                    # 总共使用流量
                    last_day_t=$(echo ${user} | jq -r ".last_day_t" 2>&1)
                    # 剩余流量
                    transfer_used=$(expr ${transfer_enable} - ${last_day_t})
                    # 转换 GB
                    transfer_enable_text=$(echo ${transfer_enable} | awk '{ byte =$1 /1024/1024**2 ; print byte " GB" }')
                    last_day_t_text=$(echo ${last_day_t} | awk '{ byte =$1 /1024/1024**2 ; print byte " GB" }')
                    transfer_used_text=$(echo ${transfer_used} | awk '{ byte =$1 /1024/1024**2 ; print byte " GB" }')
                    # 转换上次签到时间
                    if [ ${IS_MACOS} -eq 0 ]; then
                        last_check_in_time_text=$(date -d "1970-01-01 UTC ${last_check_in_time} seconds" "+%F %T")
                    else
                        last_check_in_time_text=$(date -r ${last_check_in_time} '+%Y-%m-%d %H:%M:%S')
                    fi

                    user_log_text="\n用户等级: VIP${clasx}\n"
                    user_log_text="${user_log_text}用户余额: ${money} CNY\n"
                    user_log_text="${user_log_text}用户限速: ${node_speedlimit} Mbps\n"
                    user_log_text="${user_log_text}总流量: ${transfer_enable_text}\n"
                    user_log_text="${user_log_text}剩余流量: ${transfer_used_text}\n"
                    user_log_text="${user_log_text}已使用流量: ${last_day_t_text}\n"
                    user_log_text="${user_log_text}等级过期时间: ${class_expire}\n"
                    user_log_text="${user_log_text}账户过期时间: ${expire_in}\n"
                    user_log_text="${user_log_text}上次签到时间: ${last_check_in_time_text}"
                else
                    user_log_text=""
                fi

                checkin=$(curl -k -s -d "" -b ${COOKIE_PATH} "${domain}/user/checkin")
                chechin_code=$(echo ${checkin} | jq -r ".ret" 2>&1)
                checkin_status=$(echo ${checkin} | jq -r ".msg" 2>&1)

                if [ "${checkin_status}" ]; then
                    checkin_log_text="签到状态: ${checkin_status}"
                else
                    checkin_log_text="签到状态: 签到失败, 请检查是否存在签到验证码"
                fi

                result_log_text="${login_log_text}${checkin_log_text}${user_log_text}"
            else

                result_log_text="${login_log_text}签到状态: 登录失败, 请检查配置"
            fi

            if [ ${IS_DISPLAY_CONTEXT} == 1 ]; then
                echo -e ${result_log_text}
            else 
                echo -e "\nHidden the logs, please view notify messages."
            fi

            log_text="${log_text}\n${result_log_text}"

            user_count=$(expr ${user_count} + 1)
        done

        log_text="${log_text}\n\n免费使用自: https://github.com/isecret/sspanel-autocheckin\n适配青龙自: Oreo"

        send_message

        rm -rf ${COOKIE_PATH}
        rm -rf ${PUSH_TMP_PATH}
    else
        echo "用户组环境变量未配置" && exit 1
    fi
}

check_sys
check_jq_installed_status
ssp_autochenkin
