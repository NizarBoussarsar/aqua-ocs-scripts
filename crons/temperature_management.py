import glob
import os
import sqlite3
import time

import grovepi

relay = 5


def getIdealTemperature():
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnp, upnpTemp, temp FROM 'locals'")
    data = c.fetchone()
    conn.close()
    if data[0] == "1":
        return float(data[1])
    else:
        return float(data[2])


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def setRelay(state):
    grovepi.pinMode(relay, "OUTPUT")
    # state: 1 => ON and 0 => OFF
    grovepi.digitalWrite(relay, state)


setRelay(0)

desiredTemperature = getIdealTemperature()

print "desired:" + str(desiredTemperature)
print "current:" + str(read_temp())

while read_temp() < getIdealTemperature():
    setRelay(1)
    print "Still Cold! Heater ON..."
    print "desired:" + str(desiredTemperature)
    print "current:" + str(read_temp())
    time.sleep(60)

setRelay(0)

print "Good temperature!"
