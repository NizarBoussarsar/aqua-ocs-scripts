import random
import time

import grovepi

# Connect the Grove LED Bar to digital port D5
# DI,DCKI,VCC,GND
ledbar = 3
brightness = 56
level = ''

grovepi.pinMode(ledbar, "OUTPUT")
time.sleep(1)
i = 0

while True:
    try:
        if(brightness > 0 and brightness <= 10):
            print ""
            level = int('0000000001',2)
        if(brightness > 10 and brightness <= 20):
            print ""
            level = int('0000000011',2)
        if(brightness > 20 and brightness <= 30):
            print ""
            level = int('0000000111',2)
        if(brightness > 30 and brightness <= 40):
            print ""
            level = int('0000001111',2)
        if(brightness > 40 and brightness <= 50):
            print ""
            level = int('0000011111',2)
        if(brightness > 50 and brightness <= 60):
            print ""
            level = int('0000111111',2)
        if(brightness > 60 and brightness <= 70):
            print ""
            level = int('0001111111',2)
        if(brightness > 70 and brightness <= 80):
            print ""
            level = int('0011111111',2)
        if(brightness > 80 and brightness <= 90):
            print ""
            level = int('0111111111',2)
        if(brightness > 900 and brightness <= 100):
            print ""
            level = int('1111111111',2)

        grovepi.ledBar_setBits(ledbar, level)

    except KeyboardInterrupt:
        grovepi.ledBar_setBits(ledbar, 0)
        break
    except IOError:
        print ("Error")