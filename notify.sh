#!/usr/bin/env sh

# shellcheck disable=SC2154
send_message() {
    printf "\n通知结果："

    # 钉钉群机器人通知
    if [ "${DD_BOT_TOKEN}" ]; then
        push=$(curl -k -s "https://oapi.dingtalk.com/robot/send?access_token=${DD_BOT_TOKEN}" \
            -H 'Content-Type：application/json' \
            -d "{
            \"msgtype\"：\"markdown\",
            \"markdown\"：{
                \"title\":\"${TITLE}\",
                \"text\"：\"${log_text}\"
            }
        }")
        push_code=$(echo "${push}" | jq -r ".errcode" 2>&1)
        if [ "${push_code}" -eq 0 ]; then
            printf "钉钉机器人推送结果：成功"
        else
            printf "钉钉机器人推送结果：失败"
        fi
    fi

    # Server 酱通知
    if [ "${PUSH_KEY}" ]; then
        printf "text=%s&desp=%s" "${TITLE}" "${log_text}" >"${PUSH_TMP_PATH}"
        push=$(curl -k -s --data-binary @"${PUSH_TMP_PATH}" "https://sc.ftqq.com/${PUSH_KEY}.send")
        push_code=$(echo "${push}" | jq -r ".errno" 2>&1)
        if [ "${push_code}" -eq 0 ]; then
            printf "Server 酱推送结果：成功"
        else
            printf "Server 酱推送结果：失败"
        fi
    fi

    # Server 酱 Turbo 通知
    if [ "${PUSH_TURBO_KEY}" ]; then
        printf "text=%s&desp=%s" "${TITLE}" "${log_text}" >"${PUSH_TMP_PATH}"
        push=$(curl -k -s -X POST --data-binary @"${PUSH_TMP_PATH}" "https://sctapi.ftqq.com/${PUSH_TURBO_KEY}.send")
        ###############################
        # push 成功后，获取相关查询参数
        ###############################

        push_code=$(echo "${push}" | jq -r ".data.errno" 2>&1)
        push_id=$(echo "${push}" | jq -r ".data.pushid" 2>&1)
        push_readkey=$(echo "${push}" | jq -r ".data.readkey" 2>&1)

        ########################################################
        # 企业微信推送逻辑修改
        # 先放入队列，push_code 为 0 代表放入队列成功不代表推送成功
        ########################################################

        if [ "${push_code}" -eq 0 ]; then
            printf "Server 酱 Turbo 队列结果：成功"

            ############################################
            # 推送结果需要异步查询
            # 目前每隔两秒查询一次，轮询 10 次检查推送结果
            ############################################

            i=1
            while [ $i -le 10 ]; do
                wx_status=$(curl -s "https://sctapi.ftqq.com/push?id=${push_id}&readkey=${push_readkey}")
                wx_result=$(echo "${wx_status}" | jq -r ".data.wxstatus" 2>&1 | sed 's/\"{/{/g' | sed 's/\}"/}/g' | sed 's/\\"/"/g')
                if [ "${wx_result}" ]; then
                    wx_errcode=$(echo "${wx_result}" | jq -r ".errcode" 2>&1)
                    if [ "${wx_errcode}" -eq 0 ]; then
                        printf "Server 酱 Turbo 推送结果：成功"
                    else
                        printf "Server 酱 Turbo 推送结果：失败，错误码:%s, more info at https://open.work.weixin.qq.com/devtool" "${wx_errcode}"
                    fi
                    break
                else
                    if [ $i -lt 10 ]; then
                        i=$((i + 1))
                        Sleep 2s
                    else
                        printf "Server 酱Turbo 推送结果：检查超时，请自行确认结果"
                    fi

                fi

            done
        else
            printf "Server 酱Turbo 队列结果：失败"
        fi
    fi

    # PushPlus 通知
    if [ "${PUSH_PLUS_TOKEN}" ]; then
        printf "token=%s&title=%s&content=%s" "${PUSH_PLUS_TOKEN}" "${TITLE}" "${log_text}" >"${PUSH_TMP_PATH}"
        push=$(curl -k -s --data-binary @"${PUSH_TMP_PATH}" "http://www.pushplus.plus/send")
        push_code=$(echo "${push}" | jq -r ".code" 2>&1)
        if [ "${push_code}" -eq 200 ]; then
            printf "PushPlus 推送结果：成功"
        else
            push=$(curl -k -s --data-binary @"${PUSH_TMP_PATH}" "http://pushplus.hxtrip.com/send")
            push_code=$(echo "${push}" | jq -r ".code" 2>&1)
            if [ "${push_code}" -eq 200 ]; then
                printf "PushPlus(hxtrip) 推送结果：成功"
            else
                printf "PushPlus 推送结果：失败"
            fi
        fi
    fi

    # Qmsg 酱通知
    if [ "${QMSG_KEY}" ]; then
        result_qmsg_log_text="${TITLE}${log_text}"
        printf "msg=%s" "${result_qmsg_log_text}" >"${PUSH_TMP_PATH}"
        push=$(curl -k -s --data-binary @"${PUSH_TMP_PATH}" "https://qmsg.zendee.cn/send/${QMSG_KEY}")
        push_code=$(echo "${push}" | jq -r ".success" 2>&1)
        if [ "${push_code}" = "true" ]; then
            printf "Qmsg 酱推送结果：成功"
        else
            printf "Qmsg 酱推送结果：失败"
        fi
    fi

    # 企业微信通知
    if [ "${CORPID}" ] && [ "${AGENTID}" ] && [ "${CORPSECRET}" ]; then
        # 获取 token
        token=$(curl -k -s -G "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${CORPID}&corpsecret=${CORPSECRET}")
        access_token=$(echo "${token}" | jq -r ".access_token" 2>&1)

        if [ "${access_token}" ]; then
            result_wework_log_text="${TITLE}${log_text}"
            push=$(curl -k -s "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${access_token}" \
                -H 'Content-Type：application/json' \
                -d "{
                \"touser\"：\"@all\",
                \"msgtype\"：\"text\",
                \"agentid\"：\"${AGENTID}\",
                \"text\"：{
                    \"content\":\"${result_wework_log_text}\"
                }
            }")
            push_code=$(echo "${push}" | jq -r ".errcode" 2>&1)
            if [ "${push_code}" -eq 0 ]; then
                printf "企业微信推送结果：成功"
            else
                printf "企业微信推送结果：失败"
            fi
        else
            printf "企业微信推送结果：失败 原因：token 获取失败"
        fi
    fi

    # SRE24.com 通知
    if [ "${SRE_TOKEN}" ]; then
        result_sre24_log_text="${TITLE}${log_text}"
        push=$(curl -k -sL https://push.jwks123.cn/to/ \
            -d "{\"token\":\"${token}\",\"msg\":\"${result_sre24_log_text}\"}")
        push_code=$(echo "${push}" | jq -r ".code" 2>&1)
        if [ "${push_code}" -eq 202 ]; then
            printf "SRE24.com 推送结果：成功"
        else
            printf "SRE24.com 推送结果：失败"
        fi
    fi

    # TelegramBot 通知
    if [ "${TG_BOT_TOKEN}" ] && [ "${TG_USER_ID}" ]; then
        result_tgbot_log_text="${TITLE}${log_text}"
        printf "chat_id=%s&parse_mode=Markdown&text=%s" "${TG_USER_ID}" "${result_tgbot_log_text}" >"${PUSH_TMP_PATH}"
        push=$(curl -k -s --data-binary @"${PUSH_TMP_PATH}" "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage")
        push_code=$(echo "${push}" | grep -o '"ok":true')
        if [ "${push_code}" ]; then
            printf "TelegramBot 推送结果：成功"
        else
            printf "TelegramBot 推送结果：失败"
        fi
    fi
}
