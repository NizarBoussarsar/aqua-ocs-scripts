import requests
import warnings

warnings.filterwarnings("ignore", category=UnicodeWarning)

# code = os.environ["TANKCODE"]
code = '354'


def pingServer(code):
    #req = requests.get("https://aqua-ocs.herokuapp.com/tank/ping?tankCode=" + code)
    req = requests.get("http://localhost:1337/tank/ping?tankCode=" + code)
    local_json_obj = req.json()
    return local_json_obj["status"]


pingServer(code)
