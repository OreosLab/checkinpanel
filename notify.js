/*
 * @Author: lxk0301 https://gitee.com/lxk0301
 * @Date: 2020-08-19 16:12:40
 * @Last Modified by: Oreomeow
 * @Last Modified time: 2021-11-8 23:30:00
 * sendNotify 推送通知功能
 * @param text 通知头
 * @param desp 通知体
 * @param params 某些推送通知方式点击弹窗可跳转，例：{ url: 'https://abc.com' }
 * @param author 作者仓库等信息 例：`本通知 By：https://github.com/Oreomeow/checkinpanel`
 */

const querystring = require('querystring');
const utils = require('./utils');
const Env = utils.Env;
const $ = new Env('sendNotify');
const getNotifyData = utils.getNotifyData;
const timeout = 15000; // 超时时间(单位毫秒)

const PushConfig = {
    // ================================Bark App 通知设置区域================================
    // 此处填你 Bark App 的信息(IP/设备码，例如：https://api.day.app/XXXXXXXX)
    BARK_PUSH: '',
    // Bark App 推送铃声，铃声列表去 APP 查看复制填写
    BARK_SOUND: '',
    // Bark App 推送消息的分组, 默认为"Checkinpanel"
    BARK_GROUP: 'Checkinpanel',

    // ================================钉钉机器人通知设置区域================================
    // 此处填你钉钉 bot 的 webhook，例如：5a544165465465645d0f31dca676e7bd07415asdasd
    DD_BOT_TOKEN: '',
    // 密钥，机器人安全设置页面，加签一栏下面显示的 SEC 开头的字符串
    DD_BOT_SECRET: '',

    // ================================go-cqhttp 通知设置区域================================
    // go-cqhttp 相关 API https://docs.go-cqhttp.org/api
    // gobot_url 填写请求地址 http://127.0.0.1/send_private_msg
    // gobot_token 填写在 go-cqhttp 文件设置的访问密钥
    // gobot_qq 填写推送到个人 QQ 或者 QQ 群号
    GOBOT_URL: '', // 推送到个人QQ：http://127.0.0.1/send_private_msg  群：http://127.0.0.1/send_group_msg
    GOBOT_TOKEN: '', // 访问密钥
    GOBOT_QQ: '', // 如果 GOBOT_URL 设置 /send_private_msg 则需要填入 user_id=个人QQ 相反如果是 /send_group_msg 则需要填入 group_id=QQ群

    // ================================iGot 聚合通知设置区域================================
    // 此处填你 iGot 的信息(推送 key，例如：https://push.hellyw.com/XXXXXXXX)
    IGOT_PUSH_KEY: '',

    // ================================server酱微信通知设置区域====================================
    // 此处填你申请的 SCKEY
    PUSH_KEY: '',

    // ================================pushplus 通知设置区域================================
    // 官方文档：http://www.pushplus.plus/
    // PUSH_PLUS_TOKEN：微信扫码登录后一对一推送或一对多推送下面的 token(您的 Token)，不提供 PUSH_PLUS_USER 则默认为一对一推送
    PUSH_PLUS_TOKEN: '',
    // PUSH_PLUS_USER： 一对多推送的“群组编码”(一对多推送下面->您的群组(如无则新建)->群组编码，如果您是创建群组人。也需点击“查看二维码”扫描绑定，否则不能接受群组消息推送)
    PUSH_PLUS_USER: '',

    // ================================企业微信应用通知设置区域====================================
    /*
     此处填你企业微信应用消息的值(详见文档 https://work.weixin.qq.com/api/doc/90000/90135/90236)
     环境变量名 QYWX_AM 依次填入 corpid,corpsecret,touser(注：多个成员ID使用|隔开),agentid,消息类型(选填，不填默认文本消息类型)
     注意用,号隔开(英文输入法的逗号)，例如：wwcff56746d9adwers,B-791548lnzXBE6_BWfxdf3kSTMJr9vFEPKAbh6WERQ,mingcheng,1000001,2COXgjH2UIfERF2zxrtUOKgQ9XklUqMdGSWLBoW_lSDAdafat
     可选推送消息类型(推荐使用图文消息(mpnews)):
     - 文本卡片消息: 0 (数字零)
     - 文本消息: 1 (数字一)
     - 图文消息(mpnews): 素材库图片 id, 可查看此教程(http://note.youdao.com/s/HMiudGkb)或者(https://note.youdao.com/ynoteshare1/index.html?id=1a0c8aff284ad28cbd011b29b3ad0191&type=note)
     */
    QYWX_AM: '',

    // ================================企业微信机器人通知设置区域====================================
    // 此处填你企业微信机器人的 webhook(详见文档 https://work.weixin.qq.com/api/doc/90000/90136/91770)，例如：693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa
    QYWX_KEY: '',

    // ================================telegram 机器人通知设置区域====================================
    // 此处填你 telegram bot 的 Token，telegram 机器人通知推送必填项。例如：1077xxx4424:AAFjv0FcqxxxxxxgEMGfi22B4yh15R5uw
    TG_BOT_TOKEN: '',
    // 此处填你接收通知消息的 telegram 用户的 id，telegram 机器人通知推送必填项。例如：129xxx206
    TG_USER_ID: '',
    // tg 推送 HTTP 代理设置(不懂可忽略，telegram 机器人通知推送功能中非必填)
    TG_PROXY_HOST: '', // 例如：127.0.0.1
    TG_PROXY_PORT: '', // 例如：1080
    TG_PROXY_AUTH: '', // tg 代理配置认证参数
    // Telegram api 自建的反向代理地址(不懂可忽略，telegram 机器人通知推送功能中非必填)，默认 tg 官方 api
    TG_API_HOST: 'api.telegram.org',
};

