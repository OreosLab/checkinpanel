#!/usr/bin/env sh

# shellcheck disable=SC2188
<<'COMMENT'
cron: 45 */1 * * *
new Env('JSON5toTOML 工具');
COMMENT

. utils_env.sh
get_some_path

json52toml() {
    if [ -f "${CONF_PATH}/config.sh" ]; then
        sed -i '/^RepoFileExtensions/c RepoFileExtensions="js pl py sh ts"' "${CONF_PATH}/config.sh"
        cp -f "${REPO_PATH}/OreosLab_checkinpanel_master/check.sample.toml" "${CONF_PATH}/check.template.toml"
    fi
    find . -type f -name '*utils_json52toml.pl' -exec perl {} \;
}
json52toml
