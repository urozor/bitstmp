# trading bch
import urllib, urllib2, json 
import hmac
import hashlib
import time

orderid_file="orderid_BCC.txt"
prodajalec_lastprice="prodajalec_lastprice_BCC.txt"
delta=3 #koliko evrov razlike lovimo

customer_id="123"
API_SECRET="123"
api_key = "123"

# 1.korak - preveri ali je kaj odprtih narocil (sme biti samo eno!)
url = "https://www.bitstamp.net/api/v2/open_orders/bcceur/"
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
print ('~~~~~ OPEN ORDERS ~~~~~')
print(d)
data = json.loads(d)
stevilo=len(data)
if stevilo==0:   # ce ne obstaja odprtih narocil, nadaljuj
	#2. korak - preveri stanje na racunu
	url = "https://www.bitstamp.net/api/v2/balance/"
	nonce = str(int(time.time())+1)
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
	print ('~~~~~ BALANCE ~~~~~')
	print(d)
	data = json.loads(d)
	btcjev=float(data['bch_available'])
	evrov=float(data['eur_available'])
	fee=0
#	fee=float(data['btceur_fee'])/100+0.0001

	#3. korak - dobi zadnjo ceno bch
	url = "https://www.bitstamp.net/api/v2/ticker/bcheur/"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	last=float(data['last'])
	#print (str(btcjev)+' BCH, '+str(evrov)+' EUR, zadnja cena:'+str(last))
        file=open(prodajalec_lastprice,"r")
        zadnjaprodajna=float(file.read())
        file.close()
 
	if evrov>5: #kupi BCH, to je prioriteta		
		url = "https://www.bitstamp.net/api/v2/buy/bcheur/"
		nonce = str(int(time.time())+2)
		message = nonce + customer_id + api_key
		signature = hmac.new(
                	API_SECRET,
                	msg=message,
                	digestmod=hashlib.sha256
		).hexdigest().upper()
		if zadnjaprodajna<last: last=zadnjaprodajna
		price=last-delta
		amount = float("{0:.8f}".format(evrov/price))-float("{0:.8f}".format(evrov*fee/price))
		data = {'key':api_key,'nonce':nonce,'signature':signature,'amount':amount,'price':price}
		print (data)
		request = urllib2.Request(url,urllib.urlencode(data))
		response = urllib2.urlopen(request)
		d = response.read()
		print ('~~~~~ KUPI BCH ~~~~~')
		print(d)
		data = json.loads(d)
                file=open(prodajalec_lastprice,"w")
                file.write(str(price))
                file.close()
        if btcjev>0.005: #prodaj BCH
                url = "https://www.bitstamp.net/api/v2/sell/bcheur/"
                nonce = str(int(time.time())+2)
                message = nonce + customer_id + api_key
                signature = hmac.new(
                        API_SECRET,
                        msg=message,
                        digestmod=hashlib.sha256
                ).hexdigest().upper()
		if zadnjaprodajna>=last: last=zadnjaprodajna
                price=last+delta
                amount = btcjev
                data = {'key':api_key,'nonce':nonce,'signature':signature,'amount':amount,'price':price}
		print ('~~~~~ PRODAJ BCH ~~~~~')
                print (data)
                request = urllib2.Request(url,urllib.urlencode(data))
                response = urllib2.urlopen(request)
                d = response.read()
                print(d)
                data = json.loads(d)
                file=open(prodajalec_lastprice,"w")
                file.write(str(price))
                file.close()
 
else:
	print('~~ Ne delam nic')
