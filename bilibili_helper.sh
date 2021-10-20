#!/usr/bin/env bash
#new Env('BILIBILI-HELPER');

if [ -f "$(dirname "$0")/utils_env.sh" ]; then
    source "$(dirname "$0")/utils_env.sh"
else
    wget -q -O utils_env.sh https://ghproxy.com/https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/utils_env.sh
    source "$(dirname "$0")/utils_env.sh"
fi
check_env
check_jq_installed_status
check_java_installed_status

# shellcheck disable=SC2154
if [ "${pannel}" == "qinglong" ]; then
    bili_path="/ql/scripts/bilibili"
    conf_file="/ql/config/java_conf.json"
elif [ "${pannel}" == "elecv2p" ]; then
    bili_path="/usr/local/app/script/Shell/checkinpanel/bilibili"
    conf_file="/usr/local/app/script/Lists/java_conf.json"
fi

if [ ! -d "${bili_path}" ]; then
    mkdir -p "${bili_path}"
fi

cd "${bili_path}" || exit
if [ -f "/tmp/bili-helper.log" ]; then
    VERSION=$(grep "当前版本" "/tmp/bili-helper.log" | awk '{print $2}')
else
    VERSION="0"
fi
echo "当前版本:"$VERSION

latest=$(curl -s https://api.github.com/repos/Oreomeow/bili/releases/latest)
latest_VERSION=$(echo "$latest" | jq '.tag_name' | sed 's/v\|"//g')
echo "最新版本:""$latest_VERSION"
download_url=$(echo "$latest" | jq '.assets[0].browser_download_url' | sed 's/"//g')
download() {
    curl -L -o "./BILIBILI-HELPER.zip" "https://ghproxy.com/$download_url"
    mkdir ./tmp
    echo "正在解压文件......."
    unzip -o -d ./tmp/ BILIBILI-HELPER.zip
    cp -f ./tmp/BILIBILI-HELPER*.jar BILIBILI-HELPER.jar
    if [ ! -f "${conf_file}" ]; then
        echo "配置文件不存在。"
        cp -f ./tmp/config.json "${conf_file}"
    fi
    echo "清除缓存........."
    rm -rf tmp
    rm -rf BILIBILI-HELPER.zip
    echo "更新完成"
}

function version_lt() { test "$(echo "$@" | tr " " "\n" | sort -rV | head -n 1)" != "$1"; }
if version_lt $VERSION "$latest_VERSION"; then
    echo "有新版本，开始更新"
    download
else
    echo "已经是最新版本，不需要更新！！！"
fi
if [ ! -f "${bili_path}/BILIBILI-HELPER.jar" ]; then
    echo "没找到BILIBILI-HELPER.jar，开始下载.........."
    download
fi

echo "配置文件路径:""$conf_file"
java -jar BILIBILI-HELPER.jar "$conf_file"
