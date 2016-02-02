import requests
import time
import os
import datetime
import dateutil.parser
import json
import warnings

warnings.filterwarnings("ignore", category=UnicodeWarning)

# import RPi.GPIO as GPIO

# code = os.environ["TANKCODE"]
code = '354'
json_obj = {}


# ledPin = 23

def getTankInfos(code):
    req = requests.get("http://localhost:1337/tank?code=" + code)
    local_json_obj = req.json()
    local_json_obj = local_json_obj[0]
    print local_json_obj
    return local_json_obj


def updateTankStatus(global_json_obj):
    resp = requests.put("http://localhost:1337/tank/" + str(global_json_obj['id']), data='{"state" : "online"}')
    print "done edit"
    print resp.text


def getBrightnessLevel(global_json_obj):
    # http://localhost:1337/tank/light?lat=&lng= hedha yrajaalek moon value moon 0.46980866740073773 status OK"}
    req = requests.get("http://localhost:1337/tank/light?lng=" + str(global_json_obj['longitude']) + "&lat=" + str(global_json_obj['latitude']))
    local_json_obj = req.json()

    now = datetime.datetime.now().replace(tzinfo=None)
    sunriseTime = dateutil.parser.parse(local_json_obj['lightStart']).replace(tzinfo=None)
    sunsetTime = dateutil.parser.parse(local_json_obj['lightEnd']).replace(tzinfo=None)
    solarNoonTime = dateutil.parser.parse(local_json_obj['lightMid']).replace(tzinfo=None)
    lightLength = local_json_obj['lightLength']
    moonBrightness = local_json_obj['moon']
    val = 0
    data = {}

    '''
    now = datetime.datetime.now().replace(tzinfo=None)
    sunriseTime = dateutil.parser.parse('2016-01-16T07:01:42+00:00').replace(tzinfo=None)
    sunsetTime = dateutil.parser.parse('2016-01-16T16:21:42+00:00').replace(tzinfo=None)
    solarNoonTime = dateutil.parser.parse('2016-01-16T11:41:42+00:00').replace(tzinfo=None)
    lightLength = 33600
    moonBrightness = 0.48616002612055303
    val = 0
    data = {}
    '''

    if (now > sunriseTime) and (now < sunsetTime):
        data['time'] = 'sun'
        if now < solarNoonTime:
            seconds = time.mktime(solarNoonTime.timetuple()) - time.mktime(now.timetuple())
        else:
            seconds = time.mktime(now.timetuple()) - time.mktime(solarNoonTime.timetuple())
        val = 1 - (float((seconds / (lightLength / 2))))
        val = float(("%.3f" % float(val))) * int(100)
    else:
        data['time'] = 'moon'
        val = float(("%.3f" % float(moonBrightness))) * int(100)

    data['brightness'] = val
    json_data = json.dumps(data)
    print json_data
    return json_data


def start():
    json_obj = getTankInfos(code)
    if json_obj != []:
        updateTankStatus(json_obj)
        json_brightness = getBrightnessLevel(json_obj)
    else:
        for i in range(0, 4):
            #GPIO.output(ledPin, GPIO.LOW)
            print "BLINK"
            time.sleep(1)
            #GPIO.output(ledPin, GPIO.HIGH)
            print "BLANK"
            time.sleep(1)
        time.sleep(10)
        # time.sleep(300)
        #I think when using a environment variable, it is required to rerun the script in another session
        start(json_obj)
        #


'''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
'''

start()
