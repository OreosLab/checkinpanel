# Changelog


## 20220428-4-020 (2022-04-28)

### Feature

* :sparkles: : 新增 woiden 监控：api_hax. [Oreomeow]

* :sparkles: : 修改 tg 推送格式为 HTML. [Oreomeow]

* :sparkles: : 新增 elecV2P 随机 cron 功能. [Oreomeow]

### Fix

* :bug: : 随机定时不要随机自己. [night-raise]

* :bug: : 修复返回值判断错误：duokan. [Oreomeow]

* :bug: : 修复链接失效：tieba. [Oreomeow]

* :bug: : 修复 Acfun 点赞功能. [Oreomeow]

* :bug: : 调整随机定时保存任务列表执行顺序. [Oreo]

* :bug: : fix glados. [Oreomeow]

* :bug: : fix error type. [night-raise]

* :bug: : fix glados. [Oreomeow]

  However
  --------------------

* :fire: : rm expired lecloud. [Oreomeow]

* :wrench: : 移除及修改配置信息. [Oreomeow]

### Code Style

* :art: : 规范 response(r) 和 res. [Oreomeow]

* :art: : 优化代码. [Oreomeow]

  1. 新增 HTML 格式
  2. 变量名调整
  3. 空行缩减

### Refactor Functions

* :recycle: : 重构随机定时. [night-raise]

### Other

* :arrow_up: Update cpm to 0.997009. [Oreomeow]


## 20220327-4-010 (2022-03-27)

### Fix

* :bug: : 临时关闭随机定时功能。 [night-raise]

* :fire: : rm some scripts config. [Oreomeow]

* :fire: : 移除部分脚本. [Oreomeow]

  考虑到维护和调试成本，不再维护视频网站脚本等

* :bug: : 修复知乎推送过多的问题. [night-raise]

* :bug: : 更换无用代理：bili. [Oreomeow]

* :bug: : 修正 CCAVA 类命名错误. [Oreomeow]

### Code Style

* :building_construction: 重构 hax. [Oreomeow]

### Refactor Functions

* :hammer: : 进一步降低 rss bot 的推送数量. [night-raise]

* :hammer: : 移除 rss bot 的日期格式. [night-raise]

  新增加了一些 rss 订阅链接，需要将 rss.simple.db 拷贝到 rss.db

* :hammer: : 修复重复拉取问题. [Oreomeow]

* :hammer: : 修复 acfun. [Oreomeow]

### Other

* :alien: : 青龙面板(v2.12.0+) 适配。 [night-raise]

  修正插入 rss 的 sql

* :alien: : 增加 青龙面板(v2.12.0+) 适配。 [Oreomeow]

* :arrow_down: 降低 got 版本以兼容. [Oreomeow]


## 20220226-4-020 (2022-02-26)

### Feature

* :racehorse: : 新增推送天数限制自定义：rssbot. [Oreomeow]

* :sparkles: : 更新葫芦侠脚本 #69. [Oreo]

### Fix

* :bug: : 修复在线工具签到地址. [Oreomeow]

* :bug: : 修复时间格式错误：rssbot. [Oreomeow]

