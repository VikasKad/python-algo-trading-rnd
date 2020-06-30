
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

import binascii
import random
import requests

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def create_sha256_signature(ClientSecret, StringToSign):
    signature_computed = hmac.new(
        key=ClientSecret.encode('utf-8'),
        msg=StringToSign.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return signature_computed


ClientId = "KXMzYANK"
ClientSecret = "pwGwsMp5Ftp9g1C7-qMUj1KR6ME8R_fkYuHRhDEdQwE"
timestamp = str(int(time.time() * 1000))
nonce = generate_nonce(length=10)
endpoint = "/api/v2/private/get_account_summary?currency=BTC"
HTTP_METHOD = "GET"

RequestData = HTTP_METHOD + "\n" + endpoint + "\n" + ""
StringToSign = timestamp + "\n" + nonce + "\n" + RequestData.upper()

signature = create_sha256_signature(ClientSecret, StringToSign)
headers = {"Authorization": "deri-hmac-sha256 id="+ClientId +
           ",ts="+timestamp+",sig="+signature+",nounce="+nonce+""}
print("Headers:" + str(headers))
print("\n")
r = requests.get(
    "https://test.deribit.com/api/v2/private/get_account_summary?currency=BTC", headers=headers)
print("Response:" + str(r.json()))


# IMPORTANT: www.deribit.com and test.deribit.com do not share credentials
# if to use testnet - separate registartion on test.deribit.com is needed

# api_key = "KXMzYANK"
# api_secret = "pwGwsMp5Ftp9g1C7-qMUj1KR6ME8R_fkYuHRhDEdQwE"
# tstamp = datetime.now().strftime('%s') + "000"
# data = ''
# nonce = secrets.token_urlsafe(10)
# print(nonce)
# base_signature_string = tstamp + "\n" + nonce + "\n" + data

# byte_key = api_secret.encode()
# message = base_signature_string.encode()
# signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

# print(signature)
