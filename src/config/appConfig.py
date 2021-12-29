import json

# initialize the app config global variable
appConf: dict = {}


def loadAppConfig(fName: str = "config/config.json") -> dict:
    # load config json into the global variable
    with open(fName, encoding="utf-8") as f:
        global appConf
        appConf = json.load(f)
        return appConf


def getAppConfig() -> dict:
    # get the cached application config object
    global appConf
    return appConf
