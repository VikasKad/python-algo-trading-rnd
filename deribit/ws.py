#!/usr/bin/python
import time
import base64
import hashlib
import hmac
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import websocket
import json
import secrets
from datetime import datetime


# IMPORTANT: www.deribit.com and test.deribit.com do not share credentials
# if to use testnet - separate registartion on test.deribit.com is needed

api_key = 'KXMzYANK'
api_secret = 'pwGwsMp5Ftp9g1C7-qMUj1KR6ME8R_fkYuHRhDEdQwE'
tstamp = datetime.now().strftime('%s') + "000"
data = ''
nonce = secrets.token_urlsafe(10)

base_signature_string = tstamp + "\n" + nonce + "\n" + data

byte_key = api_secret.encode()
message = base_signature_string.encode()
signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

print(signature)

def main():
    
    def on_message(ws, message):
        print("recieved:")
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        ws_data = {
            "jsonrpc" : "2.0",
            "id" : 1, 
            "method" : "public/auth",
            "params" : {
                "grant_type" : "client_signature",
                "client_id" : api_key,
                "timestamp": tstamp,
                "nonce": nonce,
                "signature" : signature,
                "data" : data}
        }
        str = json.dumps(ws_data)
        print(str)
        ws.send(str)
        
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://test.deribit.com/ws/api/v2/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    
    ws.run_forever()


if __name__ == "__main__":
    main()


