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
