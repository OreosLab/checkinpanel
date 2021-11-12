#!/usr/bin/env bash

# shellcheck disable=SC2034,2188
<<'COMMENT'
cron: 16 */2 * * *
new Env('签到依赖');
COMMENT

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

alpine_pkgs="bash curl gcc git jq libffi-dev musl-dev openssl-dev python3 python3-dev py3-pip"
py_reqs="bs4 cryptography==3.2.1 json5 pyaes requests rsa"
js_pkgs="axios crypto-js got json5 request"

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
    pip3 install --upgrade pip
    for i in $py_reqs; do
        if [[ "$(pip3 freeze)" =~ $i ]]; then
            echo "$i 已安装"
        else
            install "pip3 install $i" "$(pip3 install "$i")" "$result =~ Successfully" "pip3 install $i"
        fi
    done
}

install_js_pkgs_initial() {
    if [ -d "/ql/scripts/Oreomeow_checkinpanel_master" ]; then
        cd /ql/scripts/Oreomeow_checkinpanel_master &&
            cp /ql/repo/Oreomeow_checkinpanel_master/package.json /ql/scripts/Oreomeow_checkinpanel/package.json &&
            npm install
    elif [ -d "/ql/scripts" ]; then
        cd /ql/scripts || exit
    else
        npm install
    fi

}
install_js_pkgs() {
    if [[ "$(npm ls "$1")" =~ $1 && $(npm ls "$1" | grep ERR) == '' ]]; then
        echo "$1 已正确安装"
    elif [[ "$(npm ls "$1")" =~ $1 && $(npm ls "$1" | grep ERR) != '' ]]; then
        uninstall_js_pkgs "$1"
    elif [[ "$(npm ls "$i" -g)" =~ (empty) ]]; then
        install "npm install $1" "$(npm install "$1" --save)" "$(npm ls "$1") =~ $1 && $(npm ls "$1" | grep ERR) == ''" "npm install $1 --force"
    fi
}
uninstall_js_pkgs() {
    npm uninstall "$1"
    rm -rf "$(pwd)"/node_modules/"$1"
    rm -rf /usr/local/lib/node_modules/lodash/*
}
install_js_pkgs_all() {
    install_js_pkgs_initial
    for i in $js_pkgs; do
        install_js_pkgs "$i"
    done
    npm ls --depth 0
}

install_alpine_pkgs
install_py_reqs
install_js_pkgs_all
