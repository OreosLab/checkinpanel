/*
* @url: https://raw.githubusercontent.com/Wenmoux/checkbox/master/scripts/aiqicha.js
* @author: wenmoux
37 0-23/8 * * * ck_aiqicha.js
*/
const $ = new Env("爱企查");
const axios = require("axios");
const get_data = require('./utils');
const notify = $.isNode() ? require('./notify') : '';
const headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36",
    referer: "https://aiqicha.baidu.com/m/s?t=3&q=%E5%B0%8F%E7%B1%B3&VNK=e73b55ef",
    "X-Requested-With": "XMLHttpRequest",
    "Host": "aiqicha.baidu.com",
    cookie: ""
};
var sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
var desp = "";
let cookieAQCs = get_data().AQC;

aqc();

function rand() {
    let key = ["苹果", "华为", "百度", "一个", "暴风", "王者"]
    let i = Math.floor((Math.random() * key.length))
    return key[i]
}
let oo = {
    CX10002: "每日签到",
    CX10001: "每日登陆",
    CX11001: "查询企业",
    CX11002: "查询老板",
    CX11003: "查询老赖",
    CX11004: "查询商标",
    CX11005: "查询地图",
    CX11006: "浏览新闻",
    CX11007: "浏览监控日报",
    CX11009: "查询关系",
    CX11010: "批量查询",
    CX12001: "添加监控",
    CX12002: "添加关注",
    CX12005: "分享任务",
    CX12006: "邀请任务",
    CX12007: "高级搜索",
    CX12008: "高级筛选"
}

function get(api, method, data) {
    return new Promise(async (resolve) => {
        try {
            let url = `https://aiqicha.baidu.com/${api}`
            if (method == "get") res = await axios.get(url, {
                headers
            })
            if (method == "post") res = await axios.post(url, data, {
                headers
            })
            if (res.data.status == 0) Log("    操作成功")
            else Log("    " + res.data.msg)
            resolve(res.data)
        } catch (err) {
            Log(err)
        }
        resolve();
    });
}

async function getaskList() {
    let tres = await get("usercenter/checkTaskStatusAjax", "get")
    let obj = tres.data
    if (tres.status == 0) {
        Object.keys(obj).forEach(function (key) {
            if (oo[key]) {
                let task = obj[key]
                task.title = key
                alltaskList.push(task)
                if (task.count == task.totalcount) ytaskList.push(task)
                if (task.canClaim != 0) claimList.push(key)
                if (task.count != task.totalcount) taskList.push(task)
            }
        });
    }
    Log(`共 ${alltaskList.length}任务 已完成 ${ytaskList.length} 任务 可做 ${taskList.length}任务 ${claimList.length}任务可领取奖励`)
}

