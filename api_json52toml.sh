#!/usr/bin/env sh

# shellcheck disable=SC2188
<<'COMMENT'
cron: 45 0-23/1 * * *
new Env('JSON5toTOML 工具');
COMMENT

json52toml() {
    if [ -f "/ql/config/config.sh" ]; then
        sed -i '/^RepoFileExtensions/c RepoFileExtensions="js pl py sh ts"' /ql/config/config.sh
        cp -f /ql/repo/Oreomeow_checkinpanel_master/check.sample.toml /ql/config/check.template.toml
    fi
    find . -type f -name '*utils_json52toml.pl' -exec perl {} \;
}
json52toml
