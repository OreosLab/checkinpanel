# Changelog


## 20211127-4-120 (2021-11-27)

### Feature

* :sparkles: : 跟随上游更新：EUserv. [Oreo]

### Fix

* :bug: : 修复旧 pushplus 推送后结果解析失败问题. [Oreo]

### Code Style

* :art: : 调整推送日志行间距. [Oreo]


## 20211125-4-010 (2021-11-25)

### Fix

* :bug: : 恢复 Bash：notify.sh. [Oreo]


## 20211124-4-010 (2021-11-24)

### Code Style

* :zap: : 删除 Shell 多余代码. [Oreo]


## 20211123-4-131 (2021-11-23)

### Feature

* :sparkles: : 新增系统及面板检测函数：Bash utils_env.sh. [Oreo]

### Fix

* :bug: : 修复 pip3 包安装判定方式. [Oreo]

* :bug: : 修复 Shell 判断错误. [Oreo]

### Docs

* :memo: : 更新 elecV2P 依赖安装日志图. [Oreo]

### Code Style

* :zap: : 提高 Shell 兼容性，适配 dash. [Oreo]


## 20211122-4-110 (2021-11-22)

### Code Style

* :zap: : 提高 Shell 兼容性. [Oreo]

### Refactor Functions

* :hammer: : 改用 BeautifulSoup 方案进行 pojie 签到. [Oreo]


## 20211121-4-020 (2021-11-21)

### Other

* :pushpin: : 固定依赖. [Oreo]

* :heavy_minus_sign: 删减无用的 request 依赖. [Oreo]


## 20211120-4-010 (2021-11-20)

### Fix

* :bug: : 修改 notify_mtr.py 变量名称错误. [lustime]


## 20211119-4-011 (2021-11-19)

### Fix

* :bug: : 修复 HeyTap 逻辑错误. [Oreo]

### Docs

* :memo: : 修改 README 配置文件等说明. [Oreo]


## 20211118-4-211 (2021-11-18)

### Feature

* :racehorse: : 更新 alpine 基础安装包. [Oreo]

* :racehorse: : 更换 JS 更好的的 TOML 轮子——@iarna/toml. [Oreo]

### Fix

* :bug: : 修复 HeyTap 传参报错. [Oreo]

* :wrench: : 修复通知配置文件注释与变量错位问题. [Oreo]


## 20211117-3-6c5 (2021-11-17)

### Feature

* :sparkles: : 拉库命令更新，新增 cpm 依赖. [Oreo]

* :racehorse: : 改善 cpm 安装逻辑. [Oreo]

* :racehorse: : 分离 JSON5 to TOML 和签到依赖代码. [Oreo]

* :racehorse: : 增加 tomli 解析错误信息打印. [Oreo]

* :rocket: : 新增 Perl cpan install 并提高效率. [Oreo]

* :sparkles: : 添加新配置文件 .toml. [Oreo]

### Fix

* :ambulance: : 重命名应对青龙拉库命令. [Oreo]

* :bug: : 继续修复轮子的缺陷. [Oreo]

* :ambulance: : 使用新轮子，修复旧 bug. [Oreo]

* :fire: : 放弃兼容云函数：HeyTap. [Oreo]

* :wrench: : 移动配置文件引号位置防止误解. [Oreo]

* :bug: : 修复 Perl 转换路径错误. [Oreo]

* :wrench: : 调大必要任务倒计时秒数. [Oreo]

* :bug: : 修复 cpm 安装 bug. [Oreo]

### Docs

* :speech_balloon: 更新可执行路径注释. [Oreo]

* :memo: : 更新 TOML 配置说明文档. [Oreo]

### Code Style

* :zap: : 改善 cpm 安装逻辑. [Oreo]

* :zap: : 修改异常捕获打印学习网址. [Oreo]

* :zap: : 自动拷贝配置文件模板到青龙 config 文件夹. [Oreo]

* :zap: : 脱敏手机号信息：iqiyi. [Oreo]

