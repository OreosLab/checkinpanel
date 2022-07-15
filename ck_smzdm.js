/*
* @url: https://raw.githubusercontent.com/Tsukasa007/my_script/master/smzdm_mission.js
29 0-23/8 * * * ck_smzdm.js
*/

const utils = require('./utils');
const Env = utils.Env;
const MagicJS = utils.MagicJS;
const getData = utils.getData;

const $ = new Env('什么值得买');
const notify = $.isNode() ? require('./notify') : '';
const magicJS = MagicJS('什么值得买', 'INFO');
const COOKIES_SMZDM = getData().SMZDM;

const clickGoBuyMaxTimes = 12; // 好价点击去购买的次数
const clickLikeProductMaxTimes = 7; // 好价点值次数
const clickLikeArticleMaxTimes = 7; // 好文点赞次数
const clickFavArticleMaxTimes = 7; // 好文收藏次数

smzdm();

async function smzdm() {
    let content = '';
    let result = [];

    if (!!COOKIES_SMZDM === false) {
        content += '\n没有读取到什么值得买有效cookie，请访问zhiyou.smzdm.com进行登录';
        result.push(content);
    } else {
        for (var i = 0; i < COOKIES_SMZDM.length; i++) {
            try {
                $.index = i + 1;
                content += '\n======== [Cookie ' + $.index + '] Start ======== \n';
                magicJS.log('\n======== [Cookie ' + $.index + '] Start ======== ');
                let smzdmCookie = COOKIES_SMZDM[i].cookie;
                // 任务完成情况
                let clickGoBuyTimes = 0;
                let clickLikePrductTimes = 0;
                let clickLikeArticleTimes = 0;
                let clickFavArticleTimes = 0;

                // 查询签到前用户数据
                let [nickName, , beforeVIPLevel, beforeHasCheckin, , beforeNotice, , , beforePoint, beforeGold, beforeSilver] = await WebGetCurrentInfo(
                    smzdmCookie
                );
                if (!nickName) {
                    magicJS.notify('什么值得买', '', '❌Cookie过期或接口变化，请尝试重新登录');
                    magicJS.done();
                } else {
                    let [, , , beforeExp] = await WebGetCurrentInfoNewVersion(smzdmCookie);
                    magicJS.logInfo(
                        `昵称：${nickName}\nWeb端签到状态：${beforeHasCheckin}\n签到前等级${beforeVIPLevel}，积分${beforePoint}，经验${beforeExp}，金币${beforeGold}，碎银子${beforeSilver}， 未读消息${beforeNotice}`
                    );

                    // 每日抽奖
                    let activeId = await GetLotteryActiveId(smzdmCookie);
                    if (activeId) {
                        content += await LotteryDraw(smzdmCookie, activeId);
                    }

                    // 获取去购买和好价Id列表
                    let [, [goBuyList = [], likProductList = []]] = await magicJS.attempt(magicJS.retry(GetProductList, 5, 1000)(), [[], []]);
                    // 获取好文列表
                    let [, articleList = []] = await magicJS.attempt(magicJS.retry(GetDataArticleIdList, 5, 1000)(), []);

                    // 好价点击去购买，Web端点击已无奖励，放弃
                    const clickGoBuyAsync = async () => {
                        let clickGoBuyList = goBuyList.splice(0, clickGoBuyMaxTimes);
                        if (clickGoBuyList.length > 0) {
                            for (let a = 0; a < clickGoBuyList.length; a++) {
                                await ClickGoBuyButton(smzdmCookie, clickGoBuyList[a]);
                                magicJS.logInfo(`完成第${a + 1}次“每日去购买”任务，点击链接：\n${clickGoBuyList[a]}`);
                                clickGoBuyTimes += 1;
                                await magicJS.sleep(3100);
                            }
                        }
                    };

                    // 好价点值
                    const clickLikeProductAsync = async () => {
                        let clickLikeProductList = likProductList.splice(0, clickLikeProductMaxTimes);
                        if (clickLikeProductList.length > 0) {
                            for (let a = 0; a < clickLikeProductList.length; a++) {
                                await ClickLikeProduct(smzdmCookie, clickLikeProductList[a]);
                                magicJS.logInfo(`完成第${a + 1}次“好价点值”任务，好价Id：${clickLikeProductList[a]}`);
                                clickLikePrductTimes += 1;
                                await magicJS.sleep(3100);
                            }
                        }
                    };

                    // 好文点赞
                    const clickLikeArticleAsync = async () => {
                        let likeArticleList = articleList.splice(0, clickLikeArticleMaxTimes);
                        if (likeArticleList.length > 0) {
                            for (let a = 0; a < likeArticleList.length; a++) {
                                await ClickLikeArticle(smzdmCookie, likeArticleList[a]);
                                magicJS.logInfo(`完成第${a + 1}次“好文点赞”任务，好文Id：${likeArticleList[a]}`);
                                clickLikeArticleTimes += 1;
                                await magicJS.sleep(3100);
                            }
                        }
                    };

                    // 好文收藏
                    const clickFavArticleAsync = async () => {
                        let favArticleList = articleList.splice(0, clickFavArticleMaxTimes);
                        if (favArticleList.length > 0) {
                            // 好文收藏
                            for (let a = 0; a < favArticleList.length; a++) {
                                await ClickFavArticle(smzdmCookie, articleList[a]);
                                magicJS.logInfo(`完成第${a + 1}次“好文收藏”任务，好文Id：${articleList[a]}`);
                                clickFavArticleTimes += 1;
                                await magicJS.sleep(3100);
                            }
                            // 取消收藏
                            for (let a = 0; a < favArticleList.length; a++) {
                                await ClickFavArticle(smzdmCookie, articleList[a]);
                                magicJS.logInfo(`取消第${a + 1}次“好文收藏”任务的好文，好文Id：${articleList[a]}`);
                                await magicJS.sleep(3100);
                            }
                        }
                    };

                    await Promise.all([clickGoBuyAsync(), clickLikeProductAsync()]);
                    await Promise.all([clickLikeArticleAsync(), clickFavArticleAsync()]);

                    // 查询签到后用户数据
                    await magicJS.sleep(3000);
                    let [, , afterVIPLevel, afterHasCheckin, , afterNotice, , , afterPoint, afterGold, afterSilver] = await WebGetCurrentInfo(smzdmCookie);
                    let [, afteruserPointList, , afterExp] = await WebGetCurrentInfoNewVersion(smzdmCookie);
                    magicJS.logInfo(
                        `昵称：${nickName}\nWeb端签到状态：${afterHasCheckin}\n签到后等级${afterVIPLevel}，积分${afterPoint}，经验${afterExp}，金币${afterGold}，碎银子${afterSilver}，未读消息${afterNotice}`
                    );

                    // 通知内容
                    if (afterExp && beforeExp) {
                        let addPoint = afterPoint - beforePoint;
                        let addExp = afterExp - beforeExp;
                        let addGold = afterGold - beforeGold;
                        let addSilver = afterSilver - beforeSilver;
                        content += !!content ? '\n' : '';
                        content +=
                            '积分' +
                            afterPoint +
                            (addPoint > 0 ? '(+' + addPoint + ')' : '') +
                            ' 经验' +
                            afterExp +
                            (addExp > 0 ? '(+' + addExp + ')' : '') +
                            ' 金币' +
                            afterGold +
                            (addGold > 0 ? '(+' + addGold + ')' : '') +
                            '\n' +
                            '碎银子' +
                            afterSilver +
                            (addSilver > 0 ? '(+' + addSilver + ')' : '') +
                            ' 未读消息' +
                            afterNotice;
                    }

                    content += `\n点值 ${clickLikePrductTimes}/${clickLikeProductMaxTimes} 去购买 ${clickGoBuyTimes}/${clickGoBuyMaxTimes}\n点赞 ${clickLikeArticleTimes}/${clickLikeArticleMaxTimes} 收藏 ${clickLikeArticleTimes}/${clickFavArticleTimes}`;

                    content += !!content ? '\n' : '';
                    if (afteruserPointList.length > 0) {
                        content += '用户近期经验变动情况(有延迟)：';
                        afteruserPointList.forEach((element) => {
                            content += `\n${element['time']} ${element['detail']}`;
                        });
                        content += '\n如经验值无变动，请更新Cookie。';
                    } else {
                        content += '没有获取到用户近期的经验变动情况';
                    }
                }
            } catch (err) {
                magicJS.logError(`执行任务出现异常：${err}`);
                content += '❌执行任务出现，请查阅日志';
            }
            content += '\n======== [Cookie ' + $.index + '] End  ======== \n';
            magicJS.log('\n======== [Cookie ' + $.index + '] End  ======== \n');
            result.push(content);
        }
    }
    magicJS.done();
    notify.sendNotify('什么值得买', result.join('\n'));
    return '什么值得买' + '\n\n' + result.join('\n');
}

