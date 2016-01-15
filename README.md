1 – Start-up
- > Get Local Tank “Code” form ENV
- > Send GET query to /tank to get tank config
NO - >
Blink LED & Check back every X minutes  

YES →
Get TEMP & sun/moon (brightness) DATA FROM SERVER  


2- CRON sun/moon (Once a day)
-  > GET sun/moon (brightness) Data from sever
 - > Every (x) minutes apply values to tank (calculate local brightness from daily values)

3- CRON temp (every x minutes)  
 - >GET temperature values and apply to tank
     
  
5- RFID READ (BACKGROUND TASK)
 => IF Read value, send value (PUT) to add fish to tank API

6- UPnP
 offer lum value
