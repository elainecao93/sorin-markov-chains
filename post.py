import requests
from hashlib import sha1
import time
import hmac
import base64
import urllib
import random
import string
import markov

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

    f = open("key.txt", "r")
    key = f.read().split("\n")

    consumer_key = key[0]
    oauth_token = key[2]
    consumer_secret = key[1]
    token_secret = key[3]
    timestamp = str(int(time.time()))
    nonce = "".join(random.choice(string.ascii_lowercase) for i in range(20))
    URL = "https://api.twitter.com/1.1/statuses/update.json"
    
    message = str(chain)
    """while len(messagestr) > 280:
        message = markov.Chain()
        messagestr = str(message)"""

    print(message)

    auth = makeAuth(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL)

    URL = URL + "?include_entities=true"

    headers = {"Authorization":auth}
    data = {"status":message}

    r = requests.post(url = URL, data = data, headers = headers)
    print(r.request.headers)
    print(r.text)
    print(chain.trace())
    retval = r.json()

    log = open("output.log", "a")
    log.write(retval["created_at"] + " " + nonce + "\n")
    log.write(chain.trace() + "\n")

if __name__ =="__main__":
    chain = markov.markov()
    postToTwitter(chain)