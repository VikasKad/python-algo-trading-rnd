import websocket
import threading
from time import sleep
import hmac
import hashlib
import json
import datetime
import time
from delta.delta_rest_client import DeltaRestClient
from delta.delta_rest_client import OrderType
import csv
import requests
import urllib
api_key = '9a3e387a748f7fb76914f7a39411d3'
api_secret = '46dfd256153ba502178b789fd3e223789ace0a3cbba3bdbac548a1671359'
delta_client = DeltaRestClient(
    base_url='https://testnet-api.delta.exchange',
    api_key=api_key,
    api_secret=api_secret)


def get_time_stamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970, 1, 1)
    return str(int((d - epoch).total_seconds()))


def generate_signature(secret, message):
    message = bytes(message, 'utf-8')
    secret = bytes(secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    return hash.hexdigest()


def __on_error(ws, error):
    print(str(error))


def __on_open(ws):
    print("Delta Websocket Opened.")


def __on_close(ws):
    print('Delta Websocket Closed.')


def __on_message(ws, message):
    try:
        message = json.loads(message)
        print(message)
        if message['size'] > 0:
            print('get open order')
            with open('orders.csv', 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                print(lines[0])
                order_id = lines[0][0]
                order_price = lines[0][1]
                order_side = lines[0][2]
                # place new stop loss order
                print('order details:\t', order_id, order_price, order_side)
                # it will be stop order
                order_response = delta_client.place_stop_order(
                    product_id=16, size=10, side=order_side, order_type=OrderType.MARKET, stop_price=order_price)
                print('stop loss order:\t', order_response['id'])
            # cancel all orders
            file.close()
        else:
            print('size is 0')

    except (requests.exceptions.HTTPError, urllib.error.HTTPError) as e:
        error_msg = e.response.text
        print("Error while placing order: %s" % (error_msg))


def connect(api_key, api_secret):
    ws = websocket.WebSocketApp('wss://testnet-api.delta.exchange:2096',
                                on_message=__on_message,
                                on_close=__on_close,
                                on_open=__on_open,
                                on_error=__on_error)
    wst = threading.Thread(name='Delta Websocket',
                           target=lambda: ws.run_forever(ping_interval=30, ping_timeout=10))
    wst.daemon = True
    wst.start()

    conn_timeout = 5
    while not ws.sock or not ws.sock.connected and conn_timeout:
        sleep(1)
        conn_timeout -= 1

    method = 'GET'
    timestamp = get_time_stamp()
    path = '/live'
    signature_data = method + timestamp + path
    signature = generate_signature(api_secret, signature_data)
    ws.send(json.dumps({
        "type": "auth",
        "payload": {
            "api-key": api_key,
            "signature": signature,
            "timestamp": timestamp
        }
    }))
    sleep(1)
    ws.send(json.dumps({
        "type": "subscribe",
        "payload": {
            "channels": [
                {
                    "name": "positions",
                    "symbols": ["BTCUSD"]
                }
            ]
        }
    }))
    return ws


ws = connect(
    '9a3e387a748f7fb76914f7a39411d3',         # Api key
    '46dfd256153ba502178b789fd3e223789ace0a3cbba3bdbac548a1671359'          # Api Secret
)

while True:
    sleep(1)
    print("Connected: %s" % (ws.sock and ws.sock.connected))
