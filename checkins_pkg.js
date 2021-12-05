// @grant nodejs
console.log(`⏳ 初始化安装环境依赖开始...`);
$exec(`chmod +x ins_pkg.sh && sh ins_pkg.sh && bash ins_selenium.sh`, {
    cwd: 'script/Shell/checkinpanel',
    timeout: 0,
    cb(data, error) {
        error ? console.error(error) : console.log(data);
    },
});
