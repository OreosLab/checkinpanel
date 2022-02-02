"""
:author @luminoleon
cron: 50 1 * * *
new Env('Epic');
"""

import argparse
import asyncio
import base64
import datetime
import hashlib
import hmac
import json
import os
import re
import signal
import sys
import time
import urllib
from getpass import getpass
from json.decoder import JSONDecodeError
from typing import Callable, Dict, List, Optional, Tuple, Union

import requests
import schedule
from pyppeteer import launch, launcher
from pyppeteer.element_handle import ElementHandle
from pyppeteer.frame_manager import Frame
from pyppeteer.network_manager import Request

from notify_mtr import send
from utils import get_data
from utils_env import get_env_str

__version__ = "1.6.15"


class texts:
    class zh:
        NOTIFICATION_TITLE_START = "Epicgames Claimer：启动成功"
        NOTIFICATION_TITLE_NEED_LOGIN = "Epicgames Claimer：需要登录"
        NOTIFICATION_TITLE_CLAIM_SUCCEED = "Epicgames Claimer：领取成功"
        NOTIFICATION_TITLE_ERROR = "EpicGames Claimer：错误"
        NOTIFICATION_TITLE_TEST = "EpicGames Claimer：测试"
        NOTIFICATION_CONTENT_START = "如果你收到了此消息，表示你可以正常接收来自Epicgames Claimer的通知推送"
        NOTIFICATION_CONTENT_NEED_LOGIN = "未登录或登录信息已失效，请检查并尝试重新登录"
        NOTIFICATION_CONTENT_CLAIM_SUCCEED = "成功领取到游戏："
        NOTIFICATION_CONTENT_OPEN_BROWSER_FAILED = "打开浏览器失败："
        NOTIFICATION_CONTENT_LOGIN_FAILED = "登录失败："
        NOTIFICATION_CONTENT_CLAIM_FAILED = "领取失败："
        NOTIFICATION_CONTENT_TEST = "测试是否通知推送已被正确设置"
        NOTIFICATION_CONTENT_OWNED_ALL = "所有可领取的每周免费游戏已全部在库中"

    class en:
        NOTIFICATION_TITLE_START = "Epicgames Claimer: Startup success"
        NOTIFICATION_TITLE_NEED_LOGIN = "Epicgames Claimer: Login required"
        NOTIFICATION_TITLE_CLAIM_SUCCEED = "Epicgames Claimer: Successfully claimed"
        NOTIFICATION_TITLE_ERROR = "EpicGames Claimer: Error"
        NOTIFICATION_TITLE_TEST = "EpicGames Claimer: Test"
        NOTIFICATION_CONTENT_START = "If you receive this message, it means that you can be notified from the Epicgames Claimer"
        NOTIFICATION_CONTENT_NEED_LOGIN = (
            "Login information lost or expired, please try to re-login"
        )
        NOTIFICATION_CONTENT_CLAIM_SUCCEED = "Successfully claimed the game: "
        NOTIFICATION_CONTENT_OPEN_BROWSER_FAILED = "Error when opening the browser: "
        NOTIFICATION_CONTENT_LOGIN_FAILED = "Login failure: "
        NOTIFICATION_CONTENT_CLAIM_FAILED = "Claim failure: "
        NOTIFICATION_CONTENT_TEST = (
            "Test if the notification setting is functional or not "
        )
        NOTIFICATION_CONTENT_OWNED_ALL = (
            "All claimable weekly free games are already in the liabrary"
        )

    class ru:
        NOTIFICATION_TITLE_START = "Epicgames Claimer: Запущен"
        NOTIFICATION_TITLE_NEED_LOGIN = "Epicgames Claimer: Требуется логин"
        NOTIFICATION_TITLE_CLAIM_SUCCEED = "Epicgames Claimer: Успешно собранно"
        NOTIFICATION_TITLE_ERROR = "EpicGames Claimer: Ошибка"
        NOTIFICATION_TITLE_TEST = "EpicGames Claimer: Test"
        NOTIFICATION_CONTENT_START = "Если вы получили это сообщение, это означает, что вы можете получать уведомления от Epicgames Claimer"
        NOTIFICATION_CONTENT_NEED_LOGIN = "Информация для входа потеряна или срок ее действия истек, попробуйте повторно войти"
        NOTIFICATION_CONTENT_CLAIM_SUCCEED = "Успешно полученна игра: "
        NOTIFICATION_CONTENT_OPEN_BROWSER_FAILED = "Ошибка при открытии браузера: "
        NOTIFICATION_CONTENT_LOGIN_FAILED = "Ошибка входа: "
        NOTIFICATION_CONTENT_CLAIM_FAILED = "Ошибка получения игры: "
        NOTIFICATION_CONTENT_TEST = (
            "Проверка, работает ли настройка уведомлений или нет "
        )
        NOTIFICATION_CONTENT_OWNED_ALL = "Все еженедельные бесплатные игры, которые можно получить, уже находятся в библиотеке."


local_texts = texts.en


if "--enable-automation" in launcher.DEFAULT_ARGS:
    launcher.DEFAULT_ARGS.remove("--enable-automation")
# Solve the issue of zombie processes
if "SIGCHLD" in dir(signal):
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)


def get_current_time() -> str:
    current_time_string = str(datetime.datetime.now()).split(".")[0]
    return current_time_string


def log(text: str, level: str = "info") -> None:
    localtime = get_current_time()
    if level == "info":
        print("[{}  INFO] {}".format(localtime, text))
    elif level == "warning":
        print("\033[33m[{}  WARN] {}\033[0m".format(localtime, text))
    elif level == "error":
        print("\033[31m[{} ERROR] {}\033[0m".format(localtime, text))


class WeChat:
    def __init__(self, corpid, corpsecret, agentid) -> None:
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid

    def get_token(self) -> str:
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(
            self.corpid, self.corpsecret
        )
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            log("Failed to get access_token.", level="error")
            return ""

    def send_text(self, message, touser="@all") -> str:
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(
            self.get_token()
        )
        data = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {"content": message},
            "safe": 0,
        }
        send_msges = bytes(json.dumps(data), "utf-8")
        response = requests.post(url, send_msges)
        return response

    def send_mpnews(self, title, message, media_id, touser="@all") -> str:
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(
            self.get_token()
        )
        if not message:
            message = title
        data = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.agentid,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "content_source_url": "",
                        "content": message.replace("\n", "<br/>"),
                        "digest": message,
                    }
                ]
            },
            "safe": 0,
        }
        send_msges = bytes(json.dumps(data), "utf-8")
        response = requests.post(url, send_msges)
        return response


