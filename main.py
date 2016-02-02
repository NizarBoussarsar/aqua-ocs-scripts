#!/usr/bin/python

import socket
import os
import glob
import time
import sqlite3
import datetime
import dateutil.parser


# TODO
# Get Temperature (DONE TODO TEST)
# Set Temperature
# Get Light (Done)
# Set Light
# UPNP x2 (DONE TODO integrate & test)

def updateInDB(col, value):
    conn = sqlite3.connect('aqua.db')
    c = conn.cursor()
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)
    req = "UPDATE locals SET " + str(col) + " ='" + str(value) + "' WHERE today ='" + today + "'"
    print req
    c.execute(req)
    conn.commit()
    c.close()


    ###############################


def getUPnPLight():
    conn = sqlite3.connect('aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnpLight FROM 'locals'")
    data = c.fetchone()
    conn.close()
    return float(data[0])


def getRealLight():
    conn = sqlite3.connect('aqua.db')
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
    conn = sqlite3.connect('aqua.db')
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

    # raw
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        # return temp_c, temp_f
        return temp_c
    return -273.15


def setTemperature(value):
    updateInDB("temp", value)


def setUPnPTemperature(value):
    if isUPnPEnabled():
        updateInDB("upnpTemp", value)
        # setTemperature(value)
        # TODO underestand this
    else:
        print "Not Upnp"


def setLight(value):
    pass


def setUPnPLight(value):
    if isUPnPEnabled():
        updateInDB("upnpLight", value)
        setLight(value)
    else:
        print "Not Upnp"


###############################

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

            print "Action ", action, " Value ", value

            if action == "sample":
                pass
            elif action == "setTemperature":
                setTemperature(value)
            elif action == "setLight":
                setLight(value)
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

###############
# isUPnPEnabled()
# print getLight()
