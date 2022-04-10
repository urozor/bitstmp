# izpis transakcij
import urllib, urllib2, json 
import hmac
import hashlib
import time

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

url = "https://www.bitstamp.net/api/transactions/"
response = urllib.urlopen(url)
data = json.loads(response.read())
print(json.dumps(data,indent=2,sort_keys=True))
