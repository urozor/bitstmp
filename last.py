# preverja zadnjo ceno btc
import urllib, urllib2, json 
import hmac
import hashlib
import time

prodajalec_lastprice="lastprice.txt"

customer_id="123"
API_SECRET="123"
api_key = "123"

while True:
	url = "https://www.bitstamp.net/api/v2/ticker_hour/btceur/"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	#last=float(data['last'])
	print(json.dumps(data,indent=2,sort_keys=True))

	#print (str(bchjev)+' BCH, '+str(evrov)+' EUR, zadnja cena:'+str(last))
	#file=open(prodajalec_lastprice,"r")
	#zadnjaprodajna=float(file.read())
	#file.close()
	time.sleep(10)

