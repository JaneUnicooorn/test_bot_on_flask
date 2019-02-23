from flask import Flask
from flask_sslify import SSLify
from flask import request
from flask import jsonify
import requests
import json
import re

TOKEN = '704001319:AAHwbOYzZoHaRCN73XGEEhAF2aN_wAb61Pw'
URL = f'https://api.telegram.org/bot{TOKEN}/'

app = Flask(__name__)
sslify = SSLify(app)

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_text(text):
    pattern = r'/\w+'

    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_price(crypto):
    url = f'https://api.coinmarketcap.com/v1/ticker/{crypto}'
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    #write_json(r.json(), filename='price.json')
    return price
'''def get_updates():
    r = requests.get(URL+'getUpdates')
    #write_json(r.json())
    return r.json()'''

def send_message(chat_id, text = 'bla bla bla'):
    answer = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(URL+'sendMessage', json=answer)

    return r.json()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, text=price)
        #write_json(r)
        return jsonify(r)

    return 'Text)))'



if __name__ == '__main__':
    app.run()

#https://api.telegram.org/bot704001319:AAHwbOYzZoHaRCN73XGEEhAF2aN_wAb61Pw/setWebhook?url=https://unicorn1.pythonanywhere.com/