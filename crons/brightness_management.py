import datetime
import sqlite3
import time

import dateutil.parser
import grovepi

'''
TODO: Finir Bguthness Management
getFromDB
setBrightness
'''

# Connect the Grove LED Bar to digital port D3
ledbar = 3


def isUPnPEnabled():
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnp FROM 'locals'")
    data = c.fetchone()
    conn.close()
    if data[0] == "1":
        print "UPnP enabled"
        return True
    else:
        print "UPnP not enabled"
        return False


def getRealLight():
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT startLight, midLight, endLight, dayLength, moon FROM 'locals'")
    data = c.fetchone()
    conn.close()

    now = datetime.datetime.now().replace(tzinfo=None)

    sunriseTime = dateutil.parser.parse(data[0]).replace(tzinfo=None)
    sunsetTime = dateutil.parser.parse(data[2]).replace(tzinfo=None)
    solarNoonTime = dateutil.parser.parse(data[1]).replace(tzinfo=None)
    lightLength = int(data[3])
    moonBrightness = float(data[4])

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

    return val


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


if isUPnPEnabled() == False:
    setLedValue(getRealLight())
