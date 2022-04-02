// @grant  sudo

// 查看当前任务数
console.log($task.status());
/*
--------------------
{ running: 13, total: 20, sub: 2 }
--------------------
*/

// 添加任务（具体任务格式参考 https://github.com/elecV2/elecV2P-dei/blob/master/docs/06-task.md）
let res = $task.add(
    [
        {
            name: '$task 添加的任务 1',
            type: 'cron',
            time: '12 15 18 * * *',
            job: {
                type: 'exec',
                target: 'pm2 ls',
            },
        },
        {
            name: '$task 添加的任务 2',
            type: 'cron',
            time: '12 15 18 * * *',
            job: {
                type: 'exec',
                target: 'pm2 ls',
            },
        },
    ],
    { type: 'replace' }
);
console.log('$task 添加任务结果', res);
/*
--------------------
>> success
$task 添加任务结果 {
    rescode: 0,
    message: 'TASK: $task 添加的任务 1 started\n TASK: $task 添加的任务 2 started'
  } 
>> failure
$task 添加任务结果 {
    rescode: 0,
    message: 'some task parameters may be invalid(please check docs: https://github.com/elecV2/elecV2P-dei/blob/master/docs/06-task.md)\n' +
      'some task parameters may be invalid(please check docs: https://github.com/elecV2/elecV2P-dei/blob/master/docs/06-task.md)'
  } 
--------------------
*/

// 如果需要添加多个任务，可使用 array 数组的形式
// 比如 $task.add([{}, {}], { type: 'replace' })
// 第二个参数 options 可省略。
// 如设置 type, 表示同名任务的更新方式。有三个有效值:
// - replace    替换原同名任务
// - addition   新增同名任务
// - skip       跳过添加同名任务

// 获取任务名及对应 taskid
let tnlist = $task.nameList();
console.log(tnlist);
/*
--------------------
{
  '清空日志': 'BPvOKSlv',
  '软更新升级': 'rswqs1uC',
  'Python安装(Docker下)': 'Au7FLiaY',
  '重启 elecV2P': 'xVrbflqZ',
  '任务添加并执行': 'qM9b9JAN',
  'Shell 指令远程任务': 'nbLrklPI',
  ...
}
--------------------
*/

// 返回的是类似于 { '任务名': taskid } 的 object
// 通过该 object，可使用任务名快速查找任务 id
// 如果任务列表不经常变化的话建议使用 $store.put 或 $cache 保存

// 开始任务
console.log($task.start('BPvOKSlv'));
/*
--------------------
{
    rescode: 0,
    message: '清空日志 is running',
    taskinfo: {
      name: '清空日志',
      type: 'cron',
      time: '30 18 23 * * *',
      job: {
        type: 'runjs',
        target: 'https://raw.githubusercontent.com/elecV2/elecV2P/master/script/JSFile/deletelog.js'
      },
      id: 'BPvOKSlv',
      running: true,
      group: 'Jyhniazi'
    }
} 
--------------------
*/

// 停止任务
console.log($task.stop(tnlist['清空日志'])); // 通过任务名查找任务 id
/*
--------------------
{
    rescode: 0,
    message: '清空日志 stopped',
    taskinfo: {
      name: '清空日志',
      type: 'cron',
      time: '30 18 23 * * *',
      job: {
        type: 'runjs',
        target: 'https://raw.githubusercontent.com/elecV2/elecV2P/master/script/JSFile/deletelog.js'
      },
      id: 'BPvOKSlv',
      running: false,
      group: 'Jyhniazi'
    }
}
--------------------
*/

// 删除任务
console.log($task.delete('BPvOKSlv'));
/*
--------------------
{ rescode: 0, message: 'TASK cron 清空日志 deleted' }
--------------------
*/

// 使用数组的形式传入 taskid，可批量开始/暂停/删除 定时任务
$task.start(['m8LWPxDc', 'ataskid', tnlist['$task 添加的任务'], 'jxwQOSJZ']);
// $task.stop(['taskid1', 'taskid2', ...])
// $task.delete(['taskid1', 'taskid2', ...])

