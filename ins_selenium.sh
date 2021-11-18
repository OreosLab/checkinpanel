#!/usr/bin/env bash

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

alpine_pkgs="bash curl gcc git jq libffi-dev make musl-dev openssl-dev py3-pip python3 python3-dev wget"
py_reqs="cryptography==3.2.1 selenium PyVirtualDisplay"
chromium_pkgs="chromium libexif eudev"
chromedriver_pkgs="chromium-chromedriver"
xvfb_pkgs="xvfb"
alpine_pkgs="$alpine_pkgs $chromium_pkgs $chromedriver_pkgs $xvfb_pkgs"

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
    apk_info="$(apk info)"
    for i in $alpine_pkgs; do
        if [[ $apk_info == *[[:space:]]${i}[[:space:]]* ]] || [[ $apk_info == ${i}[[:space:]]* ]] || [[ $apk_info == *[[:space:]]${i} ]]; then
            echo "$i 已安装"
        else
            install 0 "apk add $i" "$(apk add --no-cache "$i" | grep -c 'OK')"
        fi
    done
}

install_py_reqs() {
    pip3 install --upgrade pip
    pip3_freeze=$(pip3 freeze)
    for i in $py_reqs; do
        if [[ $pip3_freeze =~ $i ]]; then
            echo "$i 已安装"
        else
            install 0 "pip3 install $i" "$(pip3 install "$i" | grep -c 'Successfully')"
        fi
    done
}

install_alpine_pkgs
install_py_reqs
