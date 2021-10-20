#!/usr/bin/env bash

# shellcheck disable=SC2188
<<'COMMENT'
cron: 16 */2 * * *
new Env('签到依赖');
COMMENT

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

alpine_pkgs="bash curl gcc git jq libffi-dev musl-dev openssl-dev python3 python3-dev py3-pip"
py_reqs="bs4 cryptography==3.2.1 json5 requests rsa"
js_pkgs="axios got json5 request"

install() {
    count=0
    flag=0
    while true; do
        echo ".......... $1 begin .........."
        result=$2
        if [[ $3 ]]; then
            flag=0
        else
            flag=1
        fi
        if [ $flag -eq 0 ]; then
            echo "---------- $1 succeed ----------"
            break
        else
            count=$((count + 1))
            if [ ${count} -eq 6 ]; then
                echo "!! 自动安装失败，请尝试进入容器后执行 $4 !!"
                break
            fi
            echo ".......... retry in 5 seconds .........."
            sleep 5
        fi
    done
}

install_alpine_pkgs() {
    apk update
    for i in $alpine_pkgs; do
        if [[ $(apk info | grep "^$i$") = "$i" ]]; then
            echo "$i 已安装"
        else
            install "apk add $i" "$(apk add --no-cache "$i")" "$result =~ OK" "apk add $i"
        fi
    done
}

install_py_reqs() {
    for i in $py_reqs; do
        if [[ "$(pip3 freeze)" =~ $i ]]; then
            echo "$i 已安装"
        else
            install "pip3 install $i" "$(pip3 install "$i")" "$result =~ Successfully" "pip3 install $i"
        fi
    done
}

install_js_pkgs() {
    for i in $js_pkgs; do
        if [[ "$(npm ls "$i")" =~ $i ]]; then
            echo "$i 已安装"
        else
            if [ -d "/ql/scripts" ]; then
                install "npm install $i" "$(npm install "$i" --force)" "$(npm ls "$i") =~ $i" "cd /ql/scripts && npm install $i"
            else
                npm install
                break
            fi
        fi
    done
}

install_alpine_pkgs
install_py_reqs
install_js_pkgs
