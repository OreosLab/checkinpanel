<div align="center"> 
<h1 align="center">签到盒 elecV2P 版</h1>
</div>

![GitHub stars](https://img.shields.io/github/stars/Oreomeow/dailycheckinV2P?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/Oreomeow/dailycheckinV2P?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/Oreomeow/dailycheckinV2P?style=flat-square)
![GitHub issues](https://img.shields.io/github/languages/code-size/Oreomeow/dailycheckinV2P?style=flat-square)


# 一个运行在 elecV2P 的签到函数

[elecV2P](https://github.com/elecV2/elecV2P.git)

## 特别声明

- 本仓库发布的脚本及其中涉及的任何解锁和解密分析脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

- 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

- 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害。

- 间接使用脚本的任何用户，包括但不限于建立 VPS 或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 本人对于由此引起的任何隐私泄漏或其他后果概不负责。

- 请勿将本仓库的任何内容用于商业或非法目的，否则后果自负。

- 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

- 任何以任何方式查看此项目的人或直接或间接使用该项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或 Script 项目的规则，则视为您已接受此免责声明。

**您必须在下载后的24小时内从计算机或手机中完全删除以上内容**

> ***您使用或者复制了本仓库且本人制作的任何脚本，则视为 `已接受` 此声明，请仔细阅读***

## 使用方法

1. TASK -> 添加订阅任务 -> 修改名称、更新方式、任务 -> 获取内容 -> 全部添加

名称：签到项目

同名任务更新方式：`替换`

任务：

```
https://raw.githubusercontent.com/Oreomeow/dailycheckinV2P/master/dailycheckin.json
```

2. 下载 [check.sample.json](https://raw.githubusercontent.com/Oreomeow/dailycheckinV2P/master/check.sample.json)，根据 [Sitoi](https://github.com/Sitoi/dailycheckin) 的[配置说明](https://sitoi.gitee.io/dailycheckin/settings/)进行抓包并配置

3. 将 `check.sample.json` 重命名为 `check.json` 后放入 `script/Shell` 文件夹

- OVERVIEW -> EFSS 文件管理界面 -> 是否开启 EFSS 功能：开启 -> 目录：`./script/Shell` -> 选择文件：`check.json` -> 开始上传

4. JSMANAGE -> store/cookie 常量储存管理填写通知环境变量

| 变量 | 描述 | 参考 |
| --- | --- |  --- |
| BARK | bark 服务 | BARK 推送[使用](https://github.com/Sitoi/dailycheckin/issues/29)，填写 `BARK_URL` 即可，例如：`https://api.day.app/DxHcxxxxxRxxxxxxcm/`，此参数如果以 `http` 或者 `https` 开头则判定为自建 bark 服务 |
| SCKEY | Server 酱 | server 酱推送[官方文档](https://sc.ftqq.com/3.version)，填写 `SCKEY` 代码即可
| TG_BOT_TOKEN | tg 机器人 | 申请 @BotFather 的 Token，如 `10xxx4:AAFcqxxxxgER5uw` |
| TG_USER_ID | tg 机器人 | @getuseridbot 中获取到的纯数字 ID，如 `1434078534` |
| TG_API_HOST | * tg 代理 api | Telegram api 自建的反向代理地址 例子：反向代理地址 `http://aaa.bbb.ccc` 则填写 aaa.bbb.ccc [简略搭建教程](https://shimo.im/docs/JD38CJDQtYy3yTd8/read) |
| TG_PROXY_IP | * tg 机器人代理 IP 地址 | 代理类型为 http，比如您代理是 `http://127.0.0.1:1080`，则填写 `127.0.0.1`，有密码例子: `username:password@127.0.0.1` |
| TG_PROXY_PORT | * tg 机器人代理端口 | 代理端口号，代理类型为 http，比如您代理是 `http://127.0.0.1:1080`，则填写 `1080` |
| DD_BOT_ACCESS_TOKEN | 钉钉机器人 | 钉钉推送[官方文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)，只需 `https://oapi.dingtalk.com/robot/send?access_token=XXX` 等于符号后面的 `XXX` |
| DD_BOT_SECRET | 钉钉机器人 | 钉钉推送[官方文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)密钥，机器人安全设置页面，加签一栏下面显示的 `SEC` 开头的字符串, 注:填写了 `DD_BOT_TOKEN` 和 `DD_BOT_SECRET`，钉钉机器人安全设置只需勾选加签即可，其他选项不要勾选 |
| QQ_SKEY | Cool Push | [Cool Push](https://cp.xuthus.cc/) 推送的 `SKEY` |
| QQ_MODE | Cool Push 推送方式 | [Cool Push](https://cp.xuthus.cc/) 推送方式：QQ、微信、邮件 |
| QYWX_APP | 企业微信应用 | 参考 http://note.youdao.com/s/HMiudGkb |
| PUSH_PLUS_TOKEN | pushplus | 用户令牌，可直接加到请求地址后，如：`http://www.pushplus.plus/send/{token}` [官方文档](https://www.pushplus.plus/doc/) |
| GOBOT_URL | go-cqhttp | 例如：推送到个人QQ：`http://127.0.0.1/send_private_msg` 群：`http://127.0.0.1/send_group_msg` |
| GOBOT_TOKEN | * go-cqhttp 的 access_token | go-cqhttp 文件设置的访问密钥 |
| GOBOT_QQ | go-cqhttp 的推送群或者用户 | `GOBOT_URL` 设置 `/send_private_msg` 则需要填入 `user_id=个人QQ` 相反如果是 `/send_group_msg` 则需要填入 `group_id=QQ群` |

*\*表示选填*

- 调用模块

> [checksendNotify.py](https://raw.githubusercontent.com/Oreomeow/dailycheckinV2P/master/checksendNotify.py)

## 修改说明

### 1. **添加了葫芦侠的签到配置**

​	参数说明：`HLX.user`：用户名 `HLX.password`：密码的MD532位小写加密[生成](https://md5jiami.bmcx.com/)

### 2. **添加了网易云游戏的签到配置**

[官网](https://cg.163.com/#/mobile)

参数说明：`163game.Authorization`

登录后抓取签到请求（一般请求的请求头也有这个字段）

[![fMdyEq.png](https://z3.ax1x.com/2021/08/07/fMdyEq.png)](https://imgtu.com/i/fMdyEq)

## 其他说明

1. 请自行修改执行时间

2. 运行 `签到更新` 任务可强制同步本仓库

3. [青龙面板平台签到函数](https://github.com/yuxian158/check)

## 致谢

[@Wenmoux](https://github.com/Wenmoux/)  

[@MayoBlueSky](https://github.com/MayoBlueSky)

[@Sitoi](https://github.com/Sitoi)

[@yuxian158](https://github.com/yuxian158)
