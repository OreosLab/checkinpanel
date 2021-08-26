// @grant nodejs
let name = $env.NAME
console.log(`⏳ 开始执行 ${name}`)
$exec(`python3 https://raw.githubusercontent.com/Oreomeow/dailycheckinV2P/master/${name}`, {
    cwd: './script/Shell/dailycheckinV2P',
    timeout: 0,
    env: {
        BARK: $store.get('BARK', 'string'),                                       // bark服务,此参数如果以http或者https开头则判定为自建bark服务; secrets可填;
        SCKEY: $store.get('SCKEY', 'string'),                                     // Server酱的SCKEY; secrets可填
        TG_BOT_TOKEN: $store.get('TG_BOT_TOKEN', 'string'),                       // tg机器人的TG_BOT_TOKEN; secrets可填
        TG_USER_ID: $store.get('TG_USER_ID', 'string'),                           // tg机器人的TG_USER_ID; secrets可填
        TG_API_HOST: $store.get('TG_API_HOST', 'string'),                         // tg 代理api
        TG_PROXY_IP: $store.get('TG_PROXY_IP', 'string'),                         // tg机器人的TG_PROXY_IP; secrets可填
        TG_PROXY_PORT: $store.get('TG_PROXY_PORT', 'string'),                     // tg机器人的TG_PROXY_PORT; secrets可填
        DD_BOT_ACCESS_TOKEN: $store.get('DD_BOT_ACCESS_TOKEN', 'string'),         // 钉钉机器人的DD_BOT_ACCESS_TOKEN; secrets可填
        DD_BOT_SECRET: $store.get('DD_BOT_SECRET', 'string'),                     // 钉钉机器人的DD_BOT_SECRET; secrets可填
        QYWX_APP: $store.get('QYWX_APP', 'string'),                               // 企业微信应用的QYWX_APP; secrets可填 参考http://note.youdao.com/s/HMiudGkb
        QQ_SKEY: $store.get('QQ_SKEY', 'string'),                                 // qq机器人的QQ_SKEY; secrets可填
        QQ_MODE: $store.get('QQ_MODE', 'string'),                                 // qq机器人的QQ_MODE; secrets可填
        QYWX_AM: $store.get('QYWX_AM', 'string'),                                 // 企业微信
        PUSH_PLUS_TOKEN: $store.get('PUSH_PLUS_TOKEN', 'string'),                 // 微信推送Plus+
        GOBOT_URL: $store.get('GOBOT_URL', 'string'),                             // go-cqhttp 例如:推送到个人QQ: http://127.0.0.1/send_private_msg  群：http://127.0.0.1/send_group_msg
        GOBOT_TOKEN: $store.get('GOBOT_TOKEN', 'string'),                         // go-cqhttp的access_token 可不填
        GOBOT_QQ: $store.get('GOBOT_QQ', 'string'),                               // go-cqhttp的推送群或者用户 GOBOT_URL设置 /send_private_msg 则需要填入 user_id=个人QQ 相反如果是 /send_group_msg 则需要填入 group_id=QQ群
    },
    cb(data, error) {
        error ? console.error(error) : console.log(data)
    }
})