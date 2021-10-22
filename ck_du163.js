/*
52 9 * * * ck_du163.js
*/

const axios = require('axios');

const utils = require('./utils');
const Env = utils.Env;
const get_data = utils.get_data;

const $ = new Env('网易蜗牛读书');
const cookieDU163s = get_data().DU163;
const notify = $.isNode() ? require('./notify') : '';

var desp = '';

du163();

function du163() {
    return new Promise(async (resolve) => {
        let result = '【网易蜗牛读书】: ';
        if (cookieDU163s) {
            Log('cookie 数量：' + cookieDU163s.length);
            for (let a = 0; a < cookieDU163s.length; a++) {
                let cookie = cookieDU163s[a].cookie;
                let _xsrf = cookie.match(/_xsrf=(\S*);*/)[1];
                let user_agent = cookieDU163s[a].user_agent;
                Log('\n========== [Cookie ' + (a + 1) + '] Start ========== ');
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
    desp = desp + '\n' + info;
    return desp;
}

module.exports = du163;