class Notifications:
    def __init__(
        self,
        serverchan_sendkey: str = None,
        bark_push_url: str = "https://api.day.app/push",
        bark_device_key: str = None,
        telegram_bot_token: str = None,
        telegram_chat_id: str = None,
        wechat_qywx_am: str = None,
        dingtalk_access_token: str = None,
        dingtalk_secret: str = None,
    ) -> None:
        self.serverchan_sendkey = serverchan_sendkey
        self.bark_push_url = bark_push_url
        self.bark_device_key = bark_device_key
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.wechat_qywx_am = wechat_qywx_am
        self.dingtalk_access_token = dingtalk_access_token
        self.dingtalk_secret = dingtalk_secret

    def push_serverchan(self, title: str, content: str = None) -> None:
        if self.serverchan_sendkey != None:
            try:
                url = "https://sctapi.ftqq.com/{}.send".format(self.serverchan_sendkey)
                data = {"title": title}
                if content != None:
                    data["desp"] = content
                requests.post(url, data=data)
            except Exception as e:
                log("Failed to push to ServerChan: {}".format(e), "error")

    def push_bark(self, title: str, content: str = None) -> None:
        if self.bark_device_key:
            try:
                response = requests.post(
                    url=self.bark_push_url,
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps(
                        {
                            "body": content,
                            "device_key": self.bark_device_key,
                            "title": title,
                        }
                    ),
                )
                log(f"Bark Response HTTP Status Code: {response.status_code}")
                log(f"Bark Response HTTP Response Body: {response.content}")
            except Exception as e:
                log("Failed to push to Bark: {}".format(e), "error")

    def push_telegram(self, title: str = None, content: str = None) -> None:
        if self.telegram_bot_token:
            try:
                push_text = f"{title}\n\n{content}" if title else content
                response = requests.post(
                    url=f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
                    data={"chat_id": self.telegram_chat_id, "text": push_text},
                )
                log(f"Telegram Response HTTP Status Code: {response.status_code}")
                log(f"Telegram Response HTTP Response Body: {response.content}")
            except Exception as e:
                log("Failed to push to Telegram: {}".format(e), "error")

    def push_wechat(self, title: str, content: str = None) -> None:
        if self.wechat_qywx_am:
            try:
                qywx_am_ay = re.split(",", self.wechat_qywx_am)
                if 4 < len(qywx_am_ay) > 5:
                    log("WeChat AM is invalid.", level="error")
                    return
                corpid = qywx_am_ay[0]
                corpsecret = qywx_am_ay[1]
                touser = qywx_am_ay[2]
                agentid = qywx_am_ay[3]
                try:
                    media_id = qywx_am_ay[4]
                except:
                    media_id = None
                wx = WeChat(corpid, corpsecret, agentid)
                if media_id != None:
                    response = wx.send_mpnews(title, content, media_id, touser)
                else:
                    message = title + "\n\n" + content
                    response = wx.send_text(message, touser)
                response = response.json()
                if response["errmsg"] == "ok":
                    log("Successfully sent wechat message.")
                else:
                    log(
                        "Failed to send wechat message. errmsg: {}".format(
                            response["errmsg"]
                        ),
                        level="error",
                    )
            except Exception as e:
                log("Failed to send wechat message. ExceptErrmsg:{}".format(e), "error")

    def _get_dingtalk_timestamp_and_sign(self) -> Tuple[str, str]:
        timestamp = str(round(time.time() * 1000))
        secret = self.dingtalk_secret
        secret_enc = secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def push_dingtalk(self, title: str, content: str) -> None:
        if self.dingtalk_access_token:
            try:
                headers = {"Content-Type": "application/json; charset=utf-8"}
                webhook = "https://oapi.dingtalk.com/robot/send"
                params = {"access_token": self.dingtalk_access_token}
                if self.dingtalk_secret:
                    (
                        params["timestamp"],
                        params["sign"],
                    ) = self._get_dingtalk_timestamp_and_sign()
                push_text = f"{title}\n\n{content}" if title else content
                data = {"msgtype": "text", "text": {"content": push_text}}
                response = requests.post(
                    url=webhook, headers=headers, params=params, data=json.dumps(data)
                )
                response_json = response.json()
                errcode = response_json["errcode"]
                errmsg = response_json["errmsg"]
                if errcode == 0:
                    log("Successfully sent DingTalk message")
                else:
                    log(f"Failed to send Dingtalk message: {errmsg}", level="error")
            except Exception as e:
                log(f"Failed to send Dingtalk message: {e}", level="error")

    def notify(self, title: str, content: str = None) -> None:
        self.push_serverchan(title, content)
        self.push_bark(title, content)
        self.push_telegram(title, content)
        self.push_wechat(title, content)
        self.push_dingtalk(title, content)


class Item:
    def __init__(
        self,
        title: str,
        offer_id: str,
        namespace: str,
        type: str,
        store_url_slug: str = None,
    ) -> None:
        self.title = title
        self.offer_id = offer_id
        self.namespace = namespace
        self.type = type
        self._store_url_slug = store_url_slug

    @property
    def purchase_url(self) -> str:
        url = "https://www.epicgames.com/store/purchase?lang=en-US&namespace={}&offers={}".format(
            self.namespace, self.offer_id
        )
        return url

    @property
    def store_url(self) -> str:
        return (
            f"https://www.epicgames.com/store/en-US/p/{self._store_url_slug}"
            if self._store_url_slug
            else None
        )


class Game:
    def __init__(self, base_game: Item, dlcs: List[Item] = []) -> None:
        self.base_game = base_game
        self.dlcs = dlcs

    @property
    def item_amount(self) -> int:
        return len(self.dlcs) + 1


