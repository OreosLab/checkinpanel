// @grant nodejs
let shname = $env.SHNAME
console.log(`⏳ 开始执行 ${shname}`)
$exec(`chmod +x ${shname} && bash ${shname}`, {
    cwd: './script/Shell/checkinpanel',
    timeout: 0,
    env: {
        ENV_PATH: $store.get('ENV_PATH', 'string'),                               // 配置文件路径
        HITOKOTO: $store.get('HITOKOTO', 'boolean'),                              // 一言，true 为开启，false 为关闭，默认关闭
        BARK: $store.get('BARK', 'string'),                                       // bark 服务，此参数如果以 http 或者 https 开头则判定为自建 bark 服务；secrets 可填
        PUSH_KEY: $store.get('PUSH_KEY', 'string'),                               // Server酱的 PUSH_KEY；secrets 可填
        TG_BOT_TOKEN: $store.get('TG_BOT_TOKEN', 'string'),                       // tg 机器人的 TG_BOT_TOKEN；secrets 可填
        TG_USER_ID: $store.get('TG_USER_ID', 'string'),                           // tg 机器人的 TG_USER_ID；secrets 可填
        TG_API_HOST: $store.get('TG_API_HOST', 'string'),                         // tg 代理 api
        TG_PROXY_IP: $store.get('TG_PROXY_IP', 'string'),                         // tg 机器人的 TG_PROXY_IP；secrets 可填
        TG_PROXY_PORT: $store.get('TG_PROXY_PORT', 'string'),                     // tg 机器人的 TG_PROXY_PORT；secrets 可填
        DD_BOT_TOKEN: $store.get('DD_BOT_TOKEN', 'string'),                       // 钉钉机器人的 DD_BOT_TOKEN；secrets 可填
        DD_BOT_SECRET: $store.get('DD_BOT_SECRET', 'string'),                     // 钉钉机器人的 DD_BOT_SECRET；secrets 可填
        QYWX_AM: $store.get('QYWX_AM', 'string'),                                 // 企业微信应用的 QYWX_AM；secrets可填 参考 http://note.youdao.com/s/HMiudGkb
        QMSG_KEY: $store.get('QMSG_KEY', 'string'),                               // qmsg 酱的 QMSG_KEY；secrets 可填
        QMSG_TYPE: $store.get('QMSG_TYPE', 'string'),                             // qmsg 酱的 QMSG_TYPE；secrets 可填
        PUSH_PLUS_TOKEN: $store.get('PUSH_PLUS_TOKEN', 'string'),                 // 微信推送 Plus+
        GOBOT_URL: $store.get('GOBOT_URL', 'string'),                             // go-cqhttp 例如：推送到个人QQ: http://127.0.0.1/send_private_msg  群: http://127.0.0.1/send_group_msg
        GOBOT_TOKEN: $store.get('GOBOT_TOKEN', 'string'),                         // go-cqhttp 的 access_token 可不填
        GOBOT_QQ: $store.get('GOBOT_QQ', 'string'),                               // go-cqhttp 的推送群或者用户 GOBOT_URL设置 /send_private_msg 则需要填入 user_id=个人QQ 相反如果是 /send_group_msg 则需要填入 group_id=QQ群
        FSKEY: $store.get('FSKEY', 'string')                                      // 飞书 的 FSKEY；https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx 的 xxxxxx 部分
    },
    cb(data, error) {
        error ? console.error(error) : console.log(data)
    }
})