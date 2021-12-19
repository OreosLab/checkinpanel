/*
* @url: https://raw.githubusercontent.com/Wenmoux/checkbox/master/scripts/aiqicha.js
* @author: wenmoux
37 0-23/8 * * * ck_aiqicha.js
*/

const axios = require('axios');

const utils = require('./utils');
const Env = utils.Env;
const sleep = utils.sleep;
const getData = utils.getData;

const $ = new Env('爱企查');
const notify = $.isNode() ? require('./notify') : '';
const COOKIES_AQC = getData().AQC;

const headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36',
    referer: 'https://aiqicha.baidu.com/m/s?t=3&q=%E5%B0%8F%E7%B1%B3&VNK=e73b55ef',
    'X-Requested-With': 'XMLHttpRequest',
    Host: 'aiqicha.baidu.com',
    cookie: '',
};
const oo = {
    CX10002: '每日签到',
    CX10001: '每日登陆',
    CX11001: '查询企业',
    CX11002: '查询老板',
    CX11003: '查询老赖',
    CX11004: '查询商标',
    CX11005: '查询地图',
    CX11006: '浏览新闻',
    CX11007: '浏览监控日报',
    CX11009: '查询关系',
    CX11010: '批量查询',
    CX12001: '添加监控',
    CX12002: '添加关注',
    CX12005: '分享任务',
    CX12006: '邀请任务',
    CX12007: '高级搜索',
    CX12008: '高级筛选',
    CX12009: '浏览互动',
    CX12011: '点赞观点',
};

var desp = '';
var key = ['苹果', '华为', '百度', '一个', '百事', '厚墨'];
var nid = null;
var popularSearchKey = [];
var ytaskList = [];
var taskList = [];
var claimList = [];
var alltaskList = [];

aqc();

async function aqc() {
    let msg = '【爱企查】：';
    if (COOKIES_AQC) {
        Log('cookie 数量：' + COOKIES_AQC.length);
        for (let a = 0; a < COOKIES_AQC.length; a++) {
            let aqcCookie = COOKIES_AQC[a].cookie;
            let exportkey = COOKIES_AQC[a].exportkey ? COOKIES_AQC[a].exportkey : '';
            headers.cookie = aqcCookie;
            Log('\n========== [Account ' + (a + 1) + '] Start ========== ');
            Log('爱企查每日任务开始');
            let logininfo = await get('m/getuserinfoAjax');
            if (logininfo.data.isLogin == 1) {
                Log('获取热搜词...');
                let keyword = await get('m/popularSearcheAjax');
                if (keyword.data)
                    popularSearchKey = keyword.data.map((item) => {
                        return item.words;
                    });
                key = [...key, ...popularSearchKey];
                await getaskList();
                await dotask(taskList, aqcCookie, exportkey);
                await dotask(taskList, aqcCookie, exportkey);
                await sleep(5000);
                await getaskList();
                for (let task of claimList) {
                    Log(`领取爱豆：${oo[task]}`);
                    let clres = await get(`zxcenter/claimUserTaskAjax?taskCode=${task}`, 'get');
                    if (clres.status == 0) Log(`  领取成功！获得${clres.data.totalScore}爱豆`);
                    await sleep(2500);
                }
                Log('去查询爱豆积分');
                let userinfo = await get('usercenter/getvipinfoAjax', 'get');
                msg += `账号 ${a + 1} 【${logininfo.data.userName}】 共 ${userinfo.data.consume} 爱豆\n`;
            } else {
                msg = 'cookie已失效';
            }
        }
    } else {
        msg += '请填写百度爱企查 cookies (同百度贴吧';
    }
    Log(msg);
    notify.sendNotify('爱企查', desp);
    return '爱企查' + '\n\n' + desp;
}

function rand() {
    let i = Math.floor(Math.random() * key.length);
    return key[i];
}

function get(api, data, method = 'get') {
    return new Promise(async (resolve) => {
        try {
            let url = `https://aiqicha.baidu.com/${api}`;
            if (method == 'get')
                var res = await axios.get(url, {
                    headers,
                });
            if (method == 'post')
                res = await axios.post(url, data, {
                    headers,
                });
            if (res.data.status == 0) Log('    操作成功');
            else Log('    ' + res.data.msg);
            resolve(res.data);
        } catch (err) {
            Log(err);
        }
        resolve();
    });
}

async function getaskList() {
    ytaskList = [];
    taskList = [];
    claimList = [];
    alltaskList = [];
    let tres = await get('usercenter/checkTaskStatusAjax');
    let obj = tres.data;
    if (tres.status == 0) {
        Object.keys(obj).forEach(function (k) {
            if (oo[k]) {
                let task = obj[k];
                task.title = k;
                alltaskList.push(task);
                if (task.count == task.totalcount) ytaskList.push(task);
                if (task.canClaim != 0) claimList.push(k);
                if (task.count != task.totalcount) taskList.push(task);
            }
        });
    }
    Log(`共 ${alltaskList.length} 任务 已完成 ${ytaskList.length} 任务 可做 ${taskList.length} 任务 ${claimList.length} 任务可领取奖励`);
}

