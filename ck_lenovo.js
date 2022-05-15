/*
* @url: https://raw.githubusercontent.com/Wenmoux/checkbox/master/scripts/lenovo.js
* @author: wenmoux
10 22 * * * ck_lenovo.js
*/

const axios = require('axios');
const CryptoJS = require('crypto-js');

const utils = require('./utils');
const Env = utils.Env;
const getData = utils.getData;

const $ = new Env('联想商城');
const notify = $.isNode() ? require('./notify') : '';
const ACCOUNTS_LENOVO = getData().LENOVO;

const url = {
    login: '',
    session:
        'https://api.club.lenovo.cn/users/getSessionID?s=8091b7729079682e9a58f609035619625b984e3a2d2b229caf45c7108b37221864b1cd92353716a721f8a240b455740951002d5cdfe3bd723c6e5a35f7bd6f2ffa955e1edf92d0a82274805efb604d602ac2900470589637e65903b9c136e458d6e6c581433bdc857f10fba9e615e3fea1ddb98a2cd86f1a828c03630c96155f3bda0b12c963868f80fc791fab1edcc1dda8a25c5722e5ec521b6050605e0da191edcfabf3d3d5412391dc77cd7ddbda89cb1abf4a0e6da165394d96b546a578c2577df88d04f6cb55d37ed4bcda03c9844a728dedc1c09558e3d08a4c2c89281ca2500ee5d9a67bd66edc6866e86114d6f2e447efbfad104461c0f75be2d9461047434315e57febbae78a30500f27ae25b3ea33a7dc50c16a50fa7fa900ca0a',
    sign1: 'https://api.club.lenovo.cn/common/signin/add',
    sign2: 'https://api.club.lenovo.cn/signin/v2/add',
};
const headers = {
    baseinfo: '',
    unique: '',
    'User-Agent': 'LenovoClub/5.1.3 (iPad; iOS 14.7.1; Scale/2.00)',
    token: '',
    //"User-Agent":"Apache-HttpClient/UNAVAILABLE (java 1.5)",
    Authorization: '',
};

var desp = '';

lenovo();

async function lenovo() {
    if (ACCOUNTS_LENOVO) {
        Log('account 数量：' + ACCOUNTS_LENOVO.length);
        for (let a = 0; a < ACCOUNTS_LENOVO.length; a++) {
            let account = ACCOUNTS_LENOVO[a].account;
            let password = ACCOUNTS_LENOVO[a].password;
            let baseinfo = ACCOUNTS_LENOVO[a].baseinfo
                ? ACCOUNTS_LENOVO[a].baseinfo
                : 'eyJpbWVpIjoiODY1MzE1MDMxOTg1ODc4IiwicGhvbmVicmFuZCI6Imhvbm9yIiwicGhvbmVNb2RlbCI6IkZSRC1BTDEwIiwiYXBwVmVyc2lvbiI6IlY0LjIuNSIsInBob25laW5jcmVtZW50YWwiOiI1NTYoQzAwKSIsIlBhZ2VJbmZvIjoiTXlJbmZvcm1hdGlvbkFjdGlvbkltcGwiLCJwaG9uZWRpc3BsYXkiOiJGUkQtQUwxMCA4LjAuMC41NTYoQzAwKSIsInBob25lTWFudWZhY3R1cmVyIjoiSFVBV0VJIiwibGVub3ZvQ2x1YkNoYW5uZWwiOiJ5aW5neW9uZ2JhbyIsImxvZ2luTmFtZSI6IjE3NjQwNDA4NTM3IiwicGhvbmVwcm9kdWN0IjoiRlJELUFMMTAiLCJzeXN0ZW1WZXJzaW9uIjoiOC4wLjAiLCJhbmRyb2lkc2RrdmVyc2lvbiI6IjI2In0=';
            let parsedWordArray = CryptoJS.enc.Base64.parse(baseinfo);
            let info = JSON.parse(parsedWordArray.toString(CryptoJS.enc.Utf8));
            let deviceid = info.imei;
            url.login = `https://uss.lenovomm.com/authen/1.2/tgt/user/get?msisdn=${account}`;
            headers.baseinfo = baseinfo;
            headers.unique = deviceid;
            Log('\n======== [Account ' + (a + 1) + '] Start ======== ');
            let lpsutgt = await lxlogin(deviceid, info, password);
            let session = await getsession(lpsutgt);
            if (session) {
                await addsign(session, deviceid);
            }
        }
    } else {
        Log(`【联想延保每日签到】：请填写联想商城抓包数据`);
    }
    notify.sendNotify('联想商城', desp);
    return '联想商城' + '\n\n' + desp;
}

function lxlogin(deviceid, info, password) {
    return new Promise(async (resolve) => {
        try {
            let data = `lang=zh-CN-%23Hans&source=android%3Acom.lenovo.club.app-V4.2.5&deviceidtype=mac&deviceid=${deviceid}&devicecategory=unknown&devicevendor=${info.phoneManufacturer}&devicefamily=unknown&devicemodel=${info.phoneModel}&osversion=${info.systemVersion}&osname=Android&password=${password}`;
            let res = await axios.post(url['login'], data);
            var lpsutgt = res.data.match(/<Value>(.+?)<\/Value>/);
            if (lpsutgt) {
                let res2 = await axios.get(
                    `https://uss.lenovomm.com/authen/1.2/st/get?lpsutgt=${lpsutgt[1]}&source=ios%3Alenovo%3Aclub%3A4.1.0&lang=zh-CN&realm=club.lenovo.com.cn`
                );
                let lpsutgt2 = res2.data.match(/<Value>(.+?)<\/Value>/);
                lpsutgt = lpsutgt2 ? lpsutgt2[1] : null;
            }
            Log('登录成功！');
            // 预约游戏id
        } catch (err) {
            lpsutgt = null;
            Log(`登录失败！${err.response}`);
        }
        resolve(lpsutgt);
    });
}

function getsession(lpsutgt) {
    return new Promise(async (resolve) => {
        try {
            headers.Authorization = 'Lenovosso ' + lpsutgt;
            headers['token'] = headers.Authorization + '==';
            let res3 = await axios.get(url['session'], {
                headers,
            });
            let json = {
                lenovoid: res3.data.res.lenovoid,
                sessionid: res3.data.res.sessionid,
                token: res3.data.res.token,
            };
            resolve(json);
        } catch (err) {
            Log(`获取token失败 ${decodeURI(err.response.data.res.error_CN)}`);
        }
        resolve();
    });
}

function addsign(session, deviceid) {
    return new Promise(async (resolve) => {
        try {
            headers.Authorization = 'Lenovo ' + session.sessionid;
            headers['token'] = session.token + '==';
            headers['User-Agent'] = 'Apache-HttpClient/UNAVAILABLE (java 1.5)';
            let data = `imei=${deviceid}&uid=${session.lenovoid}`;
            let res = await axios.post(url['sign2'], data, {
                headers,
            });
            if (typeof res.data === 'object' && res.data.status == 0) {
                //  msg+=res.data.res.add_yb_tip
                if (!res.data.res.success) {
                    Log('今天已经签到过啦');
                } else {
                    Log('签到成功\n' + res.data.res.rewardTips + '\n连续签到' + res.data.res.continueCount + '天');
                }
            }
        } catch (err) {
            Log(`签到失败 ${decodeURI(err.response.data.res.error_CN)}`);
        }
        resolve();
    });
}

function Log(info) {
    console.log(info);
    desp = desp + info + '\n';
    return desp;
}

module.exports = lenovo;