* :art: : 优化 Perl 转换代码. [Oreo]

### Refactor Functions

* :recycle: : 重大重构：JSON5 配置改为 TOML 配置. [Oreo]

  更新方法：更新仓库后运行 `签到依赖` 任务

### Other

* :see_no_evil: Update .gitignore. [Oreo]


## 20211116-3-220 (2021-11-16)

### Feature

* :rocket: : 新增 EUserv 邮箱转发方案. [Oreo]

* :sparkles: : 新增 Perl JSON5 to TOML 转换脚本. [Oreo]

### Fix

* :bug: : 修复 Perl 正则错误. [Oreo]

### Code Style

* :zap: : 同步更新 HeyTap. [Oreo]


## 20211114-3-192 (2021-11-14)

### Feature

* :racehorse: : 改善登录接口返回信息判断：airport. [Oreo]

* :sparkles: : 同步更新 HeyTap. [Oreo]

* :racehorse: : 增加登录失败或签到失败返回值打印. [Oreo]

### Fix

* :fire: : rm useless code. [Oreo]

* :bug: : 修复 JS tg 推送错误. [Oreo]

* :bug: : 修复 notify.js indexOf 错误. [Oreo]

### Docs

* :memo: : 更新青龙依赖安装截图. [Oreo]

### Code Style

* :art: : 格式化 Shell 中 JS 代码. [Oreo]

### Refactor Functions

* :hammer: : 新增 traceback 异常捕获：notify_mtr_json.py. [Oreo]

* :hammer: : 最终异常处理：airport. [Oreo]

* :hammer: : 继续增加异常捕获：airport. [Oreo]

* :hammer: : 增加异常捕获：airport. [Oreo]

* :hammer: : 重构通知文件异常捕获. [Oreo]


## 20211113-3-230 (2021-11-13)

### Refactor Functions

* :hammer: : 通过测试：依赖安装 shell. [Oreo]

* :hammer: : Update finally for npm. [Oreo]

* :hammer: : 继续测试 npm install. [Oreo]

* :hammer: : 修复 npm 依赖安装（最后一次. [Oreo]

* :hammer: : 修复和更新 npm 安装函数. [Oreo]

  npm install package-merge 改为全局安装，同时适配新版青龙


## 20211112-3-210 (2021-11-12)

### Fix

* :bug: : 继续修复依赖安装代码. [Oreo]

### Refactor Functions

* :hammer: : 重构 npm 依赖安装方法 shell 函数. [Oreo]

* :recycle: : 重构 npm 依赖安装方法. [Oreo]


## 20211111-3-021 (2021-11-11)

### Fix

* :bug: : 修复函数和常量名称错误或不规范. [Oreo]

* :bug: : 修复 notify.js process.env 错误. [Oreo]

### Code Style

* :art: : 统一代码风格（小驼峰和大驼峰） [Oreo]


## 20211110-3-120 (2021-11-10)

### Fix

* :bug: : 修复 str 与其他类型连接 bug. [Oreo]

* :bug: : 修复钉钉推送成功，反馈结果失败 bug. [Oreo]

### Refactor Functions

* :recycle: : JS 支持 notify.json5 单独配置. [Oreo]

  同时对 JS 变量和函数命名尽量采用驼峰命名法


## 20211109-3-100 (2021-11-08)

### Refactor Functions

* :hammer: : 启动 notify.js 重构. [Oreo]


## 20211108-3-111 (2021-11-08)

### Feature

* :sparkles: : 新增 hostloc. [Oreo]

  需安装新的 Python 依赖
  * `pip3 install pyaes` 或运行 `签到依赖` shell 任务

### Fix

* :wrench: : 补充配置文件注释说明（APP 类抓包） [Oreo]

### Refactor Functions

* :hammer: : 实现 heytap 国外访问. [Oreo]


## 20211107-3-031 (2021-11-07)

### Fix

* :bug: : 修复 bark lstrip() 使用错误，应为 rstrip() [Oreo]

