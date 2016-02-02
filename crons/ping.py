import datetime
import sqlite3
import warnings
import os
import requests

warnings.filterwarnings("ignore", category=UnicodeWarning)

code = os.environ["TANKCODE"]
tank = ''

def getTankByCode(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
    local_json_obj = req.json()
    local_json_obj = local_json_obj[0]
    return local_json_obj

def updateLocalDB(code):
    if tank["upnp"]:
        upnpVal = '1'
    else:
        upnpVal = '0'
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)
    req = "UPDATE locals SET upnp ='" + upnpVal + "' WHERE today ='" + today + "'"
    c.execute(req)
    conn.commit()
    c.close()

def pingServer(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank/ping?tankCode=" + code)
    local_json_obj = req.json()
    return local_json_obj["status"]

def updateInDB(col, value):
    conn = sqlite3.connect('../aqua.db')
    c = conn.cursor()
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)
    req = "UPDATE locals SET " + str(col) + " ='" + str(value) + "' WHERE today ='" + today + "'"
    print req
    c.execute(req)
    conn.commit()
    c.close()

tank = getTankByCode(code)

pingServer(code)
updateLocalDB(code)
updateInDB("temp", tank['temperature'])