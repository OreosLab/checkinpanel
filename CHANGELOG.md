# Changelog


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


