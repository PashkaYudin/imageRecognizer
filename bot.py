import requests
from time import sleep
import io
import pytesseract
from PIL import Image

token = ""
url = "https://api.telegram.org/bot" + token + "/"


def get_updates_json(request):
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    print results[total_updates]
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def get_message_text(update):
    user_text = update['message']['text']
    return user_text

def get_message_photo(update):
    path = update['message']['photo'][2]['file_id']
    # path = update[count(update) - 1]['file_id'];
    link = requests.get(url + 'getFile?file_id='+path)
    link = link.json()
    link = link['result']['file_path']
    return recognize("https://api.telegram.org/file/bot"+ token + "/" + link)

def recognize(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    text = pytesseract.image_to_string(img)
    print(text)
    return text


def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def main():
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
           send_mess(get_chat_id(last_update(get_updates_json(url))), get_message_photo(last_update(get_updates_json(url))))
           update_id += 1
        sleep(1)

if __name__ == '__main__':
    main()
