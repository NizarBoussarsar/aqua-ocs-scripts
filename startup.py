from datetime import tzinfo

import requests
import time
import os
import datetime
import dateutil.parser

# import RPi.GPIO as GPIO

# code = os.environ["TANKCODE"]
code = "354"
json_obj = ''
lat = '43.64152'
lng = '7.009186'


# ledPin = 23

def getTankInfos():
    req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
    json_obj = req.json()
    json_obj = json_obj[0]


# print json_obj

def updateTankStatus():
    payload = {'state': 'online'}
    requests.put("https://aqua-ocs.herokuapp.com/tank/" + str(json_obj['id']), data=payload)


def getBrightnessLevel():
    # https://aqua-ocs.herokuapp.com/tank/light?lat=&lng= hedha yrajaalek moon value {"moon":0.46980866740073773,"status":"OK"}
    req = requests.get("https://aqua-ocs.herokuapp.com/tank/light?lng=" + lng + "&lat=" + lat)
    json_obj = req.json()
    # print json_obj

    now = datetime.datetime.now().replace(tzinfo=None)
    sunriseTime = dateutil.parser.parse(json_obj['lightStart']).replace(tzinfo=None)
    sunsetTime = dateutil.parser.parse(json_obj['lightEnd']).replace(tzinfo=None)
    solarNoonTime = dateutil.parser.parse(json_obj['lightMid']).replace(tzinfo=None)
    lightLength = json_obj['lightLength']

    ##
    if (now > sunriseTime) and (now < sunsetTime):
        print "morning"
        if now < solarNoonTime:
            print "9bal"
            seconds = time.mktime(solarNoonTime.timetuple()) - time.mktime(now.timetuple())
            val = int(100) * float((seconds / lightLength))
            print "val: " + str("%.2f" % val)
        else:
            print "baad"
            seconds = time.mktime(now.timetuple()) - time.mktime(solarNoonTime.timetuple())
            val = int(100) * float((seconds / lightLength))
            print "val: " + str("%.2f" % val)
    else:
        print "night"
        val = float(("%.2f" % json_obj['moon'])) * int(100)
        print "Brightness level: " + str(val)
    ##

def start():
    if (json_obj != []):
        getTankInfos()
        updateTankStatus()
    else:
        '''
		for i in range(0, 4):
			GPIO.output(ledPin, GPIO.LOW)
			print "BLINK"
			time.sleep(1)
			GPIO.output(ledPin, GPIO.HIGH)
			print "BLANK"
			time.sleep(1)
		'''
        time.sleep(10)
        # time.sleep(300)
        start(json_obj)


'''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
'''

# getTankInfos()
# start()
getBrightnessLevel()
