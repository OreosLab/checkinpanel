<div align="center"> 
<h1 align="center">定时面板上的签到盒</h1>

![GitHub stars](https://img.shields.io/github/stars/Oreomeow/checkinpanel?color=brightgreen&logo=Riseup&logoColor=brightgreen&style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/Oreomeow/checkinpanel?color=brightgreen&style=flat-square)
<a href="https://github.com/Oreomeow/checkinpanel/issues"><img src="https://img.shields.io/github/issues/Oreomeow/checkinpanel?color=orange&style=flat-square" alt="GitHub issues"></a>
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Oreomeow/checkinpanel?color=informational&logo=Python&logoColor=informational&style=flat-square)
<a href="https://t.me/joinchat/muGNhnaZglQ0N2Q1"><img src="https://img.shields.io/badge/talk-Telegram-blue?logo=Telegram&style=flat-square" alt="Telegram"></a>
<a href="https://github.com/Oreomeow/checkinpanel/commits"><img src="https://img.shields.io/github/last-commit/Oreomeow/checkinpanel?color=success&logo=GitHub&style=flat-square" alt="GitHub last commit"></a>

</div>

# 一个运行在 𝐞𝐥𝐞𝐜𝐕𝟐𝐏 或 𝐪𝐢𝐧𝐠𝐥𝐨𝐧𝐠 等定时面板的签到项目