// 签到
function SignIn(cookie) {
    return new Promise((resolve) => {
        let options = {
            url: 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin',
            headers: {
                Accept: '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-cn',
                Connection: 'keep-alive',
                Cookie: cookie,
                Host: 'zhiyou.smzdm.com',
                Referer: 'https://m.smzdm.com/zhuanti/life/choujiang/',
                'User-Agent':
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/smzdm 9.9.0 rv:91 (iPhone 11 Pro Max; iOS 14.2; zh_CN)/iphone_smzdmapp/9.9.0/wkwebview/jsbv_1.0.0',
            },
        };
        magicJS.get(options, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`每日签到，请求异常：${err}`);
                resolve('');
            } else {
                magicJS.log(`每日签到成功`);
                resolve('');
            }
        });
    });
}

// 获取点击去购买和点值的链接
function GetProductList() {
    return new Promise((resolve, reject) => {
        let getGoBuyOptions = {
            url: 'https://faxian.smzdm.com/',
            headers: {
                Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'max-age=0',
                Connection: 'keep-alive',
                Host: 'www.smzdm.com',
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
            },
            body: '',
        };
        magicJS.get(getGoBuyOptions, (err, resp, data) => {
            if (err) {
                reject(err);
            } else {
                // 获取每日去购买的链接
                let goBuyList = data.match(/https?:\/\/go\.smzdm\.com\/\w*\/[^"']*_0/gi);
                if (!!goBuyList) {
                    // 去除重复的商品链接
                    let goBuyDict = {};
                    goBuyList.forEach((element) => {
                        let productCode = element.match(/https?:\/\/go\.smzdm\.com\/\w*\/([^"']*_0)/)[1];
                        goBuyDict[productCode] = element;
                    });
                    goBuyList = Object.values(goBuyDict);
                    magicJS.logDebug(`当前获取的每日去购买链接：${JSON.stringify(goBuyList)}`);
                } else {
                    goBuyList = [];
                }

                // 获取每日点值的链接
                let productUrlList = data.match(/https?:\/\/www\.smzdm\.com\/p\/\d*/gi);
                let likeProductList = [];
                if (!!productUrlList) {
                    productUrlList.forEach((element) => {
                        likeProductList.push(element.match(/https?:\/\/www\.smzdm\.com\/p\/(\d*)/)[1]);
                    });
                }
                resolve([goBuyList, likeProductList]);
            }
        });
    });
}

// 获取点赞和收藏的好文Id
function GetDataArticleIdList() {
    return new Promise((resolve, reject) => {
        let getArticleOptions = {
            url: 'https://post.smzdm.com/',
            headers: {
                Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                Host: 'post.smzdm.com',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
            },
            body: '',
        };
        magicJS.get(getArticleOptions, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`获取好文列表失败，请求异常：${err}`);
                reject('GetArticleListErr');
            } else {
                try {
                    let articleList = data.match(/data-article=".*" data-type="zan"/gi);
                    let result = [];
                    articleList.forEach((element) => {
                        result.push(element.match(/data-article="(.*)" data-type="zan"/)[1]);
                    });
                    resolve(result);
                } catch (e) {
                    magicJS.logWarning(`获取好文列表失败，执行异常：${e}`);
                    reject('GetArticleListErr');
                }
            }
        });
    });
}

// 点击去购买
function ClickGoBuyButton(cookie, url) {
    return new Promise((resolve) => {
        let clickGoBuyOptions = {
            url: url,
            headers: {
                Cookie: cookie,
            },
        };
        magicJS.get(clickGoBuyOptions, (err, resp, data) => {
            resolve();
        });
    });
}

// 好价点值
function ClickLikeProduct(cookie, articleId) {
    return new Promise((resolve) => {
        let ClickLikeProductOptions = {
            url: 'https://zhiyou.smzdm.com/user/rating/ajax_add',
            headers: {
                Accept: 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                Host: 'zhiyou.smzdm.com',
                Origin: 'https://faxian.smzdm.com',
                Referer: 'https://faxian.smzdm.com/',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
                Cookie: cookie,
            },
            body: `article_id=${articleId}&channel_id=3&rating=1&client_type=PC&event_key=%E7%82%B9%E5%80%BC&otype=%E5%80%BC&aid=${articleId}&p=16&cid=2&source=%E6%97%A0&atp=3&tagID=%E6%97%A0&sourcePage=https%3A%2F%2Ffaxian.smzdm.com%2F&sourceMode=%E6%97%A0`,
        };
        magicJS.post(ClickLikeProductOptions, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`好价${articleId}点值失败，请求异常：${articleId}`);
                resolve(false);
            } else {
                try {
                    let obj = JSON.parse(data);
                    if (obj.error_code == 0) {
                        magicJS.logDebug(`好价${articleId}点值成功`);
                        resolve(true);
                    } else if (obj.error_code == 1) {
                        magicJS.logDebug(`好价${articleId}点值重复点值`);
                        resolve(true);
                    } else {
                        magicJS.logWarning(`好价${articleId}点值失败，接口响应异常：${data}`);
                        resolve(false);
                    }
                } catch (e) {
                    magicJS.logWarning(`好价${articleId}点值失败，执行异常：${articleId}`);
                    resolve(false);
                }
            }
        });
    });
}

