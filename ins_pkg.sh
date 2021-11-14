#!/usr/bin/env bash

# shellcheck disable=SC2005,2188
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
    flag=$1
    while true; do
        echo ".......... $2 begin .........."
        result=$3
        if ((result > 0)); then
            flag=0
        else
            flag=1
        fi
        if ((flag == $1)); then
            echo "---------- $2 succeed ----------"
            break
        else
            count=$((count + 1))
            if ((count == 6)); then
                echo "!! 自动安装失败，请尝试进入容器后执行 $2 !!"
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
            install 0 "apk add $i" "$(apk add --no-cache "$i" | grep -c 'OK')"
        fi
    done
}

install_py_reqs() {
    pip3 install --upgrade pip
    for i in $py_reqs; do
        if [[ $(pip3 freeze) =~ $i ]]; then
            echo "$i 已安装"
        else
            install 0 "pip3 install $i" "$(pip3 install "$i" | grep -c 'Successfully')"
        fi
    done
}

install_js_pkgs_initial() {
    if [ -d "/ql/scripts/Oreomeow_checkinpanel_master" ]; then
        cd /ql/scripts/Oreomeow_checkinpanel_master &&
            cp /ql/repo/Oreomeow_checkinpanel_master/package.json /ql/scripts/Oreomeow_checkinpanel_master/package.json
    elif [[ -d "/ql/scripts" && ! -f "/ql/scripts/package.bak.json" ]]; then
        cd /ql/scripts || exit
        rm -rf node_modules
        rm -rf .pnpm-store
        mv package-lock.json package-lock.bak.json
        mv package.json package.bak.json
        mv pnpm-lock.yaml pnpm-lock.bak.yaml
        install 1 "npm install -g package-merge" "$(echo "$(npm install -g package-merge && npm ls -g package-merge)" | grep -cE '(empty)|ERR')" &&
            export NODE_PATH="/usr/local/lib/node_modules" &&
            node -e \
                "const merge = require('package-merge');
                 const fs = require('fs');
                 const dst = fs.readFileSync('/ql/repo/Oreomeow_checkinpanel_master/package.json');
                 const src = fs.readFileSync('/ql/scripts/package.bak.json');
                 fs.writeFile('/ql/scripts/package.json', merge(dst, src), function (err) {
                     if (err) {
                         console.log(err);
                     }
                     console.log('package.json merged successfully!');
                 });"
    fi
    npm install
}
install_js_pkgs_each() {
    npm_ls="$(npm ls "$1")"
    has_err=$(echo "$npm_ls" | grep ERR)
    if [[ $npm_ls =~ $1 && $has_err == "" ]]; then
        echo "$1 已正确安装"
    elif [[ $npm_ls =~ $1 && $has_err != "" ]]; then
        uninstall_js_pkgs "$1"
    elif [[ $npm_ls =~ (empty) ]]; then
        install 1 "npm install $1" "$(echo "$(npm install --force "$1" && npm ls --force "$1")" | grep -cE '(empty)|ERR')"
    fi
}
uninstall_js_pkgs() {
    npm uninstall "$1"
    rm -rf "$(pwd)"/node_modules/"$1"
    rm -rf /usr/local/lib/node_modules/lodash/*
    npm cache clear --force
}
install_js_pkgs_all() {
    install_js_pkgs_initial
    for i in $js_pkgs; do
        install_js_pkgs_each "$i"
    done
    npm ls --depth 0
}

install_alpine_pkgs
install_py_reqs
install_js_pkgs_all
