from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from hashlib import sha1
import time
import hmac
import base64
import urllib
import random
import string
import markov
import os
from init import Log

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

def makeSig(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL):

    auth_key = {"include_entities":"true", "oauth_consumer_key":consumer_key, "oauth_nonce":nonce, 
    "oauth_signature_method":"HMAC-SHA1", "oauth_timestamp":timestamp, "oauth_token":oauth_token, 
    "oauth_version":"1.0", "status":message}

    param_string = ""
    first = True
    for k in sorted(auth_key):
        if not first:
            param_string += "&"
        first = False
        param_string += urllib.parse.quote(k) + "=" + urllib.parse.quote(auth_key[k])
    print(param_string)

    base_string = "POST&" + urllib.parse.quote(URL).replace("/", "%2F") + "&" + urllib.parse.quote(param_string)
    print(base_string)
    secret_keys = consumer_secret + "&" + token_secret
    print(secret_keys)

    key = bytes(secret_keys, "UTF-8")
    message = bytes(base_string, "UTF-8")

    encode = hmac.new(key, message, sha1)
    signature = base64.b64encode(encode.digest()).decode()

    print(signature)

    return signature

def makeAuth(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL):
    signature = makeSig(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL)
    auth_dict = {"oauth_consumer_key":consumer_key, "oauth_nonce":nonce, "oauth_signature":signature,
    "oauth_signature_method":"HMAC-SHA1", "oauth_timestamp":timestamp, "oauth_token":oauth_token, 
    "oauth_version":"1.0"}
    auth_key = "OAuth "
    first = True
    for k in sorted(auth_dict):
        if not first:
            auth_key += ", "
        first = False
        auth_key += urllib.parse.quote(k) + "=\"" + urllib.parse.quote(auth_dict[k]).replace("/", "%2F") + "\""
    print(auth_key)
    return auth_key

def postToTwitter(chain):

    consumer_key = os.environ.get("CONSUMER_API_KEY")
    oauth_token = os.environ.get("ACCESS_TOKEN")
    consumer_secret = os.environ.get("CONSUMER_API_SECRET_KEY")
    token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    timestamp = str(int(time.time()))
    nonce = "".join(random.choice(string.ascii_lowercase) for i in range(20))
    URL = "https://api.twitter.com/1.1/statuses/update.json"
    
    message = str(chain)

    print(message)

    auth = makeAuth(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL)

    URL = URL + "?include_entities=true"

    headers = {"Authorization":auth}
    data = {"status":message}

    r = requests.post(url = URL, data = data, headers = headers)
    print(r.request.headers)
    print(r.text)
    print(chain.fullTrace())

    response = r.json()

    log = Log(nonce, response["created_at"], chain.makeIntoLog())
    db.session.add(log)
    db.session.commit()

def postFromWeb():
    chain = markov.markov(True)
    postToTwitter(chain)
    return chain

def main():
    chain = markov.markov(True)
    postToTwitter(chain)

if __name__ =="__main__":
    main()