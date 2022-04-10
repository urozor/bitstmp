# poglej odprta narocila
import urllib, urllib2, json 
import hmac
import hashlib
import time


customer_id="123"
API_SECRET="123"
api_key = "123"

url = "https://www.bitstamp.net/api/v2/open_orders/btceur/"
nonce = str(int(time.time()))
message = nonce + customer_id + api_key

signature = hmac.new(
    API_SECRET,
    msg=message,
    digestmod=hashlib.sha256
).hexdigest().upper()

data = {'key':api_key,'nonce':nonce,'signature':signature}
request = urllib2.Request(url,urllib.urlencode(data))
response = urllib2.urlopen(request)
d = response.read()
data = json.loads(d)
print(json.dumps(data,indent=2,sort_keys=True))