// ================================云端环境变量的判断与接收====================================
for (var i in PushConfig) {
    PushConfig[i] = process.env[i] ? process.env[i] : PushConfig[i];
}
// ================================云端环境变量的判断与接收====================================

// ================================notify.json5 变量再覆盖====================================
if (getNotifyData()) {
    console.log('您使用的是自己的通知配置文件。');
    for (var a in PushConfig) {
        PushConfig[a] = getNotifyData()[a];
    }
}
// ================================notify.json5 变量再覆盖====================================

// ================================某些变量本地最终处理====================================
if (PushConfig.BARK_PUSH && PushConfig.BARK_PUSH.indexOf('https') === -1 && PushConfig.BARK_PUSH.indexOf('http') === -1) {
    // 兼容 Bark 本地用户只填写设备码的情况
    PushConfig.BARK_PUSH = `https://api.day.app/${PushConfig.BARK_PUSH}`;
}
if (PushConfig.TG_PROXY_HOST && PushConfig.TG_PROXY_HOST.indexOf('@') !== -1) {
    PushConfig.TG_PROXY_AUTH = PushConfig.TG_PROXY_HOST.split('@')[0];
    PushConfig.TG_PROXY_HOST = PushConfig.TG_PROXY_HOST.split('@')[1];
}
if (!PushConfig.TG_API_HOST) {
    PushConfig.TG_API_HOST = 'api.telegram.org';
}
// ================================某些变量本地最终处理====================================

/**
 * sendNotify 推送通知功能
 * @param text 通知头
 * @param desp 通知体
 * @param params 某些推送通知方式点击弹窗可跳转，例：{ url: 'https://abc.com' }
 * @param author 作者仓库等信息 例：`本通知 By：https://github.com/Oreomeow/checkinpanel`
 * @returns {Promise<unknown>}
 */