// 好文点赞
function ClickLikeArticle(cookie, articleId) {
    return new Promise((resolve) => {
        let ClickLikeProductOptions = {
            url: 'https://zhiyou.smzdm.com/user/rating/ajax_add',
            headers: {
                Accept: 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                Host: 'zhiyou.smzdm.com',
                Origin: 'https://post.smzdm.com',
                Referer: 'https://post.smzdm.com/',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
                Cookie: cookie,
            },
            body: `article_id=${articleId}&channel_id=11&rating=1&client_type=PC&event_key=%E7%82%B9%E5%80%BC&otype=%E7%82%B9%E8%B5%9E&aid=${articleId}&p=2&cid=11&source=%E6%97%A0&atp=76&tagID=%E6%97%A0&sourcePage=https%3A%2F%2Fpost.smzdm.com%2F&sourceMode=%E6%97%A0`,
        };
        magicJS.post(ClickLikeProductOptions, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`好文${articleId}点赞失败，请求异常：${articleId}`);
                resolve(false);
            } else {
                try {
                    let obj = JSON.parse(data);
                    if (obj.error_code == 0) {
                        magicJS.logDebug(`好文${articleId}点赞成功`);
                        resolve(true);
                    } else if (obj.error_code == 1 && obj.error_msg == '已喜欢') {
                        magicJS.logDebug(`好文${articleId}点赞失败，重复点值。`);
                        resolve(false);
                    } else {
                        magicJS.logWarning(`好文${articleId}点赞失败，接口响应异常：${data}`);
                        resolve(false);
                    }
                } catch (e) {
                    magicJS.logWarning(`好文${articleId}点赞失败，请求异常：${e}`);
                    resolve(false);
                }
            }
        });
    });
}