// 查看某个任务信息
let taskinfo = $task.info('rswqs1uC'); // 查看所有任务信息 $task.info() 或者 $task.info('all')
console.log(taskinfo);
/*
--------------------
>> single
{
    name: '软更新升级',
    type: 'cron',
    time: '30 58 23 * * *',
    job: {
      type: 'runjs',
      target: 'https://raw.githubusercontent.com/elecV2/elecV2P/master/script/JSFile/softupdate.js'
    },
    id: 'rswqs1uC',
    running: true,
    group: 'Jyhniazi'
} 
--------------------
>> all  
{
    rswqs1uC: {
      name: '软更新升级',
      type: 'cron',
      time: '30 58 23 * * *',
      job: {
        type: 'runjs',
        target: 'https://raw.githubusercontent.com/elecV2/elecV2P/master/script/JSFile/softupdate.js'
      },
      id: 'rswqs1uC',
      running: true,
      group: 'Jyhniazi'
    },
    Au7FLiaY: {
      name: 'Python安装(Docker下)',
      type: 'schedule',
      time: '0',
      job: {
        type: 'runjs',
        target: 'https://raw.githubusercontent.com/elecV2/elecV2P/master/script/JSFile/python-install.js'
      },
      running: false,
      id: 'Au7FLiaY',
      group: 'Jyhniazi'
    },
    xVrbflqZ: {
      name: '重启 elecV2P',
      type: 'schedule',
      time: '0',
      job: { type: 'exec', target: 'pm2 restart elecV2P' },
      running: false,
      id: 'xVrbflqZ',
      group: 'Jyhniazi'
    },
    qM9b9JAN: {
      name: '任务添加并执行',
      type: 'schedule',
      time: '10',
      job: { type: 'exec', target: 'node -v' },
      running: false,
      id: 'qM9b9JAN',
      group: 'Jyhniazi'
    },
    nbLrklPI: {
      name: 'Shell 指令远程任务',
      type: 'schedule',
      time: '0',
      job: {
        type: 'exec',
        target: 'python3 https://raw.githubusercontent.com/elecV2/elecV2P/master/script/Shell/elecV2P-exam.py'
      },
      running: false,
      id: 'nbLrklPI',
      group: 'Jyhniazi'
    },
    WrOz0txU: {
      name: 'News',
      type: 'sub',
      job: {
        type: 'replace',
        target: 'https://raw.githubusercontent.com/Oreomeow/VIP/main/Tasks/News.json'
      },
      update_type: 'none'
    },
    FSEh4K9D: {
      name: 'Wool',
      type: 'group',
      note: '羊毛项目',
      bkcolor: '#3de1ad',
      collapse: true,
      total: 1,
      active: 0
    },
    Jyhniazi: {
      name: 'elecV2P',
      type: 'group',
      note: '系统任务',
      bkcolor: '#f47983',
      collapse: true,
      total: 6,
      active: 2
    },
    UiRsiwmO: {
      name: 'News',
      type: 'group',
      note: '新闻讯息',
      bkcolor: '#30dff3',
      collapse: true,
      total: 7,
      active: 5
    },
    ...
}
--------------------
*/

// 查询 __taskid/__taskname （仅在使用定时任务运行脚本时有值，其他情况默认为 undefined
console.log('执行该脚本的任务名:', __taskname);
console.log('相关任务信息', $task.info(__taskid));

// 尝试使用 __taskid 来停止自身定时任务
if (__taskid) {
    let stopinfo = $task.stop(__taskid); // 停止自身定时任务
    console.log(stopinfo);
}

// 保存当前任务列表
let saveres = $task.save();
console.log(saveres);
/* 
--------------------
{ rescode: 0, message: 'success save current task list 12/19/2' }
--------------------
*/