async function sendNotify(text, desp, params = {}, author = '\n\nGitHub: https://github.com/Oreomeow/checkinpanel') {
    // 提供 7 种通知
    desp += author; // 增加作者信息，防止被贩卖等
    await Promise.all([
        serverJNotify(text, desp), // server酱微信通知
        pushplusNotify(text, desp), // pushplus(推送加)
    ]);
    // 由于上述两种微信通知需点击进去才能查看到详情，故 text(标题内容)携带了账号序号以及昵称信息，方便不点击也可知道是哪个京东哪个活动
    text = text.match(/.*?(?=\s?-)/g) ? text.match(/.*?(?=\s?-)/g)[0] : text;
    await Promise.all([
        BarkNotify(text, desp, params), // iOS Bark APP
        ddBotNotify(text, desp), // 钉钉机器人
        gobotNotify(text, desp), // go-cqhttp
        iGotNotify(text, desp, params), // iGot
        qywxamNotify(text, desp), // 企业微信应用
        qywxBotNotify(text, desp), // 企业微信机器人
        tgBotNotify(text, desp), // telegram 机器人
    ]);
}

function BarkNotify(text, desp, params = {}) {
    return new Promise((resolve) => {
        if (PushConfig.BARK_PUSH) {
            const options = {
                url: `${PushConfig.BARK_PUSH}/${encodeURIComponent(text)}/${encodeURIComponent(desp)}?sound=${PushConfig.BARK_SOUND}&group=${
                    PushConfig.BARK_GROUP
                }&${querystring.stringify(params)}`,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout,
            };
            $.get(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log('Bark 发送通知调用 API 失败！！\n');
                        console.log(err);
                    } else {
                        data = JSON.parse(data);
                        if (data.code === 200) {
                            console.log('Bark 发送通知消息成功🎉\n');
                        } else {
                            console.log(`${data.message}\n`);
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve();
                }
            });
        } else {
            resolve();
        }
    });
}

function ddBotNotify(text, desp) {
    return new Promise((resolve) => {
        const options = {
            url: `https://oapi.dingtalk.com/robot/send?access_token=${PushConfig.DD_BOT_TOKEN}`,
            json: {
                msgtype: 'text',
                text: {
                    content: ` ${text}\n\n${desp}`,
                },
            },
            headers: {
                'Content-Type': 'application/json',
            },
            timeout,
        };
        if (PushConfig.DD_BOT_TOKEN && PushConfig.DD_BOT_SECRET) {
            const crypto = require('crypto');
            const dateNow = Date.now();
            const hmac = crypto.createHmac('sha256', PushConfig.DD_BOT_SECRET);
            hmac.update(`${dateNow}\n${PushConfig.DD_BOT_SECRET}`);
            const result = encodeURIComponent(hmac.digest('base64'));
            options.url = `${options.url}&timestamp=${dateNow}&sign=${result}`;
            $.post(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log('钉钉 发送通知消息失败！！\n');
                        console.log(err);
                    } else {
                        data = JSON.parse(data);
                        if (data.errcode === 0) {
                            console.log('钉钉 发送通知消息成功🎉。\n');
                        } else {
                            console.log(`${data.errmsg}\n`);
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve(data);
                }
            });
        } else if (PushConfig.DD_BOT_TOKEN) {
            $.post(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log('钉钉 发送通知消息失败！！\n');
                        console.log(err);
                    } else {
                        data = JSON.parse(data);
                        if (data.errcode === 0) {
                            console.log('钉钉 发送通知消息完成。\n');
                        } else {
                            console.log(`${data.errmsg}\n`);
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve(data);
                }
            });
        } else {
            resolve();
        }
    });
}