class EpicgamesClaimer:
    def __init__(
        self,
        data_dir: Optional[str] = None,
        headless: bool = True,
        sandbox: bool = False,
        chromium_path: Optional[str] = None,
        claimer_notifications: Notifications = None,
        timeout: int = 180000,
        debug: bool = False,
        cookies: str = None,
        browser_args: List[str] = [
            "--disable-infobars",
            "--blink-settings=imagesEnabled=false",
            "--no-first-run",
            "--disable-gpu",
        ],
        push_when_owned_all=False,
    ) -> None:
        self.data_dir = data_dir
        self.headless = headless
        self.browser_args = browser_args
        self.sandbox = sandbox
        if not self.sandbox:
            self.browser_args.append("--no-sandbox")
        self.chromium_path = chromium_path
        if "win" in launcher.current_platform() and self.chromium_path == None:
            if os.path.exists("chrome-win32"):
                self.chromium_path = "chrome-win32/chrome.exe"
            elif os.path.exists("chrome-win"):
                self.chromium_path = "chrome-win/chrome.exe"
        self._loop = asyncio.get_event_loop()
        self.browser_opened = False
        self.claimer_notifications = (
            claimer_notifications if claimer_notifications != None else Notifications()
        )
        self.timeout = timeout
        self.debug = debug
        self.cookies = cookies
        self.push_when_owned_all = push_when_owned_all
        self.page = None
        self.open_browser()

    def log(self, text: str, level: str = "info") -> None:
        localtime = get_current_time()
        if level == "info":
            print("[{}  INFO] {}".format(localtime, text))
        elif level == "warning":
            print("\033[33m[{}  WARN] {}\033[0m".format(localtime, text))
        elif level == "error":
            print("\033[31m[{} ERROR] {}\033[0m".format(localtime, text))
        elif level == "debug":
            if self.debug:
                print("[{} DEBUG] {}".format(localtime, text))

    async def _headless_stealth_async(self):
        original_user_agent = await self.page.evaluate("navigator.userAgent")
        user_agent = original_user_agent.replace("Headless", "")
        await self.page.evaluateOnNewDocument(
            "() => {Object.defineProperty(navigator, 'webdriver', {get: () => false})}"
        )
        await self.page.evaluateOnNewDocument(
            "window.chrome = {'loadTimes': {}, 'csi': {}, 'app': {'isInstalled': false, 'getDetails': {}, 'getIsInstalled': {}, 'installState': {}, 'runningState': {}, 'InstallState': {'DISABLED': 'disabled', 'INSTALLED': 'installed', 'NOT_INSTALLED': 'not_installed'}, 'RunningState': {'CANNOT_RUN': 'cannot_run', 'READY_TO_RUN': 'ready_to_run', 'RUNNING': 'running'}}, 'webstore': {'onDownloadProgress': {'addListener': {}, 'removeListener': {}, 'hasListener': {}, 'hasListeners': {}, 'dispatch': {}}, 'onInstallStageChanged': {'addListener': {}, 'removeListener': {}, 'hasListener': {}, 'hasListeners': {}, 'dispatch': {}}, 'install': {}, 'ErrorCode': {'ABORTED': 'aborted', 'BLACKLISTED': 'blacklisted', 'BLOCKED_BY_POLICY': 'blockedByPolicy', 'ICON_ERROR': 'iconError', 'INSTALL_IN_PROGRESS': 'installInProgress', 'INVALID_ID': 'invalidId', 'INVALID_MANIFEST': 'invalidManifest', 'INVALID_WEBSTORE_RESPONSE': 'invalidWebstoreResponse', 'LAUNCH_FEATURE_DISABLED': 'launchFeatureDisabled', 'LAUNCH_IN_PROGRESS': 'launchInProgress', 'LAUNCH_UNSUPPORTED_EXTENSION_TYPE': 'launchUnsupportedExtensionType', 'MISSING_DEPENDENCIES': 'missingDependencies', 'NOT_PERMITTED': 'notPermitted', 'OTHER_ERROR': 'otherError', 'REQUIREMENT_VIOLATIONS': 'requirementViolations', 'USER_CANCELED': 'userCanceled', 'WEBSTORE_REQUEST_ERROR': 'webstoreRequestError'}, 'InstallStage': {'DOWNLOADING': 'downloading', 'INSTALLING': 'installing'}}}"
        )
        await self.page.evaluateOnNewDocument(
            "() => {Reflect.defineProperty(navigator.connection,'rtt', {get: () => 200, enumerable: true})}"
        )
        await self.page.evaluateOnNewDocument(
            "() => {Object.defineProperty(navigator, 'plugins', {get: () => [{'description': 'Portable Document Format', 'filename': 'internal-pdf-viewer', 'length': 1, 'name': 'Chrome PDF Plugin'}, {'description': '', 'filename': 'mhjfbmdgcfjbbpaeojofohoefgiehjai', 'length': 1, 'name': 'Chromium PDF Viewer'}, {'description': '', 'filename': 'internal-nacl-plugin', 'length': 2, 'name': 'Native Client'}]})}"
        )
        await self.page.evaluateOnNewDocument(
            "() => {const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto}"
        )
        await self.page.evaluateOnNewDocument(
            "const getParameter = WebGLRenderingContext.getParameter; WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'Intel Open Source Technology Center';}; if (parameter === 37446) {return 'Mesa DRI Intel(R) Ivybridge Mobile ';}; return getParameter(parameter);}"
        )
        await self.page.evaluateOnNewDocument(
            "() => {Reflect.defineProperty(navigator, 'mimeTypes', {get: () => [{type: 'application/pdf', suffixes: 'pdf', description: '', enabledPlugin: Plugin}, {type: 'application/x-google-chrome-pdf', suffixes: 'pdf', description: 'Portable Document Format', enabledPlugin: Plugin}, {type: 'application/x-nacl', suffixes: '', description: 'Native Client Executable', enabledPlugin: Plugin}, {type: 'application/x-pnacl', suffixes: '', description: 'Portable Native Client Executable', enabledPlugin: Plugin}]})}"
        )
        await self.page.evaluateOnNewDocument(
            "() => {const p = {'defaultRequest': null, 'receiver': null}; Reflect.defineProperty(navigator, 'presentation', {get: () => p})}"
        )
        await self.page.setExtraHTTPHeaders(
            {"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
        )
        await self.page.setUserAgent(user_agent)

    async def _open_browser_async(self) -> None:
        if not self.browser_opened:
            self.browser = await launch(
                options={"args": self.browser_args, "headless": self.headless},
                userDataDir=None
                if self.data_dir == None
                else os.path.abspath(self.data_dir),
                executablePath=self.chromium_path,
            )
            self.page = (await self.browser.pages())[0]
            await self.page.setViewport({"width": 600, "height": 1000})
            # Async callback functions aren't possible to use (Refer to https://github.com/pyppeteer/pyppeteer/issues/220).
            # await self.page.setRequestInterception(True)
            # self.page.on('request', self._intercept_request_async)
            if self.headless:
                await self._headless_stealth_async()
            self.browser_opened = True
            if self.cookies:
                await self._load_cookies_async(self.cookies)
            if self.data_dir != None:
                cookies_path = os.path.join(self.data_dir, "cookies.json")
                if os.path.exists(cookies_path):
                    await self._load_cookies_async(cookies_path)
                    os.remove(cookies_path)
        # await self._refresh_cookies_async()

    async def _refresh_cookies_async(self) -> None:
        await self._navigate_async("https://www.epicgames.com/store/en-US/")

    async def _intercept_request_async(self, request: Request) -> None:
        if request.resourceType in ["image", "media", "font"]:
            await request.abort()
        else:
            await request.continue_()

    async def _close_browser_async(self):
        if self.browser_opened:
            if self.cookies:
                await self._save_cookies_async(self.cookies)
            await self.browser.close()
            self.browser_opened = False

    async def _type_async(
        self, selector: str, text: str, sleep: Union[int, float] = 0
    ) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep)
        await self.page.type(selector, text)

    async def _click_async(
        self,
        selector: str,
        sleep: Union[int, float] = 2,
        timeout: int = 30000,
        frame: Frame = None,
    ) -> None:
        if frame == None:
            frame = self.page
        await frame.waitForSelector(selector, options={"timeout": timeout})
        await asyncio.sleep(sleep)
        await frame.click(selector)

    async def _get_text_async(self, selector: str, frame: Frame = None) -> str:
        if frame == None:
            frame = self.page
        await self.page.waitForSelector(selector, options={"timeout": self.timeout})
        return await (
            await (await self.page.querySelector(selector)).getProperty("textContent")
        ).jsonValue()

    async def _get_texts_async(self, selector: str) -> List[str]:
        texts = []
        try:
            await self.page.waitForSelector(selector)
            for element in await self.page.querySelectorAll(selector):
                texts.append(
                    await (await element.getProperty("textContent")).jsonValue()
                )
        except:
            pass
        return texts

    async def _get_element_text_async(self, element: ElementHandle) -> str:
        return await (await element.getProperty("textContent")).jsonValue()

    async def _get_property_async(self, selector: str, property: str) -> str:
        await self.page.waitForSelector(selector, options={"timeout": self.timeout})
        return await self.page.evaluate(
            "document.querySelector('{}').getAttribute('{}')".format(selector, property)
        )

    async def _get_links_async(
        self, selector: str, filter_selector: str, filter_value: str
    ) -> List[str]:
        links = []
        try:
            await self.page.waitForSelector(selector)
            elements = await self.page.querySelectorAll(selector)
            judgement_texts = await self._get_texts_async(filter_selector)
        except:
            return []
        for element, judgement_text in zip(elements, judgement_texts):
            if judgement_text == filter_value:
                link = await (await element.getProperty("href")).jsonValue()
                links.append(link)
        return links

    async def _find_async(
        self, selectors: Union[str, List[str]], timeout: int = None, frame: Frame = None
    ) -> Union[bool, int]:
        if frame == None:
            frame = self.page
        if type(selectors) == str:
            try:
                if timeout == None:
                    timeout = 1000
                await frame.waitForSelector(selectors, options={"timeout": timeout})
                return True
            except:
                return False
        elif type(selectors) == list:
            if timeout == None:
                timeout = 300000
            for _ in range(int(timeout / 1000 / len(selectors))):
                for i in range(len(selectors)):
                    if await self._find_async(selectors[i], timeout=1000, frame=frame):
                        return i
            return -1
        else:
            raise ValueError

    async def _try_click_async(
        self, selector: str, sleep: Union[int, float] = 2, frame: Frame = None
    ) -> bool:
        if frame == None:
            frame = self.page
        try:
            await asyncio.sleep(sleep)
            await frame.click(selector)
            return True
        except:
            return False

    async def _get_elements_async(
        self, selector: str
    ) -> Union[List[ElementHandle], None]:
        try:
            await self.page.waitForSelector(selector)
            return await self.page.querySelectorAll(selector)
        except:
            return None

    async def _wait_for_text_change_async(self, selector: str, text: str) -> None:
        if await self._get_text_async(selector) != text:
            return
        for _ in range(int(self.timeout / 1000)):
            await asyncio.sleep(1)
            if await self._get_text_async(selector) != text:
                return
        raise TimeoutError(
            'Waiting for "{}" text content change failed: timeout {}ms exceeds'.format(
                selector, self.timeout
            )
        )

    async def _wait_for_element_text_change_async(
        self, element: ElementHandle, text: str
    ) -> None:
        if await self._get_element_text_async(element) != text:
            return
        for _ in range(int(self.timeout / 1000)):
            await asyncio.sleep(1)
            if await self._get_element_text_async(element) != text:
                return
        raise TimeoutError(
            'Waiting for element "{}" text content change failed: timeout {}ms exceeds'.format(
                element, self.timeout
            )
        )

    async def _navigate_async(
        self, url: str, timeout: int = 30000, reload: bool = True
    ) -> None:
        if self.page.url == url and not reload:
            return
        await self.page.goto(url, options={"timeout": timeout})

    async def _get_json_async(self, url: str, arguments: Dict[str, str] = None) -> dict:
        response_text = await self._get_async(url, arguments)
        try:
            response_json = json.loads(response_text)
        except JSONDecodeError:
            response_text_partial = (
                response_text if len(response_text) <= 96 else response_text[0:96]
            )
            raise ValueError(
                "Epic Games returnes content that cannot be resolved. Response: {} ...".format(
                    response_text_partial
                )
            )
        return response_json

    async def _login_async(
        self,
        email: str,
        password: str,
        verifacation_code: str = None,
        interactive: bool = True,
        remember_me: bool = True,
    ) -> None:
        self.log("Start to login.", level="debug")
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        if password == None or password == "":
            raise ValueError("Password can't be null.")
        await self._navigate_async(
            "https://www.epicgames.com/store/en-US/", timeout=self.timeout, reload=False
        )
        await self._click_async("div.menu-icon", timeout=self.timeout)
        await self._click_async(
            "div.mobile-buttons a[href='/login']", timeout=self.timeout
        )
        await self._click_async("#login-with-epic", timeout=self.timeout)
        await self._type_async("#email", email)
        await self._type_async("#password", password)
        if not remember_me:
            await self._click_async("#rememberMe")
        await self._click_async("#sign-in[tabindex='0']", timeout=self.timeout)
        login_result = await self._find_async(
            [
                "#talon_frame_login_prod[style*=visible]",
                "div.MuiPaper-root[role=alert] h6[class*=subtitle1]",
                "input[name=code-input-0]",
                "#user",
            ],
            timeout=self.timeout,
        )
        if login_result == -1:
            raise TimeoutError("Check login result timeout.")
        elif login_result == 0:
            raise PermissionError(
                "CAPTCHA is required for unknown reasons when logging in"
            )
        elif login_result == 1:
            alert_text = await self._get_text_async(
                "div.MuiPaper-root[role=alert] h6[class*=subtitle1]"
            )
            raise PermissionError("From Epic Games: {}".format(alert_text))
        elif login_result == 2:
            if interactive:
                await self._type_async(
                    "input[name=code-input-0]", input("Verification code: ")
                )
            else:
                await self._type_async("input[name=code-input-0]", verifacation_code)
            await self._click_async("#continue[tabindex='0']", timeout=self.timeout)
            verify_result = await self._find_async(
                ["#modal-content div[role*=alert]", "#user"], timeout=self.timeout
            )
            if verify_result == -1:
                raise TimeoutError("Check login result timeout.")
            elif verify_result == 0:
                alert_text = await self._get_text_async(
                    "#modal-content div[role*=alert]"
                )
                raise PermissionError("From Epic Games: {}".format(alert_text))
        self.log("Login end.", level="debug")

    async def _need_login_async(self, use_api: bool = False) -> bool:
        need_login = False
        if use_api:
            page_content_json = await self._get_json_async(
                "https://www.epicgames.com/account/v2/ajaxCheckLogin"
            )
            need_login = page_content_json["needLogin"]
        else:
            await self._navigate_async(
                "https://www.epicgames.com/store/en-US/", timeout=self.timeout
            )
            if (
                await self._get_property_async("#user", "data-component")
            ) == "SignedIn":
                need_login = False
            else:
                need_login = True
        self.log(f"Need Login: {need_login}.", level="debug")
        return need_login

    async def _get_authentication_method_async(self) -> Optional[str]:
        page_content_json = await self._get_json_async(
            "https://www.epicgames.com/account/v2/security/settings/ajaxGet"
        )
        if page_content_json["settings"]["enabled"] == False:
            return None
        else:
            return page_content_json["settings"]["defaultMethod"]

    def _quit(self, signum=None, frame=None) -> None:
        try:
            self.close_browser()
        except:
            pass
        exit(1)

    def _screenshot(self, path: str) -> None:
        return self._loop.run_until_complete(self.page.screenshot({"path": path}))

    async def _post_json_async(
        self,
        url: str,
        data: str,
        host: str = "www.epicgames.com",
        sleep: Union[int, float] = 2,
    ):
        await asyncio.sleep(sleep)
        if not host in self.page.url:
            await self._navigate_async("https://{}".format(host))
        response = await self.page.evaluate(
            """
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "{}", true);
            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send('{}');
            xmlhttp.responseText;
        """.format(
                url, data
            )
        )
        return response

    async def _post_async(
        self,
        url: str,
        data: dict,
        host: str = "www.epicgames.com",
        sleep: Union[int, float] = 2,
    ) -> str:
        await asyncio.sleep(sleep)
        if not host in self.page.url:
            await self._navigate_async("https://{}".format(host))
        evaluate_form = "var form = new FormData();\n"
        for key, value in data.items():
            evaluate_form += "form.append(`{}`, `{}`);\n".format(key, value)
        response = await self.page.evaluate(
            evaluate_form
            + """
            var form = new FormData();
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", `{}`, true);
            xmlhttp.send(form);
            xmlhttp.responseText;
        """.format(
                url
            )
        )
        return response

    async def _get_account_id_async(self):
        if await self._need_login_async():
            return None
        else:
            await self._navigate_async("https://www.epicgames.com/account/personal")
            account_id = (
                await self._get_text_async("#personalView div.paragraph-container p")
            ).split(": ")[1]
            return account_id

    async def _get_async(
        self, url: str, arguments: Dict[str, str] = None, sleep: Union[int, float] = 2
    ):
        args = ""
        if arguments != None:
            args = "?"
            for key, value in arguments.items():
                args += "{}={}&".format(key, value)
            args = args.rstrip("&")
        await self._navigate_async(url + args)
        response_text = await self._get_text_async("body")
        await asyncio.sleep(sleep)
        return response_text

    async def _get_game_infos_async(self, url_slug: str):
        game_infos = {}
        response = await self._get_json_async(
            "https://store-content.ak.epicgames.com/api/en-US/content/products/{}".format(
                url_slug
            )
        )
        game_infos["product_name"] = response["productName"]
        game_infos["namespace"] = response["namespace"]
        game_infos["pages"] = []
        for page in response["pages"]:
            game_info_page = {}
            if page["offer"]["hasOffer"]:
                game_info_page["offer_id"] = page["offer"]["id"]
                game_info_page["namespace"] = page["offer"]["namespace"]
                game_infos["pages"].append(game_info_page)
        return game_infos

    def _get_purchase_url(self, namespace: str, offer_id: str):
        purchase_url = "https://www.epicgames.com/store/purchase?lang=en-US&namespace={}&offers={}".format(
            namespace, offer_id
        )
        return purchase_url

    async def _get_weekly_free_base_games_async(self) -> List[Item]:
        response_text = await self._get_async(
            "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
        )
        response_json = json.loads(response_text)
        base_games = []
        for item in response_json["data"]["Catalog"]["searchStore"]["elements"]:
            if {"path": "freegames"} in item["categories"]:
                if (
                    item["price"]["totalPrice"]["discountPrice"] == 0
                    and item["price"]["totalPrice"]["originalPrice"] != 0
                ):
                    if item["offerType"] == "BASE_GAME":
                        base_game = Item(
                            item["title"], item["id"], item["namespace"], "BASE_GAME"
                        )
                        base_games.append(base_game)
        return base_games

    async def _get_weekly_free_items_async(
        self, user_country: str = "CN"
    ) -> List[Item]:
        try:
            user_country = await self._get_user_country_async()
        except:
            pass
        response_text = await self._get_async(
            f"https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country={user_country}&allowCountries={user_country}"
        )
        response_json = json.loads(response_text)
        items = []
        for item in response_json["data"]["Catalog"]["searchStore"]["elements"]:
            if item["status"] == "ACTIVE":
                if {"path": "freegames"} in item["categories"]:
                    if item["price"]["totalPrice"]["discountPrice"] == 0:
                        if item["promotions"] != None:
                            if (
                                item["promotions"]["promotionalOffers"] != []
                                and item["promotions"]["promotionalOffers"] != None
                            ):
                                items.append(
                                    Item(
                                        item["title"],
                                        item["id"],
                                        item["namespace"],
                                        item["offerType"],
                                        item["productSlug"],
                                    )
                                )
        return items

    async def _get_free_dlcs_async(self, namespace: str) -> List[Item]:
        args = {
            "query": "query searchStoreQuery($namespace: String, $category: String, $freeGame: Boolean, $count: Int){Catalog{searchStore(namespace: $namespace, category: $category, freeGame: $freeGame, count: $count){elements{title id namespace}}}}",
            "variables": '{{"namespace": "{}", "category": "digitalextras/book|addons|digitalextras/soundtrack|digitalextras/video", "freeGame": true, "count": 1000}}'.format(
                namespace
            ),
        }
        response = await self._get_json_async("https://www.epicgames.com/graphql", args)
        free_dlcs = []
        for item in response["data"]["Catalog"]["searchStore"]["elements"]:
            free_dlc = Item(item["title"], item["id"], item["namespace"], "DLC")
            free_dlcs.append(free_dlc)
        return free_dlcs

    async def _get_free_base_game_async(self, namespace: str) -> Optional[Item]:
        args = {
            "query": "query searchStoreQuery($namespace: String, $category: String, $freeGame: Boolean, $count: Int){Catalog{searchStore(namespace: $namespace, category: $category, freeGame: $freeGame, count: $count){elements{title id namespace}}}}",
            "variables": '{{"namespace": "{}", "category": "games/edition/base", "freeGame": true, "count": 1000}}'.format(
                namespace
            ),
        }
        response = await self._get_json_async("https://www.epicgames.com/graphql", args)
        if len(response["data"]["Catalog"]["searchStore"]["elements"]) > 0:
            base_game_info = response["data"]["Catalog"]["searchStore"]["elements"][0]
            base_game = Item(
                base_game_info["title"],
                base_game_info["id"],
                base_game_info["namespace"],
                "BASE_GAME",
            )
            return base_game

    async def _get_weekly_free_games_async(self) -> List[Game]:
        free_items = await self._get_weekly_free_items_async()
        free_games = []
        for item in free_items:
            if item.type == "BASE_GAME":
                free_dlcs = await self._get_free_dlcs_async(item.namespace)
                free_games.append(Game(item, free_dlcs))
            elif item.type == "DLC":
                free_base_game = await self._get_free_base_game_async(item.namespace)
                if free_base_game != None:
                    free_dlcs = await self._get_free_dlcs_async(
                        free_base_game.namespace
                    )
                    free_games.append(Game(free_base_game, free_dlcs))
            else:
                free_base_game = await self._get_free_base_game_async(item.namespace)
                if free_base_game == None:
                    free_games.append(Game(item))
                else:
                    free_dlcs = await self._get_free_dlcs_async(
                        free_base_game.namespace
                    )
                    free_games.append(Game(free_base_game, free_dlcs))
        return free_games

    async def _claim_async(self, item: Item) -> bool:
        async def findx_async(
            items: List[Dict[str, Union[str, bool, int]]], timeout: int
        ) -> int:
            for _ in range(int(timeout / 1000 / (len(items)))):
                for i in range(0, len(items)):
                    if items[i]["exist"]:
                        if await self._find_async(
                            items[i]["selector"],
                            timeout=1000,
                            frame=self.page.frames[items[i]["frame"]],
                        ):
                            return i
                    else:
                        if not await self._find_async(
                            items[i]["selector"],
                            timeout=1000,
                            frame=self.page.frames[items[i]["frame"]],
                        ):
                            return i
            return -1

        await self._navigate_async(item.store_url, timeout=self.timeout)
        await self._try_click_async("div[data-component=PDPAgeGate] Button", sleep=8)
        await self._wait_for_text_change_async(
            "div[data-component=DesktopSticky] button[data-testid=purchase-cta-button]",
            "Loading",
        )
        if (
            await self._get_text_async(
                "div[data-component=DesktopSticky] button[data-testid=purchase-cta-button]"
            )
            == "In Library"
        ):
            return False
        await self._click_async(
            "div[data-component=DesktopSticky] button[data-testid=purchase-cta-button]:not([aria-disabled])",
            timeout=self.timeout,
        )
        await self._try_click_async(
            "div[data-component=makePlatformUnsupportedWarningStep] button[data-component=BaseButton"
        )
        # await self._try_click_async("#agree")
        await self._try_click_async("div[role=dialog] button[aria-disabled=false]")
        purchase_url = "https://www.epicgames.com" + await self._get_property_async(
            "#webPurchaseContainer iframe", "src"
        )
        await self._navigate_async(purchase_url)
        await self._click_async(
            "#purchase-app button[class*=confirm]:not([disabled])", timeout=self.timeout
        )
        # await self._try_click_async("#purchaseAppContainer div.payment-overlay button.payment-btn--primary")
        result = await findx_async(
            [
                {
                    "selector": "#purchase-app div[class*=alert]",
                    "exist": True,
                    "frame": 0,
                },
                {
                    "selector": "#talon_frame_checkout_free_prod[style*=visible]",
                    "exist": True,
                    "frame": 0,
                },
                {"selector": "#purchase-app > div", "exist": False, "frame": 0},
            ],
            timeout=self.timeout,
        )
        if result == -1:
            raise TimeoutError("Timeout when claiming")
        elif result == 0:
            message = await self._get_text_async(
                "#purchase-app div[class*=alert]:not([disabled])"
            )
            raise PermissionError(message)
        elif result == 1:
            raise PermissionError(
                "CAPTCHA is required for unknown reasons when claiming"
            )
        else:
            await self._navigate_async(item.store_url, timeout=self.timeout)
            await self._wait_for_text_change_async(
                "div[data-component=DesktopSticky] button[data-testid=purchase-cta-button]",
                "Loading",
            )
            if (
                not await self._get_text_async(
                    "div[data-component=DesktopSticky] button[data-testid=purchase-cta-button]"
                )
                == "In Library"
            ):
                raise RuntimeError(
                    "An item was mistakenly considered to have been claimed"
                )
            return True

    async def _screenshot_async(self, path: str) -> None:
        await self.page.screenshot({"path": path})

    def add_quit_signal(self):
        signal.signal(signal.SIGINT, self._quit)
        signal.signal(signal.SIGTERM, self._quit)
        if "SIGBREAK" in dir(signal):
            signal.signal(signal.SIGBREAK, self._quit)
        if "SIGHUP" in dir(signal):
            signal.signal(signal.SIGHUP, self._quit)

    # Broken
    async def _is_owned_async(self, offer_id: str, namespace: str) -> bool:
        args = {
            "query": "query launcherQuery($namespace: String!, $offerId: String!){Launcher{entitledOfferItems(namespace: $namespace, offerId: $offerId){entitledToAllItemsInOffer}}}",
            "variables": '{{"namespace": "{}", "offerId": "{}"}}'.format(
                namespace, offer_id
            ),
        }
        response = await self._get_json_async("https://www.epicgames.com/graphql", args)
        try:
            owned = response["data"]["Launcher"]["entitledOfferItems"][
                "entitledToAllItemsInOffer"
            ]
        except:
            raise ValueError("The returned data seems to be incorrect.")
        return owned

    async def _get_user_country_async(self) -> None:
        response = await self._get_json_async(
            "https://www.epicgames.com/account/v2/personal/ajaxGet"
        )
        try:
            country = response["userInfo"]["country"]["value"]
        except:
            raise ValueError("The returned data seems to be incorrect.")
        return country

    async def _try_get_webpage_content_async(self) -> Optional[str]:
        try:
            if self.browser_opened:
                webpage_content = await self._get_text_async("body")
                return webpage_content
        except:
            pass

    def _async_auto_retry(
        self,
        retries: int,
        error_message: str,
        error_notification: str,
        raise_error: bool = True,
    ) -> None:
        def retry(func: Callable) -> Callable:
            async def wrapper(*arg, **kw):
                for i in range(retries):
                    try:
                        await func(*arg, **kw)
                        break
                    except Exception as e:
                        if i < retries - 1:
                            self.log(f"{e}", level="warning")
                        else:
                            self.log(f"{error_message}{e}", "error")
                            self.claimer_notifications.notify(
                                local_texts.NOTIFICATION_TITLE_ERROR,
                                f"{error_notification}{e}",
                            )
                            await self._screenshot_async("screenshot.png")
                            if raise_error:
                                raise e

            return wrapper

        return retry

    async def _run_once_async(
        self,
        interactive: bool = True,
        email: str = None,
        password: str = None,
        verification_code: str = None,
        retries: int = 3,
        raise_error: bool = False,
    ) -> List[str]:
        @self._async_auto_retry(
            retries,
            "Failed to open the browser: ",
            local_texts.NOTIFICATION_CONTENT_OPEN_BROWSER_FAILED,
        )
        async def run_open_browser():
            if not self.browser_opened:
                await self._open_browser_async()

        @self._async_auto_retry(
            retries, "Failed to login: ", local_texts.NOTIFICATION_CONTENT_LOGIN_FAILED
        )
        async def run_login(
            interactive: bool,
            email: Optional[str],
            password: Optional[str],
            verification_code: str = None,
        ):
            if await self._need_login_async():
                if interactive:
                    self.log("Need login")
                    self.claimer_notifications.notify(
                        local_texts.NOTIFICATION_TITLE_NEED_LOGIN,
                        local_texts.NOTIFICATION_CONTENT_NEED_LOGIN,
                    )
                    await self._close_browser_async()
                    email = input("Email: ")
                    password = getpass("Password: ")
                    await self._open_browser_async()
                    await self._login_async(email, password)
                    self.log("Login successful")
                else:
                    await self._login_async(
                        email, password, verification_code, interactive=False
                    )

        async def run_claim() -> List[str]:
            claimed_item_titles = []
            owned_item_titles = []

            @self._async_auto_retry(
                retries,
                "Failed to claim one item: ",
                local_texts.NOTIFICATION_CONTENT_CLAIM_FAILED,
                raise_error=False,
            )
            async def retried_claim(item: Item) -> bool:
                if await self._claim_async(item):
                    claimed_item_titles.append(item.title)
                    self.log(f"Successfully claimed: {item.title}")
                else:
                    owned_item_titles.append(item.title)

            free_items = await self._get_weekly_free_items_async()
            item_amount = len(free_items)
            for item in free_items:
                await retried_claim(item)
            if len(owned_item_titles) == item_amount:
                self.log("All available free games are already in your library")
                if self.push_when_owned_all:
                    self.claimer_notifications.notify(
                        local_texts.NOTIFICATION_TITLE_CLAIM_SUCCEED,
                        local_texts.NOTIFICATION_CONTENT_OWNED_ALL,
                    )
            if len(claimed_item_titles) != 0:
                claimed_item_titles_string = ""
                for title in claimed_item_titles:
                    claimed_item_titles_string += f"{title}, "
                claimed_item_titles_string = claimed_item_titles_string.rstrip(", ")
                self.claimer_notifications.notify(
                    local_texts.NOTIFICATION_TITLE_CLAIM_SUCCEED,
                    f"{local_texts.NOTIFICATION_CONTENT_CLAIM_SUCCEED}{claimed_item_titles_string}",
                )
            if len(claimed_item_titles) + len(owned_item_titles) < item_amount:
                raise PermissionError("Failed to claim some items")
            return claimed_item_titles

        claimed_item_titles = []
        if raise_error:
            await run_open_browser()
            await run_login(interactive, email, password, verification_code)
            claimed_item_titles = await run_claim()
        else:
            try:
                await run_open_browser()
                await run_login(interactive, email, password, verification_code)
                claimed_item_titles = await run_claim()
            except:
                pass
        try:
            await self._close_browser_async()
        except:
            pass
        return claimed_item_titles

    async def _load_cookies_async(self, path: str) -> None:
        with open(path, "r") as cookies_file:
            cookies = cookies_file.read()
            for cookie in json.loads(cookies):
                await self.page.setCookie(cookie)

    async def _save_cookies_async(self, path: str) -> None:
        dir = os.path.dirname(path)
        if not dir == "" and not os.path.exists(dir):
            os.mkdir(dir)
        with open(path, "w") as cookies_file:
            await self.page.cookies()
            cookies = await self.page.cookies()
            cookies_file.write(json.dumps(cookies, separators=(",", ": "), indent=4))

    def open_browser(self) -> None:
        return self._loop.run_until_complete(self._open_browser_async())

    def close_browser(self) -> None:
        return self._loop.run_until_complete(self._close_browser_async())

    def need_login(self) -> bool:
        return self._loop.run_until_complete(self._need_login_async())

    def login(
        self,
        email: str,
        password: str,
        verifacation_code: str = None,
        interactive: bool = True,
        remember_me: bool = True,
    ) -> None:
        return self._loop.run_until_complete(
            self._login_async(
                email, password, verifacation_code, interactive, remember_me
            )
        )

    def get_weekly_free_games(self) -> List[Game]:
        return self._loop.run_until_complete(self._get_weekly_free_games_async())

    def run_once(
        self,
        interactive: bool = True,
        email: str = None,
        password: str = None,
        verification_code: str = None,
        retries: int = 3,
        raise_error: bool = False,
    ) -> List[str]:
        return self._loop.run_until_complete(
            self._run_once_async(
                interactive, email, password, verification_code, retries, raise_error
            )
        )

    def scheduled_run(
        self,
        at: str,
        interactive: bool = True,
        email: str = None,
        password: str = None,
        verification_code: str = None,
        retries: int = 3,
    ) -> None:
        self.add_quit_signal()
        schedule.every().day.at(at).do(
            self.run_once, interactive, email, password, verification_code, retries
        )
        while True:
            schedule.run_pending()
            time.sleep(1)

    def load_cookies(self, path: str) -> None:
        return self._loop.run_until_complete(self._load_cookies_async(path))

    def save_cookies(self, path: str) -> None:
        return self._loop.run_until_complete(self._save_cookies_async(path))

    def navigate(self, url: str, timeout: int = 30000, reload: bool = True) -> None:
        return self._loop.run_until_complete(self._navigate_async(url, timeout, reload))

    def find(self, selector: str, timeout: int = None, frame: Frame = None) -> bool:
        return self._loop.run_until_complete(self._find_async(selector, timeout, frame))

    def virtual_console(self) -> None:
        print(
            "You can input JavaScript commands here for testing. Type exit and press Enter to quit."
        )
        while True:
            try:
                command = input("> ")
            except EOFError:
                break
            if command == "exit":
                break
            try:
                result = self._loop.run_until_complete(self.page.evaluate(command))
                print(result)
            except Exception as e:
                print(f"{e}")


