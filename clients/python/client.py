import hashlib
import hmac
import json
from math import floor
from os import getenv
from random import random
from time import time
from urllib.parse import urlunparse

try:
    import requests
except:
    print("please do 'pip install -r requirements.txt")
    exit(1)


def getHmac() -> dict:
    rand = generateRand(70)
    nonce = int(time()*1000)  # server requires microseconds
    PublicKey = getenv("DIAGNOSE_PUBLIC_KEY", "")
    forSigning = PublicKey + str(nonce) + rand
    Signature = generateSignature(forSigning)

    if PublicKey == "" or Signature == "":
        raise Exception("Public or secret key missing")
    return {"PublicKey": PublicKey, "Nonce": str(nonce), "Rand": rand, "Signature": Signature}


def generateRand(length: int) -> str:
    text = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()_+-=[]{}|',./<>?"
    for _ in range(0, length):
        text += possible[floor(random()*length)]
    print(len(text))
    return text


def generateSignature(Nonce):
    SecretKey = getenv("DIAGNOSE_SECRET_KEY")
    if not SecretKey:
        return ""
    encodedNonce = Nonce.encode()
    byte_key = bytes(SecretKey, 'UTF-8')
    Signature = hmac.new(byte_key, None, hashlib.sha256)
    Signature.update(encodedNonce)
    strSignature = Signature.hexdigest()
    return strSignature


def diagnose(opts):

    protocol = "https"
    hostname = "publicapi.diagnose.fi"
    url = urlunparse((protocol, hostname, opts["path"], None, opts["query"], None))

    try:
        r = requests.get(url, headers=getHmac())
        if(r.status_code == 200):
            data = json.loads(r.content)
            return data
        else:
            raise Exception(f"request failed \r\n Status: {r.status_code} \r\n {r.content.decode('utf-8')}")
    except Exception as ex:
        raise(ex)
