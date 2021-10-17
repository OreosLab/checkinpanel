# Changelog


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

* :racehorse: : 增加 EUserv 验证码识别方案. [Oreo]

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