function gobotNotify(text, desp, time = 2100) {
    return new Promise((resolve) => {
        if (PushConfig.GOBOT_URL) {
            const options = {
                url: `${PushConfig.GOBOT_URL}?access_token=${PushConfig.GOBOT_TOKEN}&${PushConfig.GOBOT_QQ}`,
                json: { message: `${text}\n${desp}` },
                headers: {
                    'Content-Type': 'application/json',
                },
                timeout,
            };
            setTimeout(() => {
                $.post(options, (err, resp, data) => {
                    try {
                        if (err) {
                            console.log('go-cqhttp 发送通知调用 API 失败！！\n');
                            console.log(err);
                        } else {
                            data = JSON.parse(data);
                            if (data.retcode === 0) {
                                console.log('go-cqhttp 发送通知消息成功🎉\n');
                            } else if (data.retcode === 100) {
                                console.log(`go-cqhttp 发送通知消息异常: ${data.errmsg}\n`);
                            } else {
                                console.log(`go-cqhttp 发送通知消息异常\n${JSON.stringify(data)}`);
                            }
                        }
                    } catch (e) {
                        $.logErr(e, resp);
                    } finally {
                        resolve(data);
                    }
                });
            }, time);
        } else {
            resolve();
        }
    });
}

function iGotNotify(text, desp, params = {}) {
    return new Promise((resolve) => {
        if (PushConfig.IGOT_PUSH_KEY) {
            // 校验传入的 PushConfig.IGOT_PUSH_KEY 是否有效
            const IGOT_PUSH_KEY_REGX = new RegExp('^[a-zA-Z0-9]{24}$');
            if (!IGOT_PUSH_KEY_REGX.test(PushConfig.IGOT_PUSH_KEY)) {
                console.log('您所提供的 IGOT_PUSH_KEY 无效\n');
                resolve();
                return;
            }
            const options = {
                url: `https://push.hellyw.com/${PushConfig.IGOT_PUSH_KEY.toLowerCase()}`,
                body: `title=${text}&content=${desp}&${querystring.stringify(params)}`,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout,
            };
            $.post(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log('iGot 发送通知调用 API 失败！！\n');
                        console.log(err);
                    } else {
                        if (typeof data === 'string') data = JSON.parse(data);
                        if (data.ret === 0) {
                            console.log('iGot 发送通知消息成功🎉\n');
                        } else {
                            console.log(`iGot 发送通知消息失败：${data.errMsg}\n`);
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve(data);
                }
            });
        } else {
            resolve();
        }
    });
}

function serverJNotify(text, desp, time = 2100) {
    return new Promise((resolve) => {
        if (PushConfig.PUSH_KEY) {
            // 微信 server酱推送通知一个 \n 不会换行，需要两个 \n 才能换行，故做此替换
            desp = desp.replace(/[\n\r]/g, '\n\n');
            const options = {
                url: PushConfig.PUSH_KEY.includes('SCT')
                    ? `https://sctapi.ftqq.com/${PushConfig.PUSH_KEY}.send`
                    : `https://sc.ftqq.com/${PushConfig.PUSH_KEY}.send`,
                body: `text=${text}&desp=${desp}`,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout,
            };
            setTimeout(() => {
                $.post(options, (err, resp, data) => {
                    try {
                        if (err) {
                            console.log('server酱 发送通知调用 API 失败！！\n');
                            console.log(err);
                        } else {
                            data = JSON.parse(data);
                            // server酱和 Server酱·Turbo 版的返回 json 格式不太一样
                            if (data.errno === 0 || data.data.errno === 0) {
                                console.log('server酱 发送通知消息成功🎉\n');
                            } else if (data.errno === 1024) {
                                // 一分钟内发送相同的内容会触发
                                console.log(`server酱 发送通知消息异常: ${data.errmsg}\n`);
                            } else {
                                console.log(`server酱 发送通知消息异常\n${JSON.stringify(data)}`);
                            }
                        }
                    } catch (e) {
                        $.logErr(e, resp);
                    } finally {
                        resolve(data);
                    }
                });
            }, time);
        } else {
            resolve();
        }
    });
}

