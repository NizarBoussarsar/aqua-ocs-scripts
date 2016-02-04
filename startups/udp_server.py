#!/usr/bin/python

import datetime
import glob
import os
import socket
import sqlite3
import time
import requests
import dateutil.parser
import grovepi

code = os.environ["TANKCODE"]


def getUPnPValues():
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnp, upnpTemp, upnpLight  FROM 'locals'")
    data = c.fetchone()
    conn.close()
    return data;


def getLastDateInDB():
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)

    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT today FROM 'locals' WHERE today = '" + today + "'")
    data = c.fetchone()
    conn.close()
    if data == None:
        return False
    else:
        return True

'''
TODO: Remplacer INSERT INTO par UPDATE
'''

# Checks if the line in DB is from today
def checkTodayInDB():
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)
    if (getLastDateInDB() == False):
        upnpValues = getUPnPValues()
        if upnpValues == None:
            reqValues = "'0','0','0'"
        else:
            reqValues = "'" + upnpValues[0] + "','" + upnpValues[1] + "','" + upnpValues[2] + "'"

        req = "INSERT into locals (upnp, upnpTemp, upnpLight, today) Values(" + reqValues + ",'" + today + "');"
        c.execute(req)
        conn.commit()
        # Delete
        c2 = conn.cursor()
        req = "DELETE FROM locals where today <> '" + today + "';"
        c2.execute(req)
        conn.commit()
        conn.close()
        return False
    else:
        return True


def updateInDB(col, value):
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)
    req = "UPDATE locals SET " + str(col) + " ='" + str(value) + "' WHERE today ='" + today + "'"
    print req
    c.execute(req)
    conn.commit()
    c.close()


def getUPnPLight():
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnpLight FROM 'locals'")
    data = c.fetchone()
    conn.close()
    return float(data[0])


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


def getLight():
    if isUPnPEnabled():
        return getUPnPLight()
    else:
        return getRealLight()


def getTemperature():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    return -273.15


def setTemperature(value):
    updateInDB("temp", value)


def setUPnPTemperature(value):
    if isUPnPEnabled():
        updateInDB("upnpTemp", value)
        updateRemoteDB(code)
    else:
        print "Not in UPnP mode"


def setUPnPLight(value):
    if isUPnPEnabled():
        updateInDB("upnpLight", value)
        setBrightness(value)
        updateRemoteDB(code)
    else:
        print "Not in UPnP mode"


def getTankByCode(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
    local_json_obj = req.json()
    local_json_obj = local_json_obj[0]
    return local_json_obj

tank = getTankByCode(code)

def updateRemoteDB(code):
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnpLight, upnpTemp FROM 'locals'")
    data = c.fetchone()
    conn.close()
    sendingData = {'upnpTemperature': str(data[0]), 'upnpLight': str(data[1])}
    requests.put("https://aqua-ocs.herokuapp.com/tank/" + str(tank['id']), data=sendingData)

# Connect the Grove LED Bar to digital port D3
ledbar = 3

def setBrightness(brightness):
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

def main():
    print "Starting local UDP server..."
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 5000))
    print "Started UDP on port 5000"
    while 1:
        data, addr = s.recvfrom(1024)
        if addr[0] == '127.0.0.1':
            print "Data : ", data
            data = data.split("#")
            action = data[0]
            value = data[1]

            checkTodayInDB()

            if action == "setTemperature":
                setTemperature(value)
            elif action == "setUPnPTemperature":
                setUPnPTemperature(value)
            elif action == "setUPnPLight":
                setUPnPLight(value)
            elif action == "getLight":
                lightVal = getLight()
                s.sendto("Light#" + str(lightVal), addr)
            elif action == "getTemperature":
                tempVal = getTemperature()
                s.sendto("Temperature#" + str(tempVal), addr)
            else:
                print("[UDP Server] W00T are you talking about m8t ?")


main()
