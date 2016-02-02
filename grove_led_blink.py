import time
from grovepi import *

# Connect the Grove LED to digital port D4
led = 6

pinMode(led,"OUTPUT")
time.sleep(1)

print "This example will blink a Grove LED connected to the GrovePi+ on the port labeled D4.  If you're having trouble seeing the LED blink, be sure to check the LED connection and the port number.  You may also try reversing the direction of the LED on the sensor."
print " "
print "Connect the LED to the port labele D4!" 

while True:
    try:
        #Blink the LED
        digitalWrite(led,1)		# Send HIGH to switch on LED
        print "LED ON!"
        time.sleep(1)

        digitalWrite(led,0)		# Send LOW to switch off LED
        print "LED OFF!"
        time.sleep(1)

    except KeyboardInterrupt:	# Turn LED off before stopping
        digitalWrite(led,0)
        break
    except IOError:				# Print "Error" if communication error encountered
        print ("Error")
