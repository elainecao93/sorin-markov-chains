import requests
from hashlib import sha1
import time
import hmac
import base64
import urllib
import random
import string

def makeSig(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL):

    f = open("solution.txt", "r")
    raw = f.read()
    solution = raw.split("\n")

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
    #print(solution[0])
    #print(param_string == solution[0])

    base_string = "POST&" + urllib.parse.quote(URL).replace("/", "%2F") + "&" + urllib.parse.quote(param_string)
    print(base_string)
    #print(solution[1])
    #print(base_string == solution[1])
    secret_keys = consumer_secret + "&" + token_secret
    print(secret_keys)
    #print(solution[2])
    #print(secret_keys == solution[2])

    key = bytes(secret_keys, "UTF-8")
    message = bytes(base_string, "UTF-8")

    encode = hmac.new(key, message, sha1)
    signature = base64.b64encode(encode.digest()).decode()

    print(signature)

    return signature
    #print(solution[3])

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

def postToTwitter():

    f = open("key.txt", "r")
    raw = f.read()
    key = raw.split("\n")

    consumer_key = key[0]
    oauth_token = key[2]
    consumer_secret = key[1]
    token_secret = key[3]
    timestamp = str(int(time.time()))
    nonce = "".join(random.choice(string.ascii_lowercase) for i in range(20))
    URL = "https://api.twitter.com/1.1/statuses/update.json?include_entities=true"
    message = "Testing API"

    print(message)

    auth = makeAuth(consumer_key, oauth_token, consumer_secret, token_secret, message, timestamp, nonce, URL)

    headers = {"Authorization":auth}
    data = {"status":message}

    r = requests.post(url = URL, data = data, headers = headers)
    print(r.request.headers)
    print(r.text)


def main():
    #these are the test cases provided by twitter, not real tokens. Real tokens are stored in a gitignore'd file.
    """consumer_key = "xvz1evFS4wEEPTGEFPHBog"
    oauth_token = "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb"
    consumer_secret = "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw"
    token_secret = "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
    timestamp = "1318622958"
    nonce = "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg"
    URL = "https://api.twitter.com/1.1/statuses/update.json"
    message = "Hello Ladies + Gentlemen, a signed OAuth request!"
    """
    """consumer_key = "xvz1evFS4wEEPTGEFPHBog"
    nonce = "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg"
    timestamp = "1318622958"
    oauth_token = "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb"
    gen = makeAuth(consumer_key, oauth_token, "asdfghjkl", "asdfghjkl", "message", timestamp, nonce, "https://api.twitter.com/1.1/statuses/update.json")
    f = open("solution.txt")
    solution = f.read().split("\n")[4]
    print(solution)
    print(gen == solution)"""
    postToTwitter()


if __name__ =="__main__":
    main()