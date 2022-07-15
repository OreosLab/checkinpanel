// @grant nodejs
let jsname = $env.JSNAME;
console.log(`⏳ 开始执行 ${jsname}`);
$exec(`node ${jsname}`, {
    cwd: 'script/Shell/checkinpanel',
    timeout: 0,
    // prettier-ignore
    env: {
        NODE_PATH: "/usr/local/lib/node_modules",                                 // Node.js 全局依赖路径
        CHECK_CONFIG: $store.get('CHECK_CONFIG', 'string'),                       // 自定义 toml 配置文件路径，如 /usr/local/app/script/Lists/config.toml     
        NOTIFY_CONFIG_PATH: $store.get('NOTIFY_CONFIG_PATH', 'string'),           // 自定义通知配置文件路径，如 /usr/locallocal/app/script/Lists/notify.json5
        BARK_PUSH: $store.get('BARK_PUSH', 'string'),                             // bark IP 或设备码，例：https://api.day.app/xxxxxx
        BARK_GROUP: $store.get('BARK_GROUP', 'string'),                           // bark 推送分组，可不填
        BARK_SOUND: $store.get('BARK_SOUND', 'string'),                           // bark 推送声音，可不填
        DD_BOT_SECRET: $store.get('DD_BOT_SECRET', 'string'),                     // 钉钉机器人的 DD_BOT_SECRET
        DD_BOT_TOKEN: $store.get('DD_BOT_TOKEN', 'string'),                       // 钉钉机器人的 DD_BOT_TOKEN
        GOBOT_URL: $store.get('GOBOT_URL', 'string'),                             // go-cqhttp e.g.推送到个人QQ: http://127.0.0.1/send_private_msg 群: http://127.0.0.1/send_group_msg
        GOBOT_QQ: $store.get('GOBOT_QQ', 'string'),                               // go-cqhttp 推送群或者用户。GOBOT_URL 设置 /send_private_msg 时填入 user_id=个人QQ；/send_group_msg 时填入 group_id=QQ群
        GOBOT_TOKEN: $store.get('GOBOT_TOKEN', 'string'),                         // go-cqhttp 的 access_token，可不填
        IGOT_PUSH_KEY: $store.get('IGOT_PUSH_KEY', 'string'),                     // iGot 聚合推送的 IGOT_PUSH_KEY
        PUSH_KEY: $store.get('PUSH_KEY', 'string'),                               // server 酱的 PUSH_KEY，兼容旧版与 Turbo 版
        PUSH_PLUS_TOKEN: $store.get('PUSH_PLUS_TOKEN', 'string'),                 // push+ 微信推送的用户令牌
        PUSH_PLUS_USER: $store.get('PUSH_PLUS_USER', 'string'),                   // push+ 微信推送的群组编码，不填仅推送自己
        QYWX_AM: $store.get('QYWX_AM', 'string'),                                 // 企业微信应用的 QYWX_AM，参考 http://note.youdao.com/s/HMiudGkb，依次填入 corpid, corpsecret, touser(注：多个成员ID使用 | 隔开), agentid, media_id(选填，不填默认文本消息类型)
        QYWX_KEY: $store.get('QYWX_KEY', 'string'),                               // 企业微信机器人的 QYWX_KEY
        TG_BOT_TOKEN: $store.get('TG_BOT_TOKEN', 'string'),                       // tg 机器人的 TG_BOT_TOKEN
        TG_USER_ID: $store.get('TG_USER_ID', 'string'),                           // tg 机器人的 TG_USER_ID
        TG_API_HOST: $store.get('TG_API_HOST', 'string'),                         // tg api 自建反向代理地址，默认 api.telegram.org，可不填
        TG_PROXY_AUTH: $store.get('TG_PROXY_AUTH', 'string'),                     // tg 代理配置认证参数，可不填
        TG_PROXY_HOST: $store.get('TG_PROXY_HOST', 'string'),                     // tg 机器人的 TG_PROXY_HOST，例：127.0.0.1，可不填
        TG_PROXY_PORT: $store.get('TG_PROXY_PORT', 'string')                      // tg 机器人的 TG_PROXY_PORT，例：1080，可不填
    },
    logname: jsname.substring(jsname.indexOf('_') + 1, jsname.lastIndexOf('.')),
    from: 'task',
});