* :bug: : 修复 platform.system() 返回值错误. [Oreo]

  返回系统平台/OS的名称，例如 'Linux', 'Darwin', 'Java', 'Windows'。如果该值无法确定则将返回一个空字符串。

### Code Style

* :art: : 修饰异常捕获打印. [Oreo]

### Other

* :children_crossing: [DEV] 测试通知文件异常捕获. [Oreo]

  1. 改用字典 get() 方法来减少报错
  2. 增加 JSON 版通知文件（Python3.6+）几个异常捕获
  3. 丰富返回值判断
  4. 增加 requests 超时参数


## 20211106-3-020 (2021-11-06)

### Fix

* :bug: : 推送逻辑优化. [night-raise]

  1. 修复自定义 bark 链接中 / 重复的 bug 。
  2. 修复一言失败导致无法发送推送的 bug 。

### Refactor Functions

* :hammer: : 修复一言异常类型。 [night-raise]


## 20211105-3-020 (2021-11-05)

### Feature

* :sparkles: : 增加推送中 json 解码错误的全局捕获. [night-raise]

### Refactor Functions

* :hammer: : 修复每日新闻随机可能被移除 8-12 点的问题。 [night-raise]


## 20211104-3-150 (2021-11-04)

### Feature

* :sparkles: : 更新 HeyTap 任务. [Oreo]

* :sparkles: : 更新 womail 任务. [Oreo]