// 好文收藏/取消收藏
function ClickFavArticle(cookie, articleId) {
    return new Promise((resolve) => {
        let options = {
            url: 'https://zhiyou.smzdm.com/user/favorites/ajax_favorite',
            headers: {
                Accept: 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                Host: 'zhiyou.smzdm.com',
                Origin: 'https://post.smzdm.com',
                Referer: 'https://post.smzdm.com/',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41',
                Cookie: cookie,
            },
            body: `article_id=${articleId}&channel_id=11&client_type=PC&event_key=%E6%94%B6%E8%97%8F&otype=%E6%94%B6%E8%97%8F&aid=${articleId}&cid=11&p=2&source=%E6%97%A0&atp=76&tagID=%E6%97%A0&sourcePage=https%3A%2F%2Fpost.smzdm.com%2F&sourceMode=%E6%97%A0`,
        };
        magicJS.post(options, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`好文${articleId}收藏失败，请求异常：${articleId}`);
                resolve(false);
            } else {
                try {
                    let obj = JSON.parse(data);
                    if (obj.error_code == 0) {
                        magicJS.logDebug(`好文${articleId}收藏成功`);
                        resolve(true);
                    } else if (obj.error_code == 2) {
                        magicJS.logDebug(`好文${articleId}取消收藏成功`);
                        resolve(true);
                    } else {
                        magicJS.logWarning(`好文${articleId}收藏失败，接口响应异常：${data}`);
                        resolve(false);
                    }
                } catch (e) {
                    magicJS.logWarning(`好文${articleId}收藏失败，请求异常：${e}`);
                    resolve(false);
                }
            }
        });
    });
}

