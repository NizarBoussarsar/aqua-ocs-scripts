# Scripts running withing the RPi (B2)

## Introduction
This repo contains the different scripts running withing the RaspberyPi we're
using for the Smart Aquarium OCS project.

Some of these scripts run when the system has just booted, some run every few
minutes other run when external events occur.

## List of Scripts

1. startup.py
    * **Done**:

    1. Get Local Tank “Code” form ENV (/etc/environment)

    2. Send GET query to `/tank` to get the current tank config.

    3. Get TEMP & sun/moon (brightness) DATA FROM SERVER.

    * **TODO**:

    1. Set Brightness / temperature in tank.

    2. [CRON]Check back every X minutes.

    3. Blink LED



2. CRON sun/moon (Once a day)
-  > GET sun/moon (brightness) Data from sever
 - > Every (x) minutes apply values to tank (calculate local brightness from daily values)

3. CRON temp (every x minutes)
 - >GET temperature values and apply to tank
     
  
4. RFID READ (BACKGROUND TASK)
 => IF Read value, send value (PUT) to add fish to tank API

6. UPnP [TODO]

 offer lum value


7. ping.py [OK]

    * **Done**:

    1. Ping server with tank code.
    This re-sets the tank attribute lastPinged to current dateTime.

    * **TODO**:

    1. add ping.py to system cron (every 5 minutes).


## Licence

TBD
