import requests
import time
import os
import RPi.GPIO as GPIO

ledPin = 23

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme 
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

code = os.environ["TANKCODE"]
#TODO: Replace it with environment variable 

req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
json_obj = req.json()

if (json_obj != []):
	json_obj = json_obj[0]
	print json_obj
	payload = {'state': 'online'}
	requests.put("https://aqua-ocs.herokuapp.com/tank/" + str(json_obj['id']), data=payload)
else:
	for i in range(0, 4):
		GPIO.output(ledPin, GPIO.LOW)
		print "BLINK"
		time.sleep(1)
		GPIO.output(ledPin, GPIO.HIGH)
		print "BLANK"
		time.sleep(1)
	time.sleep(10)
	#time.sleep(300)
	os.system("python test.py")