def login(cookies_path: str) -> None:
    claimer = EpicgamesClaimer(
        headless=False,
        sandbox=True,
        browser_args=["--disable-infobars", "--no-first-run"],
    )
    claimer.log("Creating user data, please log in in the browser ...")
    claimer.navigate(
        "https://www.epicgames.com/id/login?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fstore",
        timeout=0,
    )
    claimer.find("#user[data-component=SignedIn]", timeout=0)
    claimer.save_cookies(cookies_path)
    claimer.log("Login successful")
    claimer.close_browser()


def get_args(run_by_main_script: bool = False) -> argparse.Namespace:
    def update_args_from_env(args: argparse.Namespace) -> argparse.Namespace:
        for key in args.__dict__.keys():
            env = os.environ.get(key.upper())
            if env != None:
                if type(args.__dict__[key]) == int:
                    args.__setattr__(key, int(env))
                elif type(args.__dict__[key]) == bool:
                    if env == "true":
                        args.__setattr__(key, True)
                    elif env == "false":
                        args.__setattr__(key, False)
                else:
                    args.__setattr__(key, env)
        return args

    parser = argparse.ArgumentParser(
        description="Claim weekly free games from Epic Games Store."
    )
    parser.add_argument(
        "-n", "--no-headless", action="store_true", help="run the browser with GUI"
    )
    parser.add_argument(
        "-c", "--chromium-path", type=str, help="set path to browser executable"
    )
    parser.add_argument(
        "-r",
        "--run-at",
        type=str,
        help="set daily check and claim time, format to HH:MM, default to the current time",
    )
    parser.add_argument(
        "-o", "--once", action="store_true", help="claim once then exit"
    )
    if run_by_main_script:
        parser.add_argument(
            "-a", "--auto-update", action="store_true", help="enable auto update"
        )
        parser.add_argument("--cron", type=str, help="set cron expression")
    if not run_by_main_script:
        parser.add_argument(
            "-e",
            "--external-schedule",
            action="store_true",
            help="run in external schedule mode",
        )
    parser.add_argument(
        "-u", "--email", "--username", type=str, help="set username/email"
    )
    parser.add_argument("-p", "--password", type=str, help="set password")
    parser.add_argument(
        "-t", "--verification-code", type=str, help="set verification code (2FA)"
    )
    parser.add_argument("--cookies", type=str, help="set path to cookies file")
    parser.add_argument(
        "-l", "--login", action="store_true", help="create logged-in user data and quit"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug mode")
    parser.add_argument(
        "-dt",
        "--debug-timeout",
        type=int,
        default=180000,
        help="set timeout in milliseconds",
    )
    parser.add_argument(
        "-dr", "--debug-retries", type=int, default=3, help="set the number of retries"
    )
    parser.add_argument(
        "-dp",
        "--debug-push-test",
        action="store_true",
        help="Push a notification for testing and quit",
    )
    parser.add_argument(
        "-ds",
        "--debug-show-args",
        action="store_true",
        help="Push a notification for testing and quit",
    )
    parser.add_argument(
        "--push-lang", type=str, default="zh", help="set notifications language"
    )
    parser.add_argument(
        "-ps", "--push-serverchan-sendkey", type=str, help="set ServerChan sendkey"
    )
    parser.add_argument(
        "-pbu",
        "--push-bark-url",
        type=str,
        default="https://api.day.app/push",
        help="set Bark server address",
    )
    parser.add_argument(
        "-pbk", "--push-bark-device-key", type=str, help="set Bark device key"
    )
    parser.add_argument(
        "-ptt", "--push-telegram-bot-token", type=str, help="set Telegram bot token"
    )
    parser.add_argument(
        "-pti", "--push-telegram-chat-id", type=str, help="set Telegram chat ID"
    )
    parser.add_argument(
        "-pwx", "--push-wechat-qywx-am", type=str, help="set WeChat QYWX"
    )
    parser.add_argument(
        "-pda",
        "--push-dingtalk-access-token",
        type=str,
        help="set DingTalk access token",
    )
    parser.add_argument(
        "-pds", "--push-dingtalk-secret", type=str, help="set DingTalk secret"
    )
    parser.add_argument(
        "-ns",
        "--no-startup-notification",
        action="store_true",
        help="disable pushing a notification at startup",
    )
    parser.add_argument(
        "--push-when-owned-all",
        action="store_true",
        help="push a notification when all available weekly free games are already in the library",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="print version information and quit",
    )
    args = parser.parse_args()
    args = update_args_from_env(args)
    global local_texts
    if args.push_lang:
        local_texts = eval("texts." + args.push_lang)
    localtime = time.localtime()
    if run_by_main_script:
        if args.cron is None:
            if args.run_at == None:
                args.cron = "{0:02d} {1:02d} * * *".format(
                    localtime.tm_min, localtime.tm_hour
                )
            else:
                hour, minute = args.run_at.split(":")
                args.cron = "{0} {1} * * *".format(minute, hour)
    if args.run_at == None:
        args.run_at = "{0:02d}:{1:02d}".format(localtime.tm_hour, localtime.tm_min)
    if args.email != None and args.password == None:
        raise ValueError("Must input both username and password.")
    if args.email == None and args.password != None:
        raise ValueError("Must input both username and password.")
    args.interactive = True if args.email == None else False
    args.data_dir = (
        "User_Data/Default" if args.interactive else "User_Data/{}".format(args.email)
    )
    if args.debug_push_test:
        test_notifications = Notifications(
            serverchan_sendkey=args.push_serverchan_sendkey,
            bark_push_url=args.push_bark_url,
            bark_device_key=args.push_bark_device_key,
            telegram_bot_token=args.push_telegram_bot_token,
            telegram_chat_id=args.push_telegram_chat_id,
        )
        test_notifications.notify(
            local_texts.NOTIFICATION_TITLE_TEST, local_texts.NOTIFICATION_CONTENT_TEST
        )
        exit()
    if args.debug_show_args:
        print(args)
        exit()
    if args.login:
        login("User_Data/Default/cookies.json")
        exit()
    return args


def main(
    args: argparse.Namespace = None, raise_error: bool = False
) -> Optional[List[str]]:
    if args == None:
        args = get_args()
    claimer_notifications = Notifications(
        serverchan_sendkey=args.push_serverchan_sendkey,
        bark_push_url=args.push_bark_url,
        bark_device_key=args.push_bark_device_key,
        telegram_bot_token=args.push_telegram_bot_token,
        telegram_chat_id=args.push_telegram_chat_id,
        wechat_qywx_am=args.push_wechat_qywx_am,
        dingtalk_access_token=args.push_dingtalk_access_token,
        dingtalk_secret=args.push_dingtalk_secret,
    )
    claimer = EpicgamesClaimer(
        data_dir=args.data_dir,
        headless=not args.no_headless,
        chromium_path=args.chromium_path,
        claimer_notifications=claimer_notifications,
        timeout=args.debug_timeout,
        debug=args.debug,
        cookies=args.cookies,
        push_when_owned_all=args.push_when_owned_all,
    )
    if args.once:
        return claimer.run_once(
            args.interactive,
            args.email,
            args.password,
            args.verification_code,
            retries=args.debug_retries,
            raise_error=raise_error,
        )
    elif args.external_schedule:
        if not args.no_startup_notification:
            claimer_notifications.notify(
                local_texts.NOTIFICATION_TITLE_START,
                local_texts.NOTIFICATION_CONTENT_START,
            )
        claimer.run_once(
            args.interactive,
            args.email,
            args.password,
            args.verification_code,
            retries=args.debug_retries,
            raise_error=raise_error,
        )
    else:
        if not args.no_startup_notification:
            claimer_notifications.notify(
                local_texts.NOTIFICATION_TITLE_START,
                local_texts.NOTIFICATION_CONTENT_START,
            )
        claimer.run_once(
            args.interactive,
            args.email,
            args.password,
            args.verification_code,
            retries=args.debug_retries,
        )
        claimer.scheduled_run(
            args.run_at,
            args.interactive,
            args.email,
            args.password,
            args.verification_code,
        )


# Entry function of SCF
def main_handler(event: Dict[str, str] = None, context: Dict[str, str] = None) -> str:
    cwd = os.getcwd()
    sys.path.append(cwd)
    os.chdir("/tmp")
    args = get_args()
    args.chromium_path = cwd + "/chrome-linux/chrome"
    args.once = True
    claimed_item_titles = main(args, raise_error=True)
    result_message = (
        f"{local_texts.NOTIFICATION_CONTENT_CLAIM_SUCCEED}{claimed_item_titles}"
        if len(claimed_item_titles)
        else local_texts.NOTIFICATION_CONTENT_OWNED_ALL
    )
    return result_message


def run(args: argparse.Namespace, check_items: dict) -> str or None:
    args.chromium_path = "chromium-browser"
    args.interactive = False
    args.once = True

    msg_all = ""
    for check_item in check_items:
        args.email = check_item.get("email")
        args.password = check_item.get("password")
        args.data_dir = "User_Data/{}".format(args.email)
        if not os.path.exists("User_Data"):
            log(
                f"未发现 User_Data 文件夹，判断为初次使用。若遇到人机验证，请在能手动登录浏览器页面的环境（如 Win10）使用 get_cookies.exe/py 获取 cookies.json 并放入 {os.path.join(os.getcwd(), args.data_dir)} 文件夹，然后再尝试",
                level="warning",
            )
        else:
            args.cookies = (
                c
                if os.path.exists(c := os.path.join(args.data_dir, "cookies.json"))
                else None
            )
        claimed_item_titles = main(args, raise_error=True)
        msg = (
            f"{local_texts.NOTIFICATION_CONTENT_CLAIM_SUCCEED}{claimed_item_titles}"
            if len(claimed_item_titles)
            else local_texts.NOTIFICATION_CONTENT_OWNED_ALL
        )
        msg_all += msg + "\n\n"
    return msg_all


def start() -> None:
    args = get_args()
    if args.email and args.password:
        main()
        return
    ENV = get_env_str()
    if ENV == "v2p":
        os.chdir("/usr/local/app/script/Lists")
    elif ENV == "ql":
        os.chdir("/ql/config")
    else:
        main()
        return
    data = get_data()
    _check_items = data.get("EPIC", [])
    res = run(args, check_items=_check_items)
    send("Epicgames", res)


if __name__ == "__main__":
    start()
