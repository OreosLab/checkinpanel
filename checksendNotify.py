import requests
import os


def message2telegram(tg_api_host, tg_proxy, tg_bot_token, tg_user_id, content):
    print("Telegram 推送开始")
    send_data = {"chat_id": tg_user_id, "text": content, "disable_web_page_preview": "true"}
    if tg_api_host:
        url = f"https://{tg_api_host}/bot{tg_bot_token}/sendMessage"
    else:
        url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    if tg_proxy:
        proxies = {
            "http": tg_proxy,
            "https": tg_proxy,
        }
    else:
        proxies = None
    try :
        requests.post(url=url, data=send_data, proxies=proxies)
        print("推送成功")
        return 1
    except:
        print("推送失败")
        return 0


def send(content):
    tg_api_host = os.environ.get('TG_API_HOST')
    tg_proxy = ''
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    tg_user_id = os.environ.get('TG_USER_ID')
    message2telegram(tg_api_host=tg_api_host, tg_proxy=tg_proxy, tg_bot_token=tg_bot_token, tg_user_id=tg_user_id,
                     content=content)