// @grant nodejs
let jsname = $env.JSNAME
console.log(`⏳ 开始执行 ${jsname}`)
$exec(`node https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/${jsname}`, {
    cwd: './script/Shell/checkinpanel',
    timeout: 0,
    env: {
        BARK_PUSH: $store.get('BARK_PUSH', 'string'),
        BARK_SOUND: $store.get('BARK_SOUND', 'string'),
        BARK_GROUP: $store.get('BARK_GROUP', 'string'),
        DD_BOT_SECRET: $store.get('DD_BOT_SECRET', 'string'),                     // 钉钉机器人的 DD_BOT_SECRET
        DD_BOT_TOKEN: $store.get('DD_BOT_TOKEN', 'string'),                       // 钉钉机器人的 DD_BOT_TOKEN
        GOBOT_URL: $store.get('GOBOT_URL', 'string'),                             // go-cqhttp e.g.推送到个人QQ: http://127.0.0.1/send_private_msg 群: http://127.0.0.1/send_group_msg
        GOBOT_QQ: $store.get('GOBOT_QQ', 'string'),                               // go-cqhttp 推送群或者用户。GOBOT_URL 设置 /send_private_msg 则需要填入 user_id=个人QQ；相反如果是 /send_group_msg 则需要填入 group_id=QQ群
        GOBOT_TOKEN: $store.get('GOBOT_TOKEN', 'string'),                         // go-cqhttp 的 access_token，可不填
        IGOT_PUSH_KEY: $store.get('IGOT_PUSH_KEY', 'string'),
        PUSH_KEY: $store.get('PUSH_KEY', 'string'),                               // server 酱的 PUSH_KEY，兼容旧版与 Turbo 版
        PUSH_PLUS_TOKEN: $store.get('PUSH_PLUS_TOKEN', 'string'),                 // push+ 微信推送
        QQ_KEY: $store.get('QQ_KEY', 'string'),                                   
        QQ_MODE: $store.get('QQ_MODE', 'string'),                                 
        QYWX_AM: $store.get('QYWX_AM', 'string'),                                 // 企业微信应用的 QYWX_AM，参考 http://note.youdao.com/s/HMiudGkb
        QYWX_KEY: $store.get('QYWX_KEY', 'string'),                               // 企业微信机器人的 QYWX_KEY
        TG_BOT_TOKEN: $store.get('TG_BOT_TOKEN', 'string'),                       // tg 机器人的 TG_BOT_TOKEN
        TG_USER_ID: $store.get('TG_USER_ID', 'string'),                           // tg 机器人的 TG_USER_ID
        TG_API_HOST: $store.get('TG_API_HOST', 'string'),                         // tg 代理 api
        TG_PROXY_AUTH: $store.get('TG_PROXY_AUTH', 'string'),
        TG_PROXY_IP: $store.get('TG_PROXY_IP', 'string'),                         // tg 机器人的 TG_PROXY_IP
        TG_PROXY_PORT: $store.get('TG_PROXY_PORT', 'string')                      // tg 机器人的 TG_PROXY_PORT
    }
})