// 获取每日抽奖active_id
function GetLotteryActiveId(cookie) {
    return new Promise((resolve) => {
        let options = {
            url: 'https://m.smzdm.com/zhuanti/life/choujiang/',
            headers: {
                Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-cn',
                Connection: 'keep-alive',
                Cookie: cookie,
                Host: 'm.smzdm.com',
                'User-Agent':
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/smzdm 9.9.6 rv:93.4 (iPhone13,4; iOS 14.5; zh_CN)/iphone_smzdmapp/9.9.6/wkwebview/jsbv_1.0.0',
            },
        };
        magicJS.get(options, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`获取每日抽奖Id失败，请求异常：${err}`);
                resolve('获取每日抽奖Id失败，请求异常');
            } else {
                try {
                    let activeId = /name\s?=\s?\"lottery_activity_id\"\s+value\s?=\s?\"([a-zA-Z0-9]*)\"/.exec(data);
                    if (activeId) {
                        resolve(activeId[1]);
                    } else {
                        magicJS.logWarning(`获取每日抽奖activeId失败`);
                        resolve('');
                    }
                } catch (e) {
                    magicJS.logWarning(`获取每日抽奖activeId失败，请求异常：${e}`);
                    resolve('');
                }
            }
        });
    });
}

// 每日抽奖
function LotteryDraw(cookie, activeId) {
    return new Promise((resolve) => {
        let options = {
            url: `https://zhiyou.smzdm.com/user/lottery/jsonp_draw?callback=jQuery34109305207178886287_${new Date().getTime()}&active_id=${activeId}&_=${new Date().getTime()}`,
            headers: {
                Accept: '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-cn',
                Connection: 'keep-alive',
                Cookie: cookie,
                Host: 'zhiyou.smzdm.com',
                Referer: 'https://m.smzdm.com/zhuanti/life/choujiang/',
                'User-Agent':
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/smzdm 9.9.0 rv:91 (iPhone 11 Pro Max; iOS 14.2; zh_CN)/iphone_smzdmapp/9.9.0/wkwebview/jsbv_1.0.0',
            },
        };
        magicJS.get(options, (err, resp, data) => {
            if (err) {
                magicJS.logWarning(`每日抽奖失败，请求异常：${err}`);
                resolve('每日抽奖失败，请求异常');
            } else {
                try {
                    let newData = /\((.*)\)/.exec(data);
                    let obj = JSON.parse(newData[1]);
                    if (obj.error_code === 0 || obj.error_code === 1 || obj.error_code === 4) {
                        magicJS.logInfo(`每日抽奖结果：${obj.error_msg}`);
                        resolve(obj.error_msg);
                    } else {
                        magicJS.logWarning(`每日抽奖失败，接口响应异常：${data}`);
                        resolve('每日抽奖失败，接口响应异常');
                    }
                } catch (e) {
                    magicJS.logWarning(`每日抽奖失败，请求异常：${e}`);
                    resolve('每日抽奖失败，请求异常');
                }
            }
        });
    });
}