[𝐞𝐥𝐞𝐜𝐕𝟐𝐏](https://github.com/elecV2/elecV2P.git)

[𝐪𝐢𝐧𝐠𝐥𝐨𝐧𝐠](https://github.com/whyour/qinglong.git)

## 特别声明

* 本仓库发布的脚本及其中涉及的任何解锁和解密分析脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

* 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

* 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害。

* 间接使用脚本的任何用户，包括但不限于建立 VPS 或在某些行为违反国家/地区法律或相关法规的情况下进行传播，本人对于由此引起的任何隐私泄漏或其他后果概不负责。

* 请勿将本仓库的任何内容用于商业或非法目的，否则后果自负。

* 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明、所有权证明，我们将在收到认证文件后删除相关脚本。

* 任何以任何方式查看此项目的人或直接或间接使用该项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或 Script 项目的规则，则视为您已接受此免责声明。

**您必须在下载后的 24 小时内从计算机或手机中完全删除以上内容**

> ***您使用或者复制了本仓库且本人制作的任何脚本，则视为 `已接受` 此声明，请仔细阅读***

## 𝐞𝐥𝐞𝐜𝐕𝟐𝐏 使用方法

### 1. 添加任务

TASK -> 添加订阅任务 -> 修改名称、更新方式、任务 -> 获取内容 -> 全部添加

名称：签到项目

同名任务更新方式： `替换`

任务：

```
https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/dailycheckin.json
```

### 2. 抓包配置

下载 [check.sample.json5](https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/check.sample.json5)，根据 [Sitoi](https://github.com/Sitoi/dailycheckin) 的[配置说明](https://sitoi.gitee.io/dailycheckin/settings/)进行抓包并配置

### 3. 上传配置

将 `check.sample.json5` 重命名为 `check.json5` 后放入 `script/Lists` 文件夹

* OVERVIEW -> EFSS 文件管理界面 -> 是否开启 EFSS 功能：开启 -> 目录：`./script/Lists` -> 选择文件：`check.json5` -> 开始上传

* elecV2P 3.4.6 已支持在线编辑，右键文件即可

### 4. 配置通知

#### 4.1 JSMANAGE -> store/cookie 常量储存管理填写通知环境变量

| 变量 / key | 描述 | 参考 / value |
| --- | --- |  --- |
| HITOKOTO | 一言（一句话） | True（启用）or False（不启用） |
| BARK | bark 服务 | BARK 推送[使用](https://github.com/Sitoi/dailycheckin/issues/29)，填写 `BARK_URL` 即可，例如： `https://api.day.app/DxHcxxxxxRxxxxxxcm/` ，此参数如果以 `http` 或者 `https` 开头则判定为自建 bark 服务 |
| PUSH_KEY | Server 酱 | server 酱推送[官方文档](https://sc.ftqq.com/3.version)，填写 `SCKEY` 代码即可|
| TG_BOT_TOKEN | tg 机器人 | 申请 [@BotFather](https://t.me/BotFather) 的 Token，如 `10xxx4:AAFcqxxxxgER5uw` |
| TG_USER_ID | tg 机器人 | 给 [@getidsbot](https://t.me/getidsbot) 发送 /start 获取到的纯数字 ID，如 `1434078534` |
| TG_API_HOST | * tg 代理 api | Telegram api 自建的反向代理地址 例子：反向代理地址 `http://aaa.bbb.ccc` 则填写 aaa.bbb.ccc [简略搭建教程](https://shimo.im/docs/JD38CJDQtYy3yTd8/read) |
| TG_PROXY_IP | * tg 机器人代理 IP 地址 | 代理类型为 http，比如您代理是 `http://127.0.0.1:1080` ，则填写 `127.0.0.1` ，有密码例子: `username:password@127.0.0.1` |
| TG_PROXY_PORT | * tg 机器人代理端口 | 代理端口号，代理类型为 http，比如您代理是 `http://127.0.0.1:1080` ，则填写 `1080` |
| DD_BOT_TOKEN | 钉钉机器人 | 钉钉推送[官方文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)，只需 `https://oapi.dingtalk.com/robot/send?access_token=XXX` 等于符号后面的 `XXX` |
| DD_BOT_SECRET | 钉钉机器人 | 钉钉推送[官方文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)密钥，机器人安全设置页面，加签一栏下面显示的 `SEC` 开头的字符串，注：填写了 `DD_BOT_TOKEN` 和 `DD_BOT_SECRET` ，钉钉机器人安全设置只需勾选加签即可，其他选项不要勾选 |
| QMSG_KEY | qmsg 酱 | qmsg 酱推送[官方文档](https://qmsg.zendee.cn/index.html)，填写 `KEY` 代码即可 |
| QMSG_TYPE | qmsg 酱 | qmsg 酱推送[官方文档](https://qmsg.zendee.cn/index.html)，如果需要推送到群填写 `group` ，其他的都推送到 QQ |
| QYWX_AM | 企业微信应用 | 参考 http://note.youdao.com/s/HMiudGkb |
| PUSH_PLUS_TOKEN | pushplus | 用户令牌，可直接加到请求地址后，如： `http://www.pushplus.plus/send/{token}` [官方文档](https://www.pushplus.plus/doc/) |
| GOBOT_URL | go-cqhttp | 例如：推送到个人QQ： `http://127.0.0.1/send_private_msg` 群： `http://127.0.0.1/send_group_msg` |
| GOBOT_TOKEN | * go-cqhttp 的 access_token | go-cqhttp 文件设置的访问密钥 |
| GOBOT_QQ | go-cqhttp 的推送群或者用户 | `GOBOT_URL` 设置 `/send_private_msg` 则需要填入 `user_id=个人QQ` 相反如果是 `/send_group_msg` 则需要填入 `group_id=QQ群` |
| FSKEY | 飞书 | 飞书[官方文档](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN)，只需 `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx` 的 `xxxxxx` 部分 |

*\* 表示选填*

#### 4.2 另一种通知配置方式（当和 4.1 中值重复时，以 4.1 值为准）

下载项目中的 [推送配置文件](https://github.com/Oreomeow/checkinpanel/blob/master/notify.json5) 到**配置文件夹**，按照上述说明修改配置文件中的值，你可以**自由地删除**该文件中某些不需要的值（注意语法）。

使用了配置文件后，你可以将配置文件放在持久化位置，不受脚本更新、重置容器的影响。

如果想自定义配置文件的位置和文件名，请设置通知环境变量 `NOTIFY_CONFIG_PATH` ， 例如 `/usr/local/app/script/notify_config.json5` 。建议保持 `json5` 的后缀，防止编辑器的误解。

关于 json5 的语法参考：

* [官方说明](https://json5.org/)
* [中文网友博客说明](https://zhuanlan.zhihu.com/p/108119490)
* [json5语法验证](https://verytoolz.com/json5-validator.html)

#### 4.3 通知说明

本通知调用了项目中的 [𝒏𝒐𝒕𝒊𝒇𝒚_𝒎𝒕𝒓.𝒑𝒚](https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/notify_mtr.py) 。如果你想在**你自己的项目中**使用这个通知脚本，将它拷贝并调用对应的通知函数即可。

在非容器环境中，通知环境变量使用 系统的环境变量 或者 **你通过 `NOTIFY_CONFIG_PATH` 环境变量指定的配置文件** 进行配置。

特别的，如果你想要创建一个基于 python 的 elecV2P 或者 qinglong 项目，强烈建议你拷贝 [此文件](https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/notify_mtr.py)，如此可以大幅度降低用户脚本的配置难度和升级难度。

## 𝐪𝐢𝐧𝐠𝐥𝐨𝐧𝐠 使用方法

### 1. ssh 进入容器

```sh
docker exec -it qinglong bash
```

修改 `qinglong` 为你的青龙容器名称

### 2. 安装依赖

```sh
apk add gcc libffi-dev musl-dev openssl-dev python3-dev && pip3 install cryptography~=3.2.1 json5 requests rsa
```

**依赖持久化配置**

```sh
requirement_name="cryptography~=3.2.1 json5 requests rsa"

install_requirements() {
    for i in $requirement_name; do
        case $i in
            cryptography~=3.2.1)
                cd /ql/scripts
                if [[ "$(pip3 freeze)" =~ "cryptography==3.2.1" ]]; then
                    echo "cryptography==3.2.1 已安装"
                else
                    apk add --no-cache gcc libffi-dev musl-dev openssl-dev python3-dev && pip3 install cryptography~=3.2.1
                fi
                ;;
            *)
                if [[ "$(pip3 freeze)" =~ $i ]]; then
                    echo "$i 已安装"
                else
                    pip3 install $i
                fi
                ;;
        esac
    done
}

install_requirements
```

在 `extra.sh` 增加这段代码即可

### 3. 拉取仓库

可添加定时任务，名称、时间自定

```
ql repo https://github.com/Oreomeow/checkinpanel.git "api_|ck_" "^checkin" "^notify|^utils" "master"
```

**解决 Shell 脚本无法拉取问题**

```sh
## ql repo命令拉取脚本时需要拉取的文件后缀，直接写文件后缀名即可
RepoFileExtensions="js py sh ts"
```

将以上代码在 `config.sh` 相应位置替换

### 4. 拷贝文件

```sh
cp /ql/repo/Oreomeow_checkinpanel_master/check.sample.json5 /ql/config/check.json5
```

*通知配置文件（可选）*

~~~shell
cp /ql/repo/Oreomeow_checkinpanel_master/notify.json5 /ql/config/notify.json5
~~~

### 5. 配置通知

参见上文中的[配置通知](#https://github.com/Oreomeow/checkinpanel/blob/master/README.md#4配置通知)。

特别的：

* **如果你已经配置了 `config.sh`， 那么你可以不需要做任何改变。**
* 如果使用环境变量，请在 qinglong 面板中配置。
* 如果使用配置文件，请修改 `/ql/config/notify.json5` 文件。
* 当然你也可以在 qinglong 面板中配置 `NOTIFY_CONFIG_PATH` 环境变量为配置文件指定其他位置。

### 6. 抓包配置

不出意外的话可以在青龙面板的配置文件下找到 `check.json5` 文件

根据 [Sitoi](https://github.com/Sitoi/dailycheckin) 的[配置说明](https://sitoi.gitee.io/dailycheckin/settings/)进行抓包并配置

## 补充说明

### 1. **添加了葫芦侠的签到配置**

​	参数说明： `HLX.username` ：用户名 `HLX.password` ：密码的 MD5 32 位小写加密[生成](https://md5jiami.bmcx.com/)

### 2. **添加了网易云游戏的签到配置**

[官网](https://cg.163.com/#/mobile)

参数说明： `GAME163.authorization`

登录后抓取签到请求（一般请求的请求头也有这个字段）

[![4tfx5F.png](https://z3.ax1x.com/2021/09/22/4tfx5F.png)](https://imgtu.com/i/4tfx5F)

### 3. **Shell 脚本配置**

* 目前 Shell 脚本只有一个 SSPanel 签到，如需使用请参考 `env.sample` 配置 `.env` 后放入 `script/Lists` 或 `/ql/config` 文件夹
* 支持自定义配置文件路径
    - 环境变量 / store KEY 名称：`ENV_PATH`
    - 参考值 / VALUE：`/usr/local/app/script/.env`

### 4. **添加了欢太商城的签到配置**

* [欢太商城 HttpCanary 抓包教程](https://github.com/hwkxk/HeytapTask/wiki/%E6%AC%A2%E5%A4%AA%E5%95%86%E5%9F%8EHttpCanary%E6%8A%93%E5%8C%85%E6%95%99%E7%A8%8B)
* 部分域名屏蔽境外 IP 访问，所以本项目不适于在 非中国 IP 代理网络下 / Github Actions / 境外 VPS 上运行!
* 从未在欢太商城做过任务，请先手动进入任务中心完成一下任务再使用，否则可能无法获取到任务列表数据导致出错！@YYplus

### 5. **添加了时光相册的签到配置**

[![4tWaFg.png](https://z3.ax1x.com/2021/09/22/4tWaFg.png)](https://imgtu.com/i/4tWaFg)

## 其他说明

1. 请自行修改执行时间

2. elecV2P 运行 `手动更新` 任务可强制同步本仓库

3. 大部分脚本移植于 [Sitoi](https://github.com/Sitoi/dailycheckin)，Sitoi 于 2021 年 9 月 3 日 [dailycheckin-0.1.7](https://files.pythonhosted.org/packages/ee/8d/b49624a4d11c51f4e3dfb98f622d0c1ffe5d6315ad39452859ea8703206f/dailycheckin-0.1.7.tar.gz)  版本适配了青龙，[使用教程](https://sitoi.gitee.io/dailycheckin/qinglong/)与本仓库教程不相同，切勿使用本仓库 [checkinpanel](https://github.com/Oreomeow/checkinpanel) 的同时去问大佬

4. 2021 年 9 月 13 日起不再更新 `.json` 后缀的配置文件

## 计划说明

| 状态 | \*语言 | \*备注 | 名称 |
| --- | --- | --- | --- |
* [x] 𝑷𝒚𝒕𝒉𝒐𝒏 | api | LeetCode 每日一题 | 每日一句 | 天气预报
* [x] 𝑷𝒚𝒕𝒉𝒐𝒏 | 多账号 | AcFun | 百度搜索资源平台 | Bilibili | 天翼云盘 | CSDN | 多看阅读 | 恩山论坛 | Fa米家 | 网易云游戏 | 葫芦侠 | 爱奇艺 | 全民K歌 | MEIZU 社区 | 芒果 TV | 小米运动 | 网易云音乐 | 一加手机社区官方论坛 | 哔咔漫画 | 吾爱破解 | 什么值得买 | 百度贴吧 | V2EX | 腾讯视频 | 微博 | 联通沃邮箱 | 哔咔网单 | 王者营地 | 有道云笔记 | 智友邦
* [x] 𝑷𝒚𝒕𝒉𝒐𝒏 | 多账号 | 机场签到 | 欢太商城 | NGA | 掘金 | GLaDOS | HiFiNi | 时光相册 | 联通营业厅 | 无忧行 | FreeNom
* [x] 𝑺𝒉𝒆𝒍𝒍 | 多账号 | SSPanel 签到

### 项目完成情况

* [x] 多账号补全
* [x] 配置文件由严格的 `.json` 向支持注释的 `.json5` 过渡
* [x] 更多环境适配
* [x] 配置文件支持自定义路径
* [x] 通知多线程
* [x] 通知输出优化
* [x] 通知方式增加，如飞书
* [x] Shell 消息推送、环境检查单列
* [ ] cron 随机
* [ ] elecV2P 任务列表自动更新
* [ ] 任务多合一执行
* [ ] 英文文档编写

### 测试情况

| 状态 | 名称 |
| --- | --- |
| ✅ | LeetCode 每日一题 \| 每日一句 \| 天气预报 \| AcFun \| 机场签到 \| Bilibili \| 天翼云盘 \| CSDN \| 多看阅读 \| 恩山论坛 \| 时光相册 \| FreeNom \| GLaDOS \| 网易云游戏 \| 欢太商城 \| HiFiNi \| 爱奇艺 \| 掘金 \| 全民K歌 \| MEIZU 社区 \| 小米运动 \| 网易云音乐 \| NGA \| 一加手机社区官方论坛 \| 吾爱破解 \| 什么值得买 \| SSPanel 签到 \| 百度贴吧 \| 腾讯视频 \| 微博 \| 王者营地 \| 有道云笔记 |
| ❔ | 百度搜索资源平台 \| Fa米家 \| 葫芦侠 \| 无忧行 \| 芒果 TV \| 哔咔漫画 \| 联通营业厅 \| V2EX \| 联通沃邮箱 \| 哔咔网单 \| 智友邦 |

## 致谢

[@𝐰𝐞𝐧𝐦𝐨𝐮𝐱](https://github.com/Wenmoux/) -------- 𝗰𝗵𝗲𝗰𝗸𝗯𝗼𝘅

[@𝐒𝐢𝐭𝐨𝐢](https://github.com/Sitoi) ----------- 𝗱𝗮𝗶𝗹𝘆𝗰𝗵𝗲𝗰𝗸𝗶𝗻

[@𝐲𝐮𝐱𝐢𝐚𝐧𝟏𝟓𝟖](https://github.com/yuxian158) ---- 𝗾𝗹-𝗰𝗵𝗲𝗰𝗸𝗯𝗼𝘅

[@𝐢𝐬𝐞𝐜𝐫𝐞𝐭](https://github.com/isecret) ------- 𝗦𝗦𝗣𝗮𝗻𝗲𝗹 𝗦𝗵𝗲𝗹𝗹

[@𝐡𝐰𝐤𝐱𝐤](https://github.com/hwkxk) -------------- 𝗛𝗲𝘆𝗧𝗮𝗽

@𝑶𝒕𝒉𝒆𝒓𝒔 ----- 𝔰𝔠𝔯𝔦𝔭𝔱 𝔠𝔬𝔪𝔪𝔢𝔫𝔱𝔰

## 历史 Star 数

[![Stargazers over time](https://starchart.cc/Oreomeow/checkinpanel.svg)](https://starchart.cc/Oreomeow/checkinpanel)
