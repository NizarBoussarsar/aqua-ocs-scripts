import os
import time
import re
import requests
import serial

code = os.environ["TANKCODE"]

ser = serial.Serial('/dev/ttyAMA0', timeout=1)
rfidData = ''

print "Waiting .."

while True:
    ser.close()
    ser.open()
    ser.flushInput()
    ser.flushOutput()
    rfidData = ser.read(15)
    if len(rfidData) > 0:
        fishTag = re.sub('[^A-Za-z0-9]+', '', rfidData)
        print "RFID Tag number:", fishTag
        ser.close()
        req = requests.get(
                "https://aqua-ocs.herokuapp.com/tank/addFish?tankCode=" + str(code) + "&fishTag=" + fishTag)
        local_json_obj = req.json()
        print "response : ", local_json_obj
        time.sleep(5)
