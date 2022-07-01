// @grant  require
// @grant  sudo
const parser = require('/usr/local/app/script/Shell/checkinpanel/node_modules/cron-parser');

let taskinfo = $task.info();
let tasklist = [];
let namelist = [];
let idlist = [];
let excluding = $store.get('EXRAND', 'array');

main();

async function main() {
    await getRepList();
    await filterList();
    await getNameList();
    for (let i in tasklist) {
        tasklist[i]['time'] = await modifyTime(tasklist[i]['time']);
    }
    await replaceTask();
    startTask();
}

async function getRepList() {
    for (let i in taskinfo) {
        if (taskinfo[i]['type'] == 'cron' && taskinfo[i]['running'] == true && taskinfo[i]['name'] != '随机定时') {
            tasklist.push(taskinfo[i]);
        }
    }
}

async function filterList() {
    if (excluding != undefined) {
        console.log('🗑 排除 EXRAND 变量列表中的任务名');
        tasklist = tasklist.filter(function (i) {
            return excluding.indexOf(i['name']) == -1;
        });
    }
}

async function getNameList() {
    for (let i in tasklist) {
        namelist.push(tasklist[i]['name']);
        idlist.push(tasklist[i]['id']);
    }
}

async function modifyTime(cron) {
    let interval = parser.parseExpression(cron);
    let fields = JSON.parse(JSON.stringify(interval.fields));
    fields.minute = [Math.floor(Math.random() * 60)];
    if (fields.hour.length == 1) {
        fields.hour = [Math.floor(Math.random() * 17 + 6)];
    } else {
        let add = Math.floor(Math.random() * (fields.hour[1] - fields.hour[0]));
        for (let i in fields.hour) {
            fields.hour[i] = fields.hour[i] + add;
            if (fields.hour[i] >= 24) {
                fields.hour[i] = fields.hour[i] - 24;
            }
        }
    }
    let modifiedInterval = parser.fieldsToExpression(fields);
    let cronString = modifiedInterval.stringify();
    return cronString;
}

async function replaceTask() {
    console.log('⏱ 开始修改运行中的 cron 任务...');
    let res = $task.add(tasklist);
    console.log(res);
}

async function startTask() {
    console.log('🎈 启动之前处于运行中的 cron 任务...');
    $task.start(idlist);
    console.log('✅ 开始保存修改后的任务列表...');
    let saveres = $task.save();
    console.log(saveres);
}
