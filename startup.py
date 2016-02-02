import datetime
import json
import time
import warnings
import grovepi
import dateutil.parser
import requests

warnings.filterwarnings("ignore", category=UnicodeWarning)

'''
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
'''

# code = os.environ["TANKCODE"]
code = '354'
json_obj = {}

# Connect the Grove LED Bar to digital port D3
ledbar = 3

# ledPin = 23

def setLedValue(brightness):
    if(brightness < 10):
        grovepi.ledBar_setBits(ledbar, 0b0000000001)
    if (brightness > 10 and brightness <= 20):
        grovepi.ledBar_setBits(ledbar, 0b0000000011)
    if (brightness > 20 and brightness <= 30):
        grovepi.ledBar_setBits(ledbar, 0b0000000111)
    if (brightness > 30 and brightness <= 40):
        grovepi.ledBar_setBits(ledbar, 0b0000001111)
    if (brightness > 40 and brightness <= 50):
        grovepi.ledBar_setBits(ledbar, 0b0000011111)
    if (brightness > 50 and brightness <= 60):
        grovepi.ledBar_setBits(ledbar, 0b0000111111)
    if (brightness > 60 and brightness <= 70):
        grovepi.ledBar_setBits(ledbar, 0b0001111111)
    if (brightness > 70 and brightness <= 80):
        grovepi.ledBar_setBits(ledbar, 0b0011111111)
    if (brightness > 80 and brightness <= 90):
        grovepi.ledBar_setBits(ledbar, 0b0111111111)
    if (brightness > 90 and brightness <= 100):
        grovepi.ledBar_setBits(ledbar, 0b1111111111)

def getTankInfos(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
    local_json_obj = req.json()
    local_json_obj = local_json_obj[0]
    print local_json_obj
    return local_json_obj

def updateTankStatus(global_json_obj):
    now = datetime.datetime.now().replace(tzinfo=None)
    sendingData = {'state': 'online', 'lastPing': str(now)}
    print requests.put("https://aqua-ocs.herokuapp.com/tank/" + str(global_json_obj['id']),
                       data=sendingData).status_code


def getBrightnessLevel(global_json_obj):
    # https://aqua-ocs.herokuapp.com/tank/light?lat=&lng= hedha yrajaalek moon value moon 0.46980866740073773 status OK"}
    req = requests.get(
        "https://aqua-ocs.herokuapp.com/tank/light?lng=" + str(global_json_obj['longitude']) + "&lat=" + str(
            global_json_obj['latitude']))
    local_json_obj = req.json()

    now = datetime.datetime.now().replace(tzinfo=None)
    sunriseTime = dateutil.parser.parse(local_json_obj['lightStart']).replace(tzinfo=None)
    sunsetTime = dateutil.parser.parse(local_json_obj['lightEnd']).replace(tzinfo=None)
    solarNoonTime = dateutil.parser.parse(local_json_obj['lightMid']).replace(tzinfo=None)
    lightLength = local_json_obj['lightLength']
    moonBrightness = local_json_obj['moon']
    val = 0
    data = {}

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
    grovepi.pinMode(ledbar,"OUTPUT")
    grovepi.ledBar_init(ledbar, 0)
    json_obj = getTankInfos(code)
    if json_obj != []:
        updateTankStatus(json_obj)
        json_brightness = getBrightnessLevel(json_obj)
        if json_brightness['time'] == "sun":
            setLedValue(json_brightness['brightness'])
        else:
            setLedValue(json_brightness['brightness'] * 0.5)
    else:
        for i in range(0, 4):
            # GPIO.output(ledPin, GPIO.LOW)
            print "BLINK"
            time.sleep(1)
            # GPIO.output(ledPin, GPIO.HIGH)
            print "BLANK"
            time.sleep(1)
        time.sleep(10)
        # time.sleep(300)
        # I think when using a environment variable, it is required to rerun the script in another session
        start(json_obj)
        #



start()