async function dotask(tasklist, aqcCookie, exportkey) {
    for (var o of tasklist) {
        switch (o.title) {
            case 'CX10002': //每日签到
                Log('开始任务：' + oo[o.title]);
                await get(`usercenter/userSignAjax`);
                break;
            case 'CX10001': //每日登陆
                Log('开始任务：' + oo[o.title]);
                break;
            case 'CX11001': //查询企业
                Log('开始任务：' + oo[o.title]);
                let qys = ['苹果', '华为', '百度', '一个', '百事', '厚墨'];
                await get(`s/getHeadBrandAndPersonAjax?q=${encodeURI(qys[Math.floor(Math.random() * key.length)])}`);
                break;
            case 'CX11002': //查询老板
                Log('开始任务：' + oo[o.title]);
                await get(`person/relevantPersonalAjax?page=1&q=${encodeURI(rand())}&size=10`);
                break;
            case 'CX11003': //查询老赖
                Log('开始任务：' + oo[o.title]);
                await get(`c/dishonestAjax?q=${encodeURI(rand())}&t=8&s=10&p=1&f=%7B%22type%22:%221%22%7D`);
                break;
            case 'CX11004': //查询商标
                Log('开始任务：' + oo[o.title]);
                await get(`c/markproAjax?q=${encodeURI(rand())}&p=1&s=10&f=%7B%7D&o=%7B%7D`);
                break;
            case 'CX11005': //查询地图
                Log('开始任务：' + oo[o.title]);
                await get(`map/getAdvanceFilterListAjax?longitude=113.76343399&latitude=23.04302382&distance=2&page=1`);
                break;
            case 'CX11006': //浏览新闻
                Log('开始任务：' + oo[o.title]);
                await get('m/getYuqingDetailAjax?yuqingId=993090dcb7574be014599996098459e3');
                break;
            case 'CX11007': //浏览监控日报
                Log('开始任务：' + oo[o.title]);
                let jk = await get('zxcenter/monitorDailyReportListAjax?page=1&size=10');
                let list = jk.data.list ?? [];
                if (list) {
                    for (let p = 0; p < 2 && p < list.length; p++) {
                        await get(`zxcenter/monitorDailyReportDetailAjax?reportdate=${list[p].reportDate}`);
                    }
                }
                break;
            case 'CX11009': //查询关系
                Log('开始任务：' + oo[o.title]);
                await get(`relations/findrelationsAjax?from=e07a8ef1409bff3987f1b28d118ff826&to=6f5966de4af2eb29085ffbcc9cc0116a&pathNum=10`);
                break;
            case 'CX11010': //批量查询
                Log('开始任务：' + oo[o.title]);
                if (exportkey) {
                    await get(`batchquery/show?exportkey=${exportkey}`);
                } else {
                    Log('    配置 exportkey 后可执行批量查询任务！');
                }
                break;
            case 'CX12001': //添加监控
                Log('开始任务：' + oo[o.title]);
                for (let id of [29829264524016, 28696417032417, 31370200772422, 31242153386614]) {
                    await get(`zxcenter/addMonitorAjax?pid=${id}`);
                }
                await get(`zxcenter/addMonitorAjax?pid=29710155220353`);
                await sleep(1500);
                await get(`zxcenter/cancelMonitorAjax?pid=29710155220353`);
                break;
            case 'CX12002': //添加关注
                Log('开始任务：' + oo[o.title]);
                await get(`my/addCollectAjax`, `pid=34527616977197`, 'post');
                await get(`my/delCollectAjax`, `pid=34527616977197`, 'post');
                break;
            case 'CX12005': //分享好友
                Log('开始任务：' + oo[o.title]);
                let shres = await get(`usercenter/getShareUrlAjax`);
                let uid = shres.data.match(/uid=(.+)/);
                if (uid) {
                    uid = uid[1];
                    headers['cookie'] = '';
                    let time = Date.now();
                    headers['referer'] = 'https://' + shres.data + '&VNK=' + time;
                    headers['Zx-Open-Url'] = 'https://' + shres.data + '&VNK=' + time;
                    await get(`m/?uid=${uid}`);
                    headers['Zx-Open-Url'] = null;
                    headers['referer'] = 'https://aiqicha.baidu.com';
                    await get(`m/getuserinfoAjax?uid=${uid}`);
                    headers.cookie = aqcCookie;
                }
                break;
            case 'CX12007': //高级搜索
                Log('开始任务：' + oo[o.title]);
                await get(`search/advanceSearchAjax?q=${encodeURI(rand())}&t=11&p=1&s=10&o=0&f=%7B%22searchtype%22:[%221%22]%7D`);
                break;
            case 'CX12008': //高级筛选
                Log('开始任务：' + oo[o.title]);
                await get(`search/advanceFilterAjax?q=%E7%A6%8F%E5%B7%9E%E6%AF%8F%E6%97%A5&t=0&p=1&s=10&o=0`);
                break;
            case 'CX12009': //浏览互动
                Log('开始任务：' + oo[o.title]);
                let HomeQuestionres = await get('smart/getHomeQuestionListAjax?page=2&size=10&type=recommend');
                if (HomeQuestionres.status == 0) {
                    let qdetail = HomeQuestionres.data.list[Math.floor(Math.random() * HomeQuestionres.data.list.length)];
                    nid = qdetail.nid ?? '1851233986328193016';
                    await get(`smart/questionDetailAjax?nid=${nid}`);
                }
                break;
            case 'CX12011': //点赞观点
                Log('开始任务：' + oo[o.title]);
                nid = nid ?? '1851233986328193016';
                let qCListres = await get(`smart/questionCommentListAjax?nid=${nid}`);
                if (qCListres.status == 0) {
                    let pList = qCListres.data.list;
                    let randomkey = Math.floor(Math.random() * pList.length);
                    let pid = pList[randomkey].reply_id;
                    await get(`smart/updownAjax?undoType=0&clientType=app&nid=${nid}&parentId=${pid}`);
                }
                break;
            default:
                break;
        }
        let t = Math.round(Math.random() * 1000 * (60 - 20) * 2) + 10 * 1000;
        Log(`随机延迟 ${t / 1000} 秒：`);
        await sleep(t);
    }
}

function Log(info) {
    console.log(info);
    desp = desp + '\n' + info;
    return desp;
}

module.exports = aqc;
