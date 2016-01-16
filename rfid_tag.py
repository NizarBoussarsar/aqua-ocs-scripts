import serial

ser = serial.Serial('/dev/ttyAMA0', timeout=1)
rfidData = ''

print "Waiting for RFID Tag.."

while True:
    if (ser.isOpen() == False):
        ser.open()
        ser.flushInput()
        ser.flushOutput()
        #rfidData = ser.read(14)
	rfidData = ser.readline()
    if len(rfidData) > 0:
        print "RFID Tag number:", rfidData
        ser.close()
#		print "Communication closed"
    break