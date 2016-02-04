#!/bin/sh
cd /home/pi/Aquarium/scripts/startups/

python startup.py
echo "startup"
python udp_server.py
echo "udp_server"
mono SampleDevice.exe
echo "SampleDevice"
python rfid_tag.py
echo "rfid_tag"

cd /