import json
import requests
import time
import urllib

import config

starttime = -1
endtime = -1

TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_response(text):
    return text.upper() + "!";

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    while True:
        try:
            content = get_url(url)
            break
        except:
            print("having troubles with connection")
            time.sleep(5)

    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        print(update)
        if "message" in update:
             text = update["message"]["text"]
             chat = update["message"]["chat"]["id"]
             send_message(get_response(text), chat)
        elif "channel_post" in update:
             text = update["channel_post"]["text"]
             chat = update["channel_post"]["chat"]["id"]
             if update["channel_post"]["chat"]["username"] == "worktimebotchat":
                 global starttime,endtime
                 if text == "start":
                     if(starttime == -1):
                         starttime = time.time()
                 if text == "end":
                     if(endtime == -1):
                         endtime = time.time()
                         timesecs = endtime - starttime
                         timemins = timesecs/60
                         min = timemins%60
                         hour = (timemins - min)/60
                         msg = "Worktime "+str(round(hour))+"h "+str(round(min))+"min"
                         send_message(msg,chat)
                         endtime = -1
                         starttime = -1
             else:
                 send_message(get_response(text), chat)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    print("starting")
    print(starttime)
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
