#!/usr/bin/python

import socket


def UDP_Client(channel, value):
    message = str(channel) + "#" + str(value)
    print "Starting UDP Client..."
    print "Content: ", message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, ("127.0.0.1", 5000))

    #    recv_data, addr = sock.recvfrom(2048)

    #    print recv_data, "!!"

    sock.close()
    print "Closing UDP Client..."


UDP_Client("Temperature", 10)
