import requests
import time
import os
import datetime
import dateutil.parser
import json
import warnings

# warnings.filterwarnings("ignore", category=UnicodeWarning)


# code = os.environ["TANKCODE"]
code = '354'
json_obj = {}


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
    req = requests.get("http://localhost:1337/tank/light?lng=" + str(global_json_obj['longitude']) + "&lat=" + str(
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
