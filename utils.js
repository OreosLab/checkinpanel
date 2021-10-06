const fs = require('fs');
const JSON5 = require('json5');
let check_config = [];
let v2p_path = '/usr/local/app/script/Lists/';
let v2p_file = (fs.existsSync(v2p_path + 'check.json5')) ? v2p_path + 'check.json5' : v2p_path + 'check.json';
let ql_path = '/ql/config/';
let ql_file = (fs.existsSync(ql_path + 'check.json5')) ? ql_path + 'check.json5' : ql_path + 'check.json';

function get_data() {
    if (process.env.CHECK_PATH) {
        check_config = JSON5.parse(fs.readFileSync(CHECK_PATH, 'utf-8'))
    }
    else if (fs.existsSync(v2p_file)) {
        check_config = JSON5.parse(fs.readFileSync(v2p_file, 'utf-8'))
    }
    else if (fs.existsSync(ql_file)) {
        check_config = JSON5.parse(fs.readFileSync(ql_file, 'utf-8'))
    }
    else if (fs.existsSync('./check.json5')) {
        check_config = JSON5.parse(fs.readFileSync('./check.json5', 'utf-8'))
    }
    else {
        console.log('错误：未检查到签到配置文件，请在指定位置创建文件或设置 CHECK_CONFIG 指定你的文件。')
    }
    return check_config
}

module.exports = get_data;
