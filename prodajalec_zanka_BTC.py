# btc auto trading
import urllib, urllib2, json 
import hmac
import hashlib
import time

prodajalec_lastprice="prodajalec_lastprice.txt"
delta=80 #koliko evrov razlike lovimo

customer_id="123"
API_SECRET="123"  #api account
api_key = "123" #api account

while True:
	# 1.korak - preveri ali je kaj odprtih narocil (sme biti samo eno!)
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
		btcjev=float(data['btc_available'])
		evrov=float(data['eur_available'])
		fee=float(data['btceur_fee'])/100+0.0001
	
		#3. korak - dobi zadnjo ceno btc
		url = "https://www.bitstamp.net/api/v2/ticker/btceur/"
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		last=float(data['last'])
		#print (str(btcjev)+' BTC, '+str(evrov)+' EUR, zadnja cena:'+str(last))
		file=open(prodajalec_lastprice,"r")
		zadnjaprodajna=float(file.read())
		file.close()
 
		if evrov>5: #kupi BTC, to je prioriteta		
			url = "https://www.bitstamp.net/api/v2/buy/btceur/"
			nonce = str(int(time.time())+2)
			message = nonce + customer_id + api_key
			signature = hmac.new(
       		         	API_SECRET,
               		 	msg=message,
                		digestmod=hashlib.sha256
			).hexdigest().upper()
			price=zadnjaprodajna-delta
			if zadnjaprodajna>=(last+delta): price=last
			amount = float("{0:.8f}".format(evrov/price))-float("{0:.8f}".format(evrov*fee/price))
			data = {'key':api_key,'nonce':nonce,'signature':signature,'amount':amount,'price':price}
			print (data)
			request = urllib2.Request(url,urllib.urlencode(data))
			response = urllib2.urlopen(request)
			d = response.read()
			print ('~~~~~ KUPI BTC ~~~~~')
			print(d)
			data = json.loads(d)
			file=open(prodajalec_lastprice,"w")
			file.write(str(price))
			file.close()
		if btcjev>0.005: #prodaj BTC
                	url = "https://www.bitstamp.net/api/v2/sell/btceur/"
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
			print ('~~~~~ PRODAJ BTC ~~~~~')
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
		time.sleep(1)
	time.sleep(10)