function pushplusNotify(text, desp) {
    return new Promise((resolve) => {
        if (PushConfig.PUSH_PLUS_TOKEN) {
            desp = desp.replace(/[\n\r]/g, '<br>'); // 默认为 html, 不支持 plaintext
            const body = {
                token: `${PushConfig.PUSH_PLUS_TOKEN}`,
                title: `${text}`,
                content: `${desp}`,
                topic: `${PushConfig.PUSH_PLUS_USER}`,
            };
            const options = {
                url: `https://www.pushplus.plus/send`,
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': ' application/json',
                },
                timeout,
            };
            $.post(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log(`pushplus 发送${PushConfig.PUSH_PLUS_USER ? '一对多' : '一对一'}通知消息失败！！\n`);
                        console.log(err);
                    } else {
                        data = JSON.parse(data);
                        if (data.code === 200) {
                            console.log(`pushplus 发送${PushConfig.PUSH_PLUS_USER ? '一对多' : '一对一'}通知消息完成。\n`);
                        } else if (data.code === 600) {
                            options['url'] = 'http://pushplus.hxtrip.com/send';
                            $.post(options, (e, r, d) => {
                                try {
                                    if (e) {
                                        console.log(`pushplus(hxtrip) 发送${PushConfig.PUSH_PLUS_USER ? '一对多' : '一对一'}通知消息失败！！\n`);
                                        console.log(e);
                                    } else {
                                        data = JSON.parse(d);
                                        if (data.code === 200) {
                                            console.log(`pushplus(hxtrip) 发送${PushConfig.PUSH_PLUS_USER ? '一对多' : '一对一'}通知消息完成。\n`);
                                        } else {
                                            console.log(`pushplus(hxtrip) 发送${PushConfig.PUSH_PLUS_USER ? '一对多' : '一对一'}通知消息失败：${data.msg}\n`);
                                        }
                                    }
                                } catch (error) {
                                    $.logErr(error, r);
                                } finally {
                                    resolve(data);
                                }
                            });
                        } else {
                            console.log(`pushplus 发送${PushConfig.PUSH_PLUS_USER ? '一对多' : '一对一'} 通知消息失败：${data.msg}\n`);
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve(data);
                }
            });
        } else {
            resolve();
        }
    });
}

function qywxamNotify(text, desp) {
    return new Promise((resolve) => {
        if (PushConfig.QYWX_AM) {
            const QYWX_AM_AY = PushConfig.QYWX_AM.split(',');
            const options_accesstoken = {
                url: `https://qyapi.weixin.qq.com/cgi-bin/gettoken`,
                json: {
                    corpid: `${QYWX_AM_AY[0]}`,
                    corpsecret: `${QYWX_AM_AY[1]}`,
                },
                headers: {
                    'Content-Type': 'application/json',
                },
                timeout,
            };
            $.post(options_accesstoken, (err, resp, data) => {
                var html = desp.replace(/\n/g, '<br/>');
                var json = JSON.parse(data);
                var accesstoken = json.access_token;
                let options;

                switch (QYWX_AM_AY[4]) {
                    case '0':
                        options = {
                            msgtype: 'textcard',
                            textcard: {
                                title: `${text}`,
                                description: `${desp}`,
                                url: 'https://github.com/Oreomeow/checkinpanel',
                                btntxt: '更多',
                            },
                        };
                        break;

                    case '1':
                        options = {
                            msgtype: 'text',
                            text: {
                                content: `${text}\n\n${desp}`,
                            },
                        };
                        break;

                    default:
                        options = {
                            msgtype: 'mpnews',
                            mpnews: {
                                articles: [
                                    {
                                        title: `${text}`,
                                        thumb_media_id: `${QYWX_AM_AY[4]}`,
                                        author: `智能助手`,
                                        content_source_url: ``,
                                        content: `${html}`,
                                        digest: `${desp}`,
                                    },
                                ],
                            },
                        };
                }
                if (!QYWX_AM_AY[4]) {
                    // 如不提供第四个参数，则默认进行文本消息类型推送
                    options = {
                        msgtype: 'text',
                        text: {
                            content: `${text}\n\n${desp}`,
                        },
                    };
                }
                options = {
                    url: `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${accesstoken}`,
                    json: {
                        touser: `${ChangeUserId(desp)}`,
                        agentid: `${QYWX_AM_AY[3]}`,
                        safe: '0',
                        ...options,
                    },
                    headers: {
                        'Content-Type': 'application/json',
                    },
                };

                $.post(options, (err, resp, data) => {
                    try {
                        if (err) {
                            console.log('成员 ID:' + ChangeUserId(desp) + '企业微信应用 发送通知消息失败！！\n');
                            console.log(err);
                        } else {
                            data = JSON.parse(data);
                            if (data.errcode === 0) {
                                console.log('成员 ID:' + ChangeUserId(desp) + '企业微信应用 发送通知消息成功🎉。\n');
                            } else {
                                console.log(`${data.errmsg}\n`);
                            }
                        }
                    } catch (e) {
                        $.logErr(e, resp);
                    } finally {
                        resolve(data);
                    }
                });
            });
        } else {
            resolve();
        }
    });
}
function ChangeUserId(desp) {
    const QYWX_AM_AY = PushConfig.QYWX_AM.split(',');
    if (QYWX_AM_AY[2]) {
        const userIdTmp = QYWX_AM_AY[2].split('|');
        let userId = '';
        for (let i = 0; i < userIdTmp.length; i++) {
            const count2 = '签到号 ' + (i + 1);
            if (desp.match(count2)) {
                userId = userIdTmp[i];
            }
        }
        if (!userId) userId = QYWX_AM_AY[2];
        return userId;
    } else {
        return '@all';
    }
}

