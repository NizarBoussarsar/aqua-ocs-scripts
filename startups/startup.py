import datetime
import time
import warnings
import dateutil.parser
import grovepi
import requests
import sqlite3
from grovepi import *
import os

warnings.filterwarnings("ignore", category=UnicodeWarning)

code = os.environ["TANKCODE"]
json_obj = {}

# Connect the Grove LED Bar to digital port D3
ledbar = 3

# Connect the Grove LED to digital port D6
led = 6

def setLedValue(brightness):
    level = 0
    if (brightness > 0 and brightness <= 10):
        level = int('0000000001', 2)
    if (brightness > 10 and brightness <= 20):
        level = int('0000000011', 2)
    if (brightness > 20 and brightness <= 30):
        level = int('0000000111', 2)
    if (brightness > 30 and brightness <= 40):
        level = int('0000001111', 2)
    if (brightness > 40 and brightness <= 50):
        level = int('0000011111', 2)
    if (brightness > 50 and brightness <= 60):
        level = int('0000111111', 2)
    if (brightness > 60 and brightness <= 70):
        level = int('0001111111', 2)
    if (brightness > 70 and brightness <= 80):
        level = int('0011111111', 2)
    if (brightness > 80 and brightness <= 90):
        level = int('0111111111', 2)
    if (brightness > 90 and brightness <= 100):
        level = int('1111111111', 2)
    grovepi.ledBar_setBits(ledbar, level)

def getTankInfos(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
    local_json_obj = req.json()
    if local_json_obj != []:
        return local_json_obj[0]
    else:
        return []

def updateTankStatus(global_json_obj):
    now = datetime.datetime.now().replace(tzinfo=None)
    sendingData = {'state': 'online', 'lastPing': str(now)}
    requests.put("https://aqua-ocs.herokuapp.com/tank/" + str(global_json_obj['id']), data=sendingData)


def getBrightnessLevel(global_json_obj):
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
    return data

def checkLightUPnP():
    conn = sqlite3.connect('aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnp, upnpLight FROM 'locals'")
    data = c.fetchone()
    conn.close()
    return data

def start():
    grovepi.pinMode(ledbar, "OUTPUT")
    grovepi.ledBar_init(ledbar, 0)
    grovepi.ledBar_orientation(ledbar, 1)
    pinMode(led,"OUTPUT")
    json_obj = getTankInfos(code)
    if json_obj != []:
        updateTankStatus(json_obj)
        data = checkLightUPnP()
        if data != None:
            if data[0] == '1':
                level = int(data[1])
            else:
                json_brightness = getBrightnessLevel(json_obj)
                if json_brightness['time'] == "sun":
                    level = float(json_brightness['brightness'])
                else:
                    level = float(json_brightness['brightness'])
        setLedValue(int(level))
    else:
        for i in range(0, 4):
            digitalWrite(led,1)
            time.sleep(1)
            digitalWrite(led,0)
            time.sleep(1)
        time.sleep(60)
        start(json_obj)

start()
