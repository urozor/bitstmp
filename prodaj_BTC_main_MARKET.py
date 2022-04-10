# Skripta odda MARKET SELL ORDER za BTC
import urllib, urllib2, json 
import hmac
import hashlib
import time


price=19900


customer_id="123"
API_SECRET="123"
nonce = str(int(time.time()))
api_key = "123"


message = nonce + customer_id + api_key
signature = hmac.new(
    API_SECRET,
    msg=message,
    digestmod=hashlib.sha256
).hexdigest().upper()


#url = "https://www.bitstamp.net/api/v2/balance?key=" + api_key + "&signature=" + signature + "&nonce=" + nonce

url = "https://www.bitstamp.net/api/v2/balance/"
data = {'key':api_key,'nonce':nonce,'signature':signature}
print (data)
request = urllib2.Request(url,urllib.urlencode(data))
response = urllib2.urlopen(request)

d = response.read()
print(d)
data = json.loads(d)

btcjev=float(data['btc_available'])
evrov=float(data['eur_available'])
fee=float(data['btceur_fee'])/100+0.0001

url = "https://www.bitstamp.net/api/v2/sell/market/btceur/"
nonce = str(int(time.time())+1)
message = nonce + customer_id + api_key
signature = hmac.new(
       API_SECRET,
       msg=message,
       digestmod=hashlib.sha256
).hexdigest().upper()
amount = btcjev
data = {'key':api_key,'nonce':nonce,'signature':signature,'amount':amount}
request = urllib2.Request(url,urllib.urlencode(data))
response = urllib2.urlopen(request)
d = response.read()
data = json.loads(d)
print(json.dumps(data,indent=2,sort_keys=True))