* :sparkles: : 新增通知方式 SRE24.com. [Oreo]

  - [官网](https://push.jwks123.cn/)
  - 暂仅支持 SH，PY 后续增加

### Fix

* :wrench: : 修改和更新配置文件. [Oreo]

* :bug: : 修复 aqc bug. [Oreo]

### Other

* :construction: : 尝试修复 smzdm 任务版报错. [Oreo]


## 20211103-3-100 (2021-11-03)

### Feature

* :rocket: : 兼容 <http://pushplus.hxtrip.com/send> 推送. [Oreo]


## 20211102-3-001 (2021-11-01)

### Other

* :see_no_evil: Update .gitignore. [Oreo]


## 20211101-3-111 (2021-11-01)

### Feature

* :sparkles: : 更新 HeyTap 新活动. [Oreo]

### Fix

* :fire: : rm unused import. [Oreo]

* :fire: : 移除 `notify_mtr_json.py` 异常捕获代码. [Oreo]

  因为 Python 3.6 不支持......
  <https://docs.python.org/3/library/threading.html>


## 20211031-3-011 (2021-10-31)

### Fix

* :bug: : 修复通知文件 `json` 和 `json5` 不兼容的问题. [Oreo]

  重命名 `notify_mtr_older.py` 为 `notify_mtr_json.py` ，表示使用的模块为 `json`

### Docs

* :memo: : 更新 `README` 关于 `notify_mtr_` 系列通知文件的说明. [Oreo]


## 20211030-3-110 (2021-10-30)

### Feature

* :sparkles: : 新增爱企查e卡监控. [Oreo]

### Fix

* :bug: : 修复 smzdm 推送错误. [Oreo]


## 20211028-3-010 (2021-10-27)

### Feature

* :sparkles: : 增加一个新的推送文件。 https://github.com/Oreomeow/checkinpanel/issues/25. [night-raise]

  1. 可以不需要 json5 依赖，那么配置必须符合 json 格式。
  2. 可以不提供 json 配置，通过环境变量指定推送情况。
  3. 未使用海象。


## 20211027-3-020 (2021-10-27)

### Fix

* :bug: : fix leetcode type error. [lustime]

* :bug: : fix hlx param error. [Oreo]


## 20211026-3-020 (2021-10-25)

### Fix

* :bug: : 修复什么值得买任务版消息错误. [Oreo]

* :bug: : 修复爱企查代码错误. [Oreo]


## 20211025-3-300 (2021-10-25)

### Feature

* :sparkles: : 更新爱企查功能. [Oreo]

  新增浏览互动和点赞观点任务，任务间增加随机延迟

* :sparkles: : 新增联想乐云和 WPS. [Oreo]

* :sparkles: : 新增企鹅电竞. [Oreo]

  顺便优化代码，reduce code smell


## 20211024-3-030 (2021-10-24)

### Feature

* :sparkles: : 新增 CCAVA. [Oreo]

* :racehorse: : 新增功能，优化输出. [Oreo]

### Fix

* :bug: : 修复 AcFun 弹幕任务错误. [Oreo]


## 20211023-3-420 (2021-10-23)

### Feature

* :racehorse: : 优化新增功能和输出. [Oreo]

* :sparkles: : 新增每日新闻. [Oreo]

* :sparkles: : 新增在线工具. [Oreo]

* :sparkles: : 新增联想商城. [Oreo]

* :sparkles: : 新增网易蜗牛读书. [Oreo]

### Other

* :children_crossing: 更新天气预报. [Oreo]


## 20211022-3-040 (2021-10-22)

### Fix

* :bug: : 修复 acfun 弹幕和投蕉. [Oreo]

* :bug: : 修复 bili ValueError. [Oreo]

* :bug: : 修复 aqc 函数缺少参数 bug. [Oreo]

* :bug: : 修复 smzdm_mission debug 拼写错误. [Oreo]


## 20211021-3-004 (2021-10-21)

### Feature

* :racehorse: : 重构并优化 JS PY. [Oreo]

### Fix

* :bug: : 修复 elecV2P JS 运行没有控制台输出的错误. [Oreo]

### Code Style

* :art: : 优化代码. [Oreo]

* :art: : 格式化整体项目. [Oreo]


## 20211020-3-120 (2021-10-20)

### Feature

* :sparkles: : 新增 alpine selenium 环境一键搭建脚本. [Oreo]

### Fix

* :bug: : 修复 TG_PROXY_AUTH 和 TG_PROXY_HOST 参数兼容问题. [Oreo]

* :bug: : 修复 apk info 包含匹配错误，使用 grep 命令. [Oreo]

  $(apk info | grep "^$i$") = "$i"


## 20211019-3-200 (2021-10-19)

### Fix

* :ambulance: : 修复 JavaScript 依赖持久化配置. [Oreo]

  npm 安装由全局变为本地

### Refactor Functions

* :recycle: : 重构项目整体依赖安装方法. [Oreo]


## 20211018-2-102 (2021-10-18)

### Feature

* :sparkles: : 新增爱企查. [Oreo]

### Code Style

* :art: : Use Python: black JavaScript: prettier. [Oreo]

### Refactor Functions

* :hammer: : 重构 JS 模块. [Oreo]


## 20211017-2-001 (2021-10-17)

### Docs

* :speech_balloon: 改正日志分类错误. [Oreo]


## 20211016-2-003 (2021-10-16)

### Fix

* :wrench: : 修改配置文件为示例. [Oreo]

### Other

* :see_no_evil: update .gitignore. [Oreo]

* :heavy_plus_sign: add npm dependency got. [Oreo]


## 20211015-2-002 (2021-10-15)

### Docs

* :memo: : 预防 .json5 填写大写 True 而造成格式错误. [Oreo]

### Code Style

* :art: : 调整配置文件缩进. [Oreo]


## 20211014-2-121 (2021-10-14)

### Fix

* :bug: : 修复 nga 任务完成状态判断，使用 re 正则匹配. [Oreo]

### Docs

* :memo: : 修改 README. [Oreo]

### Refactor Functions

* :hammer: : 修复联通沃邮箱. [Oreo]

* :recycle: : 重构控制台输出核心信息. [Oreo]


## 20211013-2-011 (2021-10-13)

### Fix

* :wrench: : 修改欢太商城配置 if_draw -> draw. [Oreo]

* :bug: : 测试修复 nga 判断中... [Oreo]


## 20211012-2-131 (2021-10-12)

### Feature

* :sparkles: : 新增 bili 助手一键脚本. [Oreo]

  1. 支持青龙和 elecV2P
  2. 自动安装 jq Java 依赖

### Fix

* :bug: : 修复 PATH 变量错误导致 apk command not found. [Oreo]

* :bug: : 修复 SF 轻小说输出. [Oreo]

* :bug: : 修复 SF 轻小说 int 和 str 类型连接问题. [Oreo]

### Docs

* :memo: : 更新测试情况. [Oreo]


## 20211011-2-182 (2021-10-11)

### Feature

* :racehorse: : 增加 EUserv 验证码识别方案. [Oreo]

* :sparkles: : 新增 SF 轻小说. [Oreo]

### Fix

* :bug: : 修复 JS 配置文件路径变量读取错误. [Oreo]

* :bug: : 修复 SF 轻小说签到判断. [Oreo]

* :bug: : fix bark push. [night-raise]

  fix type errror.

* :bug: : fix bark push. [night-raise]

  修复由于 BARK 修改为 BARK_PUSH 引起的问题。

* :bug: : fix site.py. [night-raise]

  1. 修复了 学校pt 签到匹配的正则错误。
  2. 优化了 猫站pt 签到的日志输出。

### Docs

* :memo: : 完善 README. [Oreo]

### Code Style

* :art: : 修复联通营业厅和沃邮箱. [Oreo]

* :art: : 修改 Site 键名为 SITE，同时优化代码. [Oreo]

### Other

* :heavy_plus_sign: 增加依赖文件. [Oreo]


## 20211010-2-022 (2021-10-10)

### Feature

* :sparkles: : bark 推送增加参数. [night-raise]

  1. 增加若干可选参数
  2. 当内容为空的时候不推送。

### Fix

* :bug: : 修复 bark 推送变量配置错误. [Oreo]

### Code Style

* :zap: : 调整推送. [Oreo]

  1. 推送方式增加：iGot
  2. 推送变量修改：BARK -> BARK_PUSH 等
  3. 推送变量增加：+PUSH_PLUS_USER 等

### Other

* :page_facing_up: add MIT License. [Oreo]


## 20211008-2-010 (2021-10-07)

### Fix

* :bug: : 修复 bili 银币兑换错误. [Oreo]


## 20211006-2-100 (2021-10-06)

### Feature

* :sparkles: : 新增 smzdm 任务版 JS. [Oreo]


## 20211005-2-021 (2021-10-04)

### Feature

* :sparkles: : 新增通知方式：企业微信机器人. [Oreo]

  1. 新增
  2. 调整顺序及注释等

### Fix

* :bug: : 修复企业微信机器人通知环境变量读取问题. [Oreo]


## 20211003-2-001 (2021-10-03)

### Docs

* :memo: : 调整注释和排版. [Oreo]


## 20210928-2-020 (2021-09-28)

### Fix

* :fire: : rm kjwj. [Oreo]

### Code Style

* :art: : v2ex 代码结构. [night-raise]

  修复了 v2ex 结构，增加了 v2ex ck 获取的说明。


## 20210926-2-001 (2021-09-26)

### Fix

* :wrench: : add euserv config. [Oreo]

  EUserv 在未开启登录验证时有效


## 20210924-2-111 (2021-09-24)

### Feature

* :sparkles: : add site.py. [Oreo]

### Fix

* :bug: : fix ck_site. [night-raise]

  1. 优化了日志输出。
  2. 对于 session ，禁止了复用。

* :wrench: : fix heytap config. [Oreo]


## 20210923-2-210 (2021-09-23)

### Feature

* :sparkles: : add euserv.py & install dependencies cd. [Oreo]

  The script is temporarily disabled and will be fixed later.

* :tada: : init. [Oreo]

### Fix

* :bug: : fix api_ran_time. [night-raise]

  修复随机事件会随机自己的bug。

### Docs

* :speaker: : 增加关于项目历史变动的说明。 [night-raise]


