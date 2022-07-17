#!/usr/bin/env sh

# shellcheck disable=SC2188
<<'COMMENT'
cron: 45 12 */7 * *
new Env('国内加速');
COMMENT

# alpine 换源
sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# Python 换源
mkdir -p /root/.config/pip
cat >/root/.config/pip/pip.conf <<EOF
[global]                                                                                                                             
index-url=https://pypi.mirrors.ustc.edu.cn/simple/
EOF

# NPM 换源
npm config set registry https://registry.npmmirror.com/

# CPAN 换源
if ! (
    perl -MCPAN -e 'CPAN::HandleConfig->load();' \
        -e 'CPAN::HandleConfig->prettyprint("urllist")' |
        grep -qF 'https://mirrors.tuna.tsinghua.edu.cn/CPAN/'
); then
    echo "Yes" | perl -MCPAN -e 'CPAN::HandleConfig->load();' \
        -e 'CPAN::HandleConfig->edit("urllist", "unshift", "https://mirrors.tuna.tsinghua.edu.cn/CPAN/");' \
        -e 'CPAN::HandleConfig->commit()'
fi
