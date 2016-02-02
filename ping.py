import datetime
import sqlite3
import warnings

import requests

warnings.filterwarnings("ignore", category=UnicodeWarning)

# code = os.environ["TANKCODE"]
code = '354'


def getTankByCode(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank?code=" + code)
    local_json_obj = req.json()
    local_json_obj = local_json_obj[0]
    return local_json_obj


tank = getTankByCode(code)


def updateLocalDB(code):
    if tank["upnp"]:
        upnpVal = '1'
    else:
        upnpVal = '0'
    conn = sqlite3.connect('aqua.db')
    c = conn.cursor()
    today = str('{:02d}'.format(datetime.datetime.now().day))
    today += str('{:02d}'.format(datetime.datetime.now().month))
    today += str(datetime.datetime.now().year)
    req = "UPDATE locals SET upnp ='" + upnpVal + "' WHERE today ='" + today + "'"
    c.execute(req)
    conn.commit()
    c.close()


def updateRemoteDB(code):
    conn = sqlite3.connect('aqua.db')
    c = conn.cursor()
    c.execute("SELECT upnpLight, upnpTemp FROM 'locals'")
    data = c.fetchone()
    conn.close()
    sendingData = {'upnpTemperature': str(data[0]), 'upnpLight': str(data[1])}
    print  sendingData

    requests.put("https://aqua-ocs.herokuapp.com/tank/" + str(tank['id']), data=sendingData)


def pingServer(code):
    req = requests.get("https://aqua-ocs.herokuapp.com/tank/ping?tankCode=" + code)
    local_json_obj = req.json()
    return local_json_obj["status"]


########

pingServer(code)

updateLocalDB(code)

updateRemoteDB(code)