function qywxBotNotify(text, desp) {
    return new Promise((resolve) => {
        const options = {
            url: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${PushConfig.QYWX_KEY}`,
            json: {
                msgtype: 'text',
                text: {
                    content: ` ${text}\n\n${desp}`,
                },
            },
            headers: {
                'Content-Type': 'application/json',
            },
            timeout,
        };
        if (PushConfig.QYWX_KEY) {
            $.post(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log('企业微信机器人 发送通知消息失败！！\n');
                        console.log(err);
                    } else {
                        data = JSON.parse(data);
                        if (data.errcode === 0) {
                            console.log('企业微信机器人 发送通知消息成功🎉。\n');
                        } else {
                            console.log(`${data.errmsg}\n`);
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve(data);
                }
            });
        } else {
            resolve();
        }
    });
}

function tgBotNotify(text, desp) {
    return new Promise((resolve) => {
        if (PushConfig.TG_BOT_TOKEN && PushConfig.TG_USER_ID) {
            const options = {
                url: `https://${PushConfig.TG_API_HOST}/bot${PushConfig.TG_BOT_TOKEN}/sendMessage`,
                body: `chat_id=${PushConfig.TG_USER_ID}&text=${text}\n\n${desp}&disable_web_page_preview=true`,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout,
            };
            if (PushConfig.TG_PROXY_HOST && PushConfig.TG_PROXY_PORT) {
                const tunnel = require('tunnel');
                const agent = {
                    https: tunnel.httpsOverHttp({
                        proxy: {
                            host: PushConfig.TG_PROXY_HOST,
                            port: PushConfig.TG_PROXY_PORT * 1,
                            proxyAuth: PushConfig.TG_PROXY_AUTH,
                        },
                    }),
                };
                Object.assign(options, { agent });
            }
            $.post(options, (err, resp, data) => {
                try {
                    if (err) {
                        console.log('telegram 发送通知消息失败！！\n');
                        console.log(err);
                    } else {
                        data = JSON.parse(data);
                        if (data.ok) {
                            console.log('telegram 发送通知消息成功🎉。\n');
                        } else if (data.error_code === 400) {
                            console.log('请主动给 bot 发送一条消息并检查接收用户 TG_USER_ID 是否正确。\n');
                        } else if (data.error_code === 401) {
                            console.log('TG_BOT_TOKEN 填写错误。\n');
                        }
                    }
                } catch (e) {
                    $.logErr(e, resp);
                } finally {
                    resolve(data);
                }
            });
        } else {
            resolve();
        }
    });
}

module.exports = {
    sendNotify,
};