async function dotask(taskList, exportkey) {
    for (var o of taskList) {
        switch (o.title) {
            case "CX10002": //每日签到
                Log("开始任务：" + oo[o.title])
                await get(`usercenter/userSignAjax`, "get")
                break
            case "CX10001": //每日登陆
                Log("开始任务：" + oo[o.title])
                break
            case "CX11001": //查询企业 
                Log("开始任务：" + oo[o.title])
                await get(`s/getHeadBrandAndPersonAjax?q=${encodeURI(rand())}`, "get")
                await sleep(500)
                break
            case "CX11002": //查询老板 
                Log("开始任务：" + oo[o.title])
                await get(`person/relevantPersonalAjax?page=1&q=${encodeURI(rand())}&size=10`, "get")
                await sleep(500)
                break
            case "CX11003": //查询老赖
                Log("开始任务：" + oo[o.title])
                await get(`c/dishonestAjax?q=${encodeURI(rand())}&t=8&s=10&p=1&f=%7B%22type%22:%221%22%7D`, "get")
                await sleep(500)
                break
            case "CX11004": //查询商标
                Log("开始任务：" + oo[o.title])
                await get(`c/markproAjax?q=${encodeURI(rand())}&p=1&s=10&f=%7B%7D&o=%7B%7D`, "get")
                await sleep(500)
                break
            case "CX11005": //查询地图
                Log("开始任务：" + oo[o.title])
                await get(`map/getAdvanceFilterListAjax?longitude=113.76343399&latitude=23.04302382&distance=2&page=1`, "get")
                await sleep(500)
                break
            case "CX11006": //浏览新闻
                Log("开始任务：" + oo[o.title])
                await get("m/getYuqingDetailAjax?yuqingId=993090dcb7574be014599996098459e3", "get")
                break
            case "CX11007": //浏览监控日报
                Log("开始任务：" + oo[o.title])
                let jk = await get("zxcenter/monitorDailyReportListAjax?page=1&size=10", "get")
                let list = jk.data.list
                if (list) {
                    for (p = 0; p < 2 && p < list.length; p++) {
                        await get(`zxcenter/monitorDailyReportDetailAjax?reportdate=${list[p].reportDate}`, "get")
                    }
                }
                break
            case "CX11009": //查询关系
                Log("开始任务：" + oo[o.title])
                await get(`relations/findrelationsAjax?from=e07a8ef1409bff3987f1b28d118ff826&to=6f5966de4af2eb29085ffbcc9cc0116a&pathNum=10`, "get")
                await sleep(500)
                break
            case "CX11010": //批量查询 
                Log("开始任务：" + oo[o.title])
                if (exportkey) {
                    await get(`batchquery/show?exportkey=${exportkey}`, "get")
                    await sleep(500)
                } else {
                    Log("    配置 exportkey 后可执行批量查询任务！")
                }
                break
            case "CX12001": //添加监控
                Log("开始任务：" + oo[o.title])
                for (id of [29829264524016, 28696417032417, 31370200772422, 31242153386614]) {
                    await get(`zxcenter/addMonitorAjax?pid=${id}`, "get")
                }
                await get(`zxcenter/addMonitorAjax?pid=29710155220353`, "get")
                await get(`zxcenter/cancelMonitorAjax?pid=29710155220353`, "get")
                await sleep(500)
                break
            case "CX12002": //添加关注
                Log("开始任务：" + oo[o.title])
                await get(`my/addCollectAjax`, "post", `pid=34527616977197`)
                await get(`my/delCollectAjax`, "post", `pid=34527616977197`)
                await sleep(500)
                break
            case "CX12005": //分享好友
                Log("开始任务：" + oo[o.title])
                let shres = await get(`usercenter/getShareUrlAjax`, "get")
                uid = shres.data.match(/uid=(.+)/)
                if (uid) {
                    uid = uid[1]
                    headers["cookie"] = ""
                    let t = Date.now()
                    headers["referer"] = "https://" + shres.data + "&VNK=" + t
                    headers["Zx-Open-Url"] = "https://" + shres.data + "&VNK=" + t
                    await get(`m/?uid=${uid}`, "get")
                    await get(`m/getuserinfoAjax?uid=${uid}`, "get")
                    headers.cookie = aqcCookie
                    await sleep(500)
                }
                break
            case "CX12007": //高级搜索
                Log("开始任务：" + oo[o.title])
                await get(`search/advanceSearchAjax?q=${encodeURI(rand())}&t=11&p=1&s=10&o=0&f=%7B%22searchtype%22:[%221%22]%7D`, "get")
                break
            case "CX12008": //高级筛选
                Log("开始任务：" + oo[o.title])
                await get(`search/advanceFilterAjax?q=%E7%A6%8F%E5%B7%9E%E6%AF%8F%E6%97%A5&t=0&p=1&s=10&o=0`, "get")
                break
            default:
                break
        }
        await sleep(500)
        Log("  去领取爱豆")
        let clres = await get(`zxcenter/claimUserTaskAjax?taskCode=${o.title}`, "get")
        if (clres.status == 0) Log(`  领取成功！获得${clres.data.totalScore}爱豆`)
    }
}

async function aqc() {
    msg = "【爱企查】："
    if (cookieAQCs) {
        Log("爱企查cookie数量：" + cookieAQCs.length)
        for (a = 0; a < cookieAQCs.length; a++) {
            aqcCookie = cookieAQCs[a].cookie
            exportkey = cookieAQCs[a].exportkey ? cookieAQCs[a].exportkey : ""
            headers.cookie = aqcCookie
            ytaskList = []
            taskList = []
            claimList = []
            alltaskList = []
            Log("\n========== [Account " + (a + 1) + "] Start ========== ")
            let logininfo = await get("m/getuserinfoAjax", "get")
            if (logininfo.data.isLogin == 1) {
                await getaskList()
                await dotask(taskList, exportkey)
                await dotask(taskList, exportkey)
                await sleep(500)
                claimList = []
                await getaskList()
                for (task of claimList) {
                    Log(`领取爱豆：${oo[task]}`)
                    let clres = await get(`zxcenter/claimUserTaskAjax?taskCode=${task}`, "get")
                    if (clres.status == 0) Log(`  领取成功！获得${clres.data.totalScore}爱豆`)
                }
                Log("去查询爱豆积分")
                let userinfo = await get("usercenter/getvipinfoAjax", "get")
                msg += `账号${a+1} 【${logininfo.data.userName}】 共${userinfo.data.consume}爱豆\n`
            } else {
                msg = "cookie已失效"
            }
        }
    } else {
        msg += "请填写百度爱企查cookies(同百度贴吧"
    }
    Log(msg)
    notify.sendNotify("爱企查", desp)
}

function Log(info) {
    console.log(info)
    desp = desp + "\n" + info
    return desp
}

// prettier-ignore @formatter:off
function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), Log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), Log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }
