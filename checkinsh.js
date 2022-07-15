// @grant nodejs
let shname = $env.SHNAME;
console.log(`⏳ 开始执行 ${shname}`);
$exec(`bash ${shname}`, {
    cwd: 'script/Shell/checkinpanel',
    timeout: 0,
    // prettier-ignore
    env: {
        ENV_PATH: $store.get('ENV_PATH', 'string'),                               // 自定义 .env 配置文件路径，如 /usr/local/app/script/Lists/.env
        DD_BOT_SECRET: $store.get('DD_BOT_SECRET', 'string'),                     // 钉钉机器人的 DD_BOT_SECRET
        DD_BOT_TOKEN: $store.get('DD_BOT_TOKEN', 'string'),                       // 钉钉机器人的 DD_BOT_TOKEN
        PUSH_KEY: $store.get('PUSH_KEY', 'string'),                               // server 酱旧版 PUSH_KEY
        PUSH_TURBO_KEY: $store.get('PUSH_KEY', 'string'),                         // server 酱 Turbo 版 PUSH_KEY
        PUSH_PLUS_TOKEN: $store.get('PUSH_PLUS_TOKEN', 'string'),                 // push+ 微信推送的用户令牌
        QMSG_KEY: $store.get('QMSG_KEY', 'string'),                               // qmsg 酱的 QMSG_KEY
        CORPID: $store.get('CORPID', 'string'),                                   // 企业微信 ID
        AGENTID: $store.get('AGENTID', 'string'),                                 // 企业微信应用 ID
        CORPSECRET: $store.get('CORPSECRET', 'string'),                           // 企业微信密钥
        SRE_TOKEN: $store.get('SRE_TOKEN', 'string'),                             // SRE24.com 的 SRE_TOKEN，https://push.jwks123.cn 关注公众号后再次点击获取令牌
        TG_BOT_TOKEN: $store.get('TG_BOT_TOKEN', 'string'),                       // tg 机器人的 TG_BOT_TOKEN
        TG_USER_ID: $store.get('TG_USER_ID', 'string'),                           // tg 机器人的 TG_USER_ID
    },
    logname: shname.substring(shname.indexOf('_') + 1, shname.lastIndexOf('.')),
    from: 'task',
});