* :bug: : fix sre24 push domain (#102) [Tony]

* :bug: : 修改在线工具地址 (#96) [七mi]

  抓取该页面的cookie即可

### Docs

* :memo: : 更新测试情况 失效脚本数量较多，暂不更新. [Oreomeow]

* :memo: : 调整 CHANGELOG 和 tag. [Oreomeow]

  以大版本号为界打 tag
  当前版本以月为界，当月第一次更新时打 tag

### Code Style

* :zap: : 分批发送：rssbot. [Oreomeow]

* :building_construction: 更改名称和 rss.db 位置：api_rssbot 1. 上线 elecV2P 2. qinglong 或 elecV2P 根据脚本提示移动 rss.db 位置. [Oreomeow]

* :zap: : 改进 hax 正则. [Oreo]

### Refactor Functions

* :hammer: : 给 rss 订阅加入日期格式. [night-raise]

### Other

* :arrow_up: Bump follow-redirects from 1.14.7 to 1.14.8 (#101) [dependabot[bot]]

  Bumps [follow-redirects](https://github.com/follow-redirects/follow-redirects) from 1.14.7 to 1.14.8.
  - [Release notes](https://github.com/follow-redirects/follow-redirects/releases)
  - [Commits](https://github.com/follow-redirects/follow-redirects/compare/v1.14.7...v1.14.8)

  ---
  updated-dependencies:
  - dependency-name: follow-redirects
    dependency-type: indirect
  ...

* :see_no_evil: 更新 .gitignore 修改排序并增加 rss.db. [Oreomeow]


## 20220129-4-100 (2022-02-02)

### Feature

* :racehorse: : 加入新区域 VPS 可开通查询：hax. [Oreo]

* :racehorse: : 同时支持普通用户名：airport #79. [Oreo]

* :sparkles: : 恢复更新. [Oreo]

  1. 同步更新 epic
  2. 修复 iqiyi
  3. 整合新脚本：换源、RSS

* :sparkles: : add rssbot (#90) [JaimeZeng]

  * add rssbot

  * remove dateparser

* :sparkles: : 增加 hdtime 签到. [LiGuo]

* :sparkles: : 跟随上游适配圣诞特惠. [Oreo]

* :sparkles: : 更新 api_hax 功能并重构消息. [Oreo]

  应对新增的数据中心

### Fix

* :bug: : 修正错字 (#94) [Canary233]

* :bug: : rss 只推送 7 天内的内容，两小时更新一次。 [night-raise]

* :bug: : 跟随上游修复 aqc. [Oreo]

* :bug: : 修复 18 岁验证：epic. [Oreo]

* :bug: : 修复一个判断错误：api_hax. [Oreo]

* :fire: : rm haxclock. [Oreo]

* :wrench: : 修改配置文件错误：HAXCLOCK. [Oreo]

### Code Style

* :zap: : 本地化日志输出：EUserv. [Oreo]

### Other

* :arrow_up: 升级 follow-redirects. [Oreo]

* Add pt时间. [LiGuo]

* 添加国内换源脚本. [Vincent]

* :white_check_mark: 增加测试代码：haxclock. [Oreo]


## 20211211-4-201 (2021-12-11)

### Feature

* :sparkles: : 新增 Hax 续期提醒. [Oreo]

* :sparkles: : 更新 Hax 监控. [Oreo]

* :sparkles: : 跟随上游更新并优化. [Oreo]

* :sparkles: : 新增开机自动安装依赖文件：checkins_pkg.js. [Oreo]

* :sparkles: : 更新并重构 ck_epic 主函数. [Oreo]

* :sparkles: : 跟随上游更新：ck_epic. [Oreo]

* :rocket: : 新增获取 config/script 目录路径函数：utils_env.sh. [Oreo]

* :sparkles: : 新增 Epic. [Oreo]

### Fix

* :fire: : 关闭  heytap 早睡打卡. [Oreo]

* :bug: : 修复 epic 会被删除 cookies.json 的 bug. [Oreo]

  其实不算 bug......

* :bug: : 修复 freenom 多账号打印 bug. [Oreo]

* :bug: : 尝试修复 tg 推送错误：notify.sh. [Oreo]

  `&parse_mode=Markdown&text=` 改为 `&parse_mode=HTML&text=`

* :bug: : 修复打印错误：utils_env.sh. [Oreo]

* :bug: : 修复 shell 变量名 panel 拼写错误. [Oreo]

* :wrench: : 添加 ins_selenium 任务. [Oreo]

### Docs

* :memo: : 调整 CHANGELOG 和 tag. [Oreo]

  以大版本号为界打 tag
  当前版本以周为界，周一或每周第一次更新时打 tag

* :memo: : 更新 README badges. [Oreo]

### Code Style

* :zap: : 改进代码错误. [Oreo]

### Refactor Functions

* :recycle: : 重构入口文件：checkin*.js 系列. [Oreo]

### Other

* :see_no_evil: 更新 .gitignore. [Oreo]


## 20211127-4-120 (2021-11-27)

### Feature

* :sparkles: : 跟随上游更新：EUserv. [Oreo]

* :sparkles: : 新增系统及面板检测函数：Bash utils_env.sh. [Oreo]

* :racehorse: : 更新 alpine 基础安装包. [Oreo]

* :racehorse: : 更换 JS 更好的的 TOML 轮子——@iarna/toml. [Oreo]

### Fix

* :bug: : 修复旧 pushplus 推送后结果解析失败问题. [Oreo]

* :bug: : 恢复 Bash：notify.sh. [Oreo]

* :bug: : 修复 pip3 包安装判定方式. [Oreo]

* :bug: : 修复 Shell 判断错误. [Oreo]

* :bug: : 修改 notify_mtr.py 变量名称错误. [lustime]

* :bug: : 修复 HeyTap 逻辑错误. [Oreo]

* :bug: : 修复 HeyTap 传参报错. [Oreo]

* :wrench: : 修复通知配置文件注释与变量错位问题. [Oreo]

### Docs

* :memo: : 更新 elecV2P 依赖安装日志图. [Oreo]

* :memo: : 修改 README 配置文件等说明. [Oreo]

### Code Style

* :art: : 调整推送日志行间距. [Oreo]

* :zap: : 删除 Shell 多余代码. [Oreo]

* :zap: : 提高 Shell 兼容性，适配 dash. [Oreo]

* :zap: : 提高 Shell 兼容性. [Oreo]

### Refactor Functions

* :hammer: : 改用 BeautifulSoup 方案进行 pojie 签到. [Oreo]

### Other

* :pushpin: : 固定依赖. [Oreo]

* :heavy_minus_sign: 删减无用的 request 依赖. [Oreo]


## 20211117-3-6c5 (2021-11-17)

### Feature

* :sparkles: : 拉库命令更新，新增 cpm 依赖. [Oreo]

* :racehorse: : 改善 cpm 安装逻辑. [Oreo]

* :racehorse: : 分离 JSON5 to TOML 和签到依赖代码. [Oreo]

* :racehorse: : 增加 tomli 解析错误信息打印. [Oreo]

* :rocket: : 新增 Perl cpan install 并提高效率. [Oreo]

* :sparkles: : 添加新配置文件 .toml. [Oreo]

* :rocket: : 新增 EUserv 邮箱转发方案. [Oreo]

* :sparkles: : 新增 Perl JSON5 to TOML 转换脚本. [Oreo]

* :racehorse: : 改善登录接口返回信息判断：airport. [Oreo]

* :sparkles: : 同步更新 HeyTap. [Oreo]

* :racehorse: : 增加登录失败或签到失败返回值打印. [Oreo]

* :sparkles: : 新增 hostloc. [Oreo]

  需安装新的 Python 依赖
  * `pip3 install pyaes` 或运行 `签到依赖` shell 任务

* :sparkles: : 增加推送中 json 解码错误的全局捕获. [night-raise]

* :sparkles: : 更新 HeyTap 任务. [Oreo]

* :sparkles: : 更新 womail 任务. [Oreo]

* :sparkles: : 新增通知方式 SRE24.com. [Oreo]

  - [官网](https://push.jwks123.cn/)
  - 暂仅支持 SH，PY 后续增加

* :rocket: : 兼容 <http://pushplus.hxtrip.com/send> 推送. [Oreo]

* :sparkles: : 更新 HeyTap 新活动. [Oreo]

* :sparkles: : 新增爱企查e卡监控. [Oreo]

* :sparkles: : 增加一个新的推送文件。 https://github.com/Oreomeow/checkinpanel/issues/25. [night-raise]

  1. 可以不需要 json5 依赖，那么配置必须符合 json 格式。
  2. 可以不提供 json 配置，通过环境变量指定推送情况。
  3. 未使用海象。

* :sparkles: : 更新爱企查功能. [Oreo]

  新增浏览互动和点赞观点任务，任务间增加随机延迟

* :sparkles: : 新增联想乐云和 WPS. [Oreo]

* :sparkles: : 新增企鹅电竞. [Oreo]

  顺便优化代码，reduce code smell

* :sparkles: : 新增 CCAVA. [Oreo]

* :racehorse: : 新增功能，优化输出. [Oreo]

* :racehorse: : 优化新增功能和输出. [Oreo]

* :sparkles: : 新增每日新闻. [Oreo]

* :sparkles: : 新增在线工具. [Oreo]

* :sparkles: : 新增联想商城. [Oreo]

* :sparkles: : 新增网易蜗牛读书. [Oreo]

* :racehorse: : 重构并优化 JS PY. [Oreo]

* :sparkles: : 新增 alpine selenium 环境一键搭建脚本. [Oreo]

### Fix

* :ambulance: : 重命名应对青龙拉库命令. [Oreo]

* :bug: : 继续修复轮子的缺陷. [Oreo]

* :ambulance: : 使用新轮子，修复旧 bug. [Oreo]

* :fire: : 放弃兼容云函数：HeyTap. [Oreo]

* :wrench: : 移动配置文件引号位置防止误解. [Oreo]

* :bug: : 修复 Perl 转换路径错误. [Oreo]

* :wrench: : 调大必要任务倒计时秒数. [Oreo]

* :bug: : 修复 cpm 安装 bug. [Oreo]

* :bug: : 修复 Perl 正则错误. [Oreo]

* :fire: : rm useless code. [Oreo]

* :bug: : 修复 JS tg 推送错误. [Oreo]

* :bug: : 修复 notify.js indexOf 错误. [Oreo]

* :bug: : 继续修复依赖安装代码. [Oreo]

* :bug: : 修复函数和常量名称错误或不规范. [Oreo]

* :bug: : 修复 notify.js process.env 错误. [Oreo]

* :bug: : 修复 str 与其他类型连接 bug. [Oreo]

* :bug: : 修复钉钉推送成功，反馈结果失败 bug. [Oreo]

* :wrench: : 补充配置文件注释说明（APP 类抓包） [Oreo]

* :bug: : 修复 bark lstrip() 使用错误，应为 rstrip() [Oreo]

* :bug: : 修复 platform.system() 返回值错误. [Oreo]

  返回系统平台/OS的名称，例如 'Linux', 'Darwin', 'Java', 'Windows'。如果该值无法确定则将返回一个空字符串。

* :bug: : 推送逻辑优化. [night-raise]

  1. 修复自定义 bark 链接中 / 重复的 bug 。
  2. 修复一言失败导致无法发送推送的 bug 。

* :wrench: : 修改和更新配置文件. [Oreo]

* :bug: : 修复 aqc bug. [Oreo]

* :fire: : rm unused import. [Oreo]

* :fire: : 移除 `notify_mtr_json.py` 异常捕获代码. [Oreo]

  因为 Python 3.6 不支持......
  <https://docs.python.org/3/library/threading.html>

* :bug: : 修复通知文件 `json` 和 `json5` 不兼容的问题. [Oreo]

  重命名 `notify_mtr_older.py` 为 `notify_mtr_json.py` ，表示使用的模块为 `json`

* :bug: : 修复 smzdm 推送错误. [Oreo]

* :bug: : fix leetcode type error. [lustime]

* :bug: : fix hlx param error. [Oreo]

* :bug: : 修复什么值得买任务版消息错误. [Oreo]

* :bug: : 修复爱企查代码错误. [Oreo]

* :bug: : 修复 AcFun 弹幕任务错误. [Oreo]

* :bug: : 修复 acfun 弹幕和投蕉. [Oreo]

* :bug: : 修复 bili ValueError. [Oreo]

* :bug: : 修复 aqc 函数缺少参数 bug. [Oreo]

* :bug: : 修复 smzdm_mission debug 拼写错误. [Oreo]

* :bug: : 修复 elecV2P JS 运行没有控制台输出的错误. [Oreo]

* :bug: : 修复 TG_PROXY_AUTH 和 TG_PROXY_HOST 参数兼容问题. [Oreo]

* :bug: : 修复 apk info 包含匹配错误，使用 grep 命令. [Oreo]

  $(apk info | grep "^$i$") = "$i"

* :ambulance: : 修复 JavaScript 依赖持久化配置. [Oreo]

  npm 安装由全局变为本地

### Docs

* :speech_balloon: 更新可执行路径注释. [Oreo]

* :memo: : 更新 TOML 配置说明文档. [Oreo]

* :memo: : 更新青龙依赖安装截图. [Oreo]

* :memo: : 更新 `README` 关于 `notify_mtr_` 系列通知文件的说明. [Oreo]

### Code Style

* :zap: : 改善 cpm 安装逻辑. [Oreo]

* :zap: : 修改异常捕获打印学习网址. [Oreo]

* :zap: : 自动拷贝配置文件模板到青龙 config 文件夹. [Oreo]

* :zap: : 脱敏手机号信息：iqiyi. [Oreo]

* :art: : 优化 Perl 转换代码. [Oreo]

* :zap: : 同步更新 HeyTap. [Oreo]

* :art: : 格式化 Shell 中 JS 代码. [Oreo]

* :art: : 统一代码风格（小驼峰和大驼峰） [Oreo]

* :art: : 修饰异常捕获打印. [Oreo]

* :art: : 优化代码. [Oreo]

* :art: : 格式化整体项目. [Oreo]

### Refactor Functions

* :recycle: : 重大重构：JSON5 配置改为 TOML 配置. [Oreo]

  更新方法：更新仓库后运行 `签到依赖` 任务

* :hammer: : 新增 traceback 异常捕获：notify_mtr_json.py. [Oreo]

* :hammer: : 最终异常处理：airport. [Oreo]

* :hammer: : 继续增加异常捕获：airport. [Oreo]

* :hammer: : 增加异常捕获：airport. [Oreo]

* :hammer: : 重构通知文件异常捕获. [Oreo]

* :hammer: : 通过测试：依赖安装 shell. [Oreo]

* :hammer: : Update finally for npm. [Oreo]

* :hammer: : 继续测试 npm install. [Oreo]

* :hammer: : 修复 npm 依赖安装（最后一次. [Oreo]

* :hammer: : 修复和更新 npm 安装函数. [Oreo]

  npm install package-merge 改为全局安装，同时适配新版青龙

* :hammer: : 重构 npm 依赖安装方法 shell 函数. [Oreo]

* :recycle: : 重构 npm 依赖安装方法. [Oreo]

* :recycle: : JS 支持 notify.json5 单独配置. [Oreo]

  同时对 JS 变量和函数命名尽量采用驼峰命名法

* :hammer: : 启动 notify.js 重构. [Oreo]

* :hammer: : 实现 heytap 国外访问. [Oreo]

* :hammer: : 修复一言异常类型。 [night-raise]

* :hammer: : 修复每日新闻随机可能被移除 8-12 点的问题。 [night-raise]

* :recycle: : 重构项目整体依赖安装方法. [Oreo]

### Other

* :see_no_evil: Update .gitignore. [Oreo]

* :children_crossing: [DEV] 测试通知文件异常捕获. [Oreo]

  1. 改用字典 get() 方法来减少报错
  2. 增加 JSON 版通知文件（Python3.6+）几个异常捕获
  3. 丰富返回值判断
  4. 增加 requests 超时参数

* :construction: : 尝试修复 smzdm 任务版报错. [Oreo]

* :see_no_evil: Update .gitignore. [Oreo]

* :children_crossing: 更新天气预报. [Oreo]


## 20211018-2-102 (2021-10-18)

### Feature

* :sparkles: : 新增爱企查. [Oreo]

* :sparkles: : 新增 bili 助手一键脚本. [Oreo]

  1. 支持青龙和 elecV2P
  2. 自动安装 jq Java 依赖

* :racehorse: : 增加 EUserv 验证码识别方案. [Oreo]

* :sparkles: : 新增 SF 轻小说. [Oreo]

* :sparkles: : bark 推送增加参数. [night-raise]

  1. 增加若干可选参数
  2. 当内容为空的时候不推送。

* :sparkles: : 新增 smzdm 任务版 JS. [Oreo]

* :sparkles: : 新增通知方式：企业微信机器人. [Oreo]

  1. 新增
  2. 调整顺序及注释等

* :sparkles: : add site.py. [Oreo]

* :sparkles: : add euserv.py & install dependencies cd. [Oreo]

  The script is temporarily disabled and will be fixed later.

* :tada: : init. [Oreo]

### Fix

* :wrench: : 修改配置文件为示例. [Oreo]

* :bug: : 修复 nga 任务完成状态判断，使用 re 正则匹配. [Oreo]

* :wrench: : 修改欢太商城配置 if_draw -> draw. [Oreo]

* :bug: : 测试修复 nga 判断中... [Oreo]

* :bug: : 修复 PATH 变量错误导致 apk command not found. [Oreo]

* :bug: : 修复 SF 轻小说输出. [Oreo]

* :bug: : 修复 SF 轻小说 int 和 str 类型连接问题. [Oreo]

* :bug: : 修复 JS 配置文件路径变量读取错误. [Oreo]

* :bug: : 修复 SF 轻小说签到判断. [Oreo]

* :bug: : fix bark push. [night-raise]

  fix type errror.

* :bug: : fix bark push. [night-raise]

  修复由于 BARK 修改为 BARK_PUSH 引起的问题。

* :bug: : fix site.py. [night-raise]

  1. 修复了 学校pt 签到匹配的正则错误。
  2. 优化了 猫站pt 签到的日志输出。

* :bug: : 修复 bark 推送变量配置错误. [Oreo]

* :bug: : 修复 bili 银币兑换错误. [Oreo]

* :bug: : 修复企业微信机器人通知环境变量读取问题. [Oreo]

* :fire: : rm kjwj. [Oreo]

* :wrench: : add euserv config. [Oreo]

  EUserv 在未开启登录验证时有效

* :bug: : fix ck_site. [night-raise]

  1. 优化了日志输出。
  2. 对于 session ，禁止了复用。

* :wrench: : fix heytap config. [Oreo]

* :bug: : fix api_ran_time. [night-raise]

  修复随机事件会随机自己的bug。

### Docs

* :speech_balloon: 改正日志分类错误. [Oreo]

* :memo: : 预防 .json5 填写大写 True 而造成格式错误. [Oreo]

* :memo: : 修改 README. [Oreo]

* :memo: : 更新测试情况. [Oreo]

* :memo: : 完善 README. [Oreo]

* :memo: : 调整注释和排版. [Oreo]

* :speaker: : 增加关于项目历史变动的说明。 [night-raise]

### Code Style

* :art: : Use Python: black JavaScript: prettier. [Oreo]

* :art: : 调整配置文件缩进. [Oreo]

* :art: : 修复联通营业厅和沃邮箱. [Oreo]

* :art: : 修改 Site 键名为 SITE，同时优化代码. [Oreo]

* :zap: : 调整推送. [Oreo]

  1. 推送方式增加：iGot
  2. 推送变量修改：BARK -> BARK_PUSH 等
  3. 推送变量增加：+PUSH_PLUS_USER 等

* :art: : v2ex 代码结构. [night-raise]

  修复了 v2ex 结构，增加了 v2ex ck 获取的说明。

### Refactor Functions

* :hammer: : 重构 JS 模块. [Oreo]

* :hammer: : 修复联通沃邮箱. [Oreo]

* :recycle: : 重构控制台输出核心信息. [Oreo]

### Other

* :see_no_evil: update .gitignore. [Oreo]

* :heavy_plus_sign: add npm dependency got. [Oreo]

* :heavy_plus_sign: 增加依赖文件. [Oreo]

* :page_facing_up: add MIT License. [Oreo]


