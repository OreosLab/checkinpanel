/*
52 9 * * * ck_du163.js
*/

const axios = require('axios');

const utils = require('./utils');
const Env = utils.Env;
const getData = utils.getData;

const $ = new Env('网易蜗牛读书');
const notify = $.isNode() ? require('./notify') : '';
const COOKIES_DU163 = getData().DU163;

var desp = '';

du163();

function du163() {
    return new Promise(async (resolve) => {
        let result = '【网易蜗牛读书】: ';
        if (COOKIES_DU163) {
            Log('cookie 数量：' + COOKIES_DU163.length);
            for (let a = 0; a < COOKIES_DU163.length; a++) {
                let cookie = COOKIES_DU163[a].cookie;
                let _xsrf = cookie.match(/_xsrf=(\S*);*/)[1];
                let user_agent = COOKIES_DU163[a].user_agent;
                Log('\n======== [Cookie ' + (a + 1) + '] Start ======== ');
                try {
                    const headers = {
                        headers: {
                            cookie: cookie,
                            'user-agent': user_agent,
                        },
                    };
                    let url = 'https://du.163.com/activity/201907/activityCenter/sign.json';
                    let data = `csrfToken=${_xsrf}`;
                    let res = await axios.post(url, data, headers);
                    if (res.data.code == -1104) {
                        var msg = res.data.msg;
                    } else if (res.data.code == 0) {
                        msg = res.data.message + ' 连签' + res.data.continuousSignedDays + '天';
                    } else {
                        msg = '签到失败 ' + res.data.msg;
                    }
                    result += msg;
                } catch (err) {
                    result = result + '签到失败  ' + err.response.data.msg;
                }
            }
        } else {
            result += '请填写网易蜗牛读书cookies';
        }
        resolve(result);
        Log(result);
        notify.sendNotify('网易蜗牛读书', desp);
    });
}

function Log(info) {
    console.log(info);
    desp = desp + info + '\n';
    return desp;
}

module.exports = du163;
