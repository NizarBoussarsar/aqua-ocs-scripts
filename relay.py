import glob
import os
import time

import grovepi
import requests

# code = os.environ["TANKCODE"]
code = '354'

# Connect the Grove Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

json_obj = {}

localTemperature = ''
desiredTemperature = ''


def setRelay(state):
    grovepi.pinMode(relay, "OUTPUT")
    # state: 1 => ON and 0 => OFF
    grovepi.digitalWrite(relay, state)


def getTemperature(code):
    print
    req = requests.get("https://aqua-ocs.herokuapp.com/tank/temp?tankCode=" + code)
    local_json_obj = req.json()
    if local_json_obj['status'] == 'error':
        getTemperature(code)
    else:
        return float(local_json_obj['temp'])


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
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        # return temp_c, temp_f
        return temp_c


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

setRelay(0)

print "desired:" + str(getTemperature(code))
print "current:" + str(read_temp())

while read_temp() < getTemperature(code):
    setRelay(1)
    print "Still Cold! Heater ON..."
    print "desired:" + str(getTemperature(code))
    print "current:" + str(read_temp())
    time.sleep(60)

setRelay(0)

print "Good temperature!"