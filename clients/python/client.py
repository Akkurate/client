import hashlib
import hmac
import json
import secrets
from os import getenv
from time import time
from urllib.parse import urlunparse

try:
    import requests
except:
    print("please do 'pip i -r requirements.txt")
    exit(1)


def getHmac() -> dict:
    Nonce = generateNonce()
    Signature = generateSignature(Nonce)
    PublicKey = getenv("DIAGNOSE_PUBLIC_KEY", "")
    if PublicKey == "" or Signature == "":
        raise Exception("Public or secret key missing")
    return {"PublicKey": PublicKey, "Nonce": Nonce, "Signature": Signature}


def generateNonce():
    hx = secrets.token_bytes(32)
    return str(int(time())) + hx.hex()


def generateSignature(Nonce):
    SecretKey = getenv("DIAGNOSE_SECRET_KEY")
    if not SecretKey:
        return ""
    encodedNonce = Nonce.encode()
    byte_key = bytes(SecretKey, 'UTF-8')
    Signature = hmac.new(byte_key, None, hashlib.sha512)
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
            return data['response']
        else:
            raise Exception(f"request failed \r\n Status: {r.status_code} \r\n {r.content.decode('utf-8')}")
    except Exception as ex:
        raise(ex)
