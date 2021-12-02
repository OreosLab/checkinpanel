#!/usr/bin/env sh

# shellcheck disable=SC2005,2188
<<'COMMENT'
cron: 16 */2 * * *
new Env('签到依赖');
COMMENT

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

alpine_pkgs="bash curl gcc git jq libffi-dev make musl-dev openssl-dev perl perl-app-cpanminus perl-dev py3-pip python3 python3-dev wget"
py_reqs="bs4 cryptography pyaes pyppeteer requests rsa schedule tomli"
js_pkgs="@iarna/toml axios crypto-js got"
pl_mods="File::Slurp JSON5 TOML::Dumper"

install() {
    count=0
    flag=$1
    while true; do
        echo ".......... $2 begin .........."
        result=$3
        if [ "$result" -gt 0 ]; then
            flag=0
        else
            flag=1
        fi
        if [ $flag -eq "$1" ]; then
            echo "---------- $2 succeed ----------"
            break
        else
            count=$((count + 1))
            if [ $count -eq 6 ]; then
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
    apk_info=" $(apk info) "
    for i in $alpine_pkgs; do
        if expr "$apk_info" : ".*\s${i}\s.*" >/dev/null; then
            echo "$i 已安装"
        else
            install 0 "apk add $i" "$(apk add --no-cache "$i" | grep -c 'OK')"
        fi
    done
}

install_py_reqs() {
    pip3 install --upgrade pip
    pip3_freeze="$(pip3 freeze)"
    for i in $py_reqs; do
        if expr "$pip3_freeze" : ".*${i}" >/dev/null; then
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
    elif [ -d "/ql/scripts" ] && [ ! -f "/ql/scripts/package.bak.json" ]; then
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
    is_empty=$(npm ls "$1" | grep empty)
    has_err=$(npm ls "$1" | grep ERR)
    if [ "$is_empty" = "" ] && [ "$has_err" = "" ]; then
        echo "$1 已正确安装"
    elif [ "$has_err" != "" ]; then
        uninstall_js_pkgs "$1"
    else
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

install_pl_mods() {
    if command -v cpm >/dev/null 2>&1; then
        echo "App::cpm 已安装"
    else
        install 1 "cpanm -fn App::cpm" "$(cpanm -fn App::cpm | grep -c "FAIL")"
        if ! command -v cpm >/dev/null 2>&1; then
            if [ -f ./cpm ]; then
                chmod +x cpm && ./cpm --version
            else
                cp -f /ql/repo/Oreomeow_checkinpanel_master/cpm ./ && chmod +x cpm && ./cpm --version
                if [ ! -f ./cpm ]; then
                    curl -fsSL https://cdn.jsdelivr.net/gh/Oreomeow/checkinpanel/cpm >cpm && chmod +x cpm && ./cpm --version
                fi
            fi
        fi
    fi
    for i in $pl_mods; do
        if [ -f "$(perldoc -l "$i")" ]; then
            echo "$i 已安装"
        else
            install 1 "cpm install -g $i" "$(cpm install -g "$i" | grep -c "FAIL")"
        fi
    done
}

install_alpine_pkgs
install_py_reqs
install_js_pkgs_all
install_pl_mods