// 获取用户信息，新版
function WebGetCurrentInfoNewVersion(smzdmCookie) {
    return new Promise((resolve) => {
        let options = {
            url: 'https://zhiyou.smzdm.com/user/exp/',
            headers: {
                Cookie: smzdmCookie,
            },
            body: '',
        };
        magicJS.get(options, (err, resp, data) => {
            if (err) {
                magicJS.logError(`获取用户信息失败，异常信息：${err}`);
                resolve([null, null, null, null, null, null, null]);
            } else {
                try {
                    // 获取用户名
                    let userName = data.match(/info-stuff-nickname.*zhiyou\.smzdm\.com\/user[^<]*>([^<]*)</)[1].trim();
                    // 获取近期经验值变动情况
                    let pointTimeList = data.match(/<div class="scoreLeft">(.*)<\/div>/gi);
                    let pointDetailList = data.match(/<div class=['"]scoreRight ellipsis['"]>(.*)<\/div>/gi);
                    let minLength = pointTimeList.length > pointDetailList.length ? pointDetailList.length : pointTimeList.length;
                    let userPointList = [];
                    for (let i = 0; i < minLength; i++) {
                        userPointList.push({
                            time: pointTimeList[i].match(/\<div class=['"]scoreLeft['"]\>(.*)\<\/div\>/)[1],
                            detail: pointDetailList[i].match(/\<div class=['"]scoreRight ellipsis['"]\>(.*)\<\/div\>/)[1],
                        });
                    }
                    // 获取用户资源
                    let assetsNumList = data.match(/assets-part[^<]*>(.*)</gi);
                    let points = assetsNumList[0].match(/assets-num[^<]*>(.*)</)[1]; // 积分
                    let experience = assetsNumList[2].match(/assets-num[^<]*>(.*)</)[1]; // 经验
                    let gold = assetsNumList[4].match(/assets-num[^<]*>(.*)</)[1]; // 金币
                    let prestige = 0;
                    let silver = assetsNumList[6].match(/assets-num[^<]*>(.*)</)[1]; // 碎银子
                    resolve([userName, userPointList, Number(points), Number(experience), Number(gold), Number(prestige), Number(silver)]);
                } catch (e) {
                    magicJS.logError(`获取用户信息失败，异常信息：${e}`);
                    resolve([null, null, null, null, null, null, null]);
                }
            }
        });
    });
}

// 获取用户信息
function WebGetCurrentInfo(smzdmCookie) {
    return new Promise((resolve) => {
        let webGetCurrentInfo = {
            url: `https://zhiyou.smzdm.com/user/info/jsonp_get_current?with_avatar_ornament=1&callback=jQuery112403507528653716241_${new Date().getTime()}&_=${new Date().getTime()}`,
            headers: {
                Accept: 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                Connection: 'keep-alive',
                DNT: '1',
                Host: 'zhiyou.smzdm.com',
                Referer: 'https://zhiyou.smzdm.com/user/',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                Cookie: smzdmCookie,
            },
        };
        magicJS.get(webGetCurrentInfo, (err, resp, data) => {
            try {
                let obj = JSON.parse(/\((.*)\)/.exec(data)[1]);
                if (obj['smzdm_id'] !== 0) {
                    resolve([
                        obj['nickname'], // 昵称
                        `https:${obj['avatar']}`, // 头像
                        obj['vip_level'], // 新版VIP等级
                        obj['checkin']['has_checkin'], // 是否签到
                        Number(obj['checkin']['daily_checkin_num']), // 连续签到天数
                        Number(obj['unread']['notice']['num']), // 未读消息
                        Number(obj['level']), // 旧版等级
                        Number(obj['exp']), // 旧版经验
                        Number(obj['point']), // 积分
                        Number(obj['gold']), // 金币
                        Number(obj['silver']), // 碎银子
                    ]);
                } else {
                    magicJS.logWarning(`获取用户信息异常，Cookie过期或接口变化：${data}`);
                    resolve([null, null, null, null, null, false, null, null]);
                }
            } catch (e) {
                magicJS.logError(`获取用户信息异常，代码执行异常：${e}，接口返回数据：${data}`);
                resolve([null, null, null, null, null, false, null, null]);
            }
        });
    });
}

module.exports = smzdm;
