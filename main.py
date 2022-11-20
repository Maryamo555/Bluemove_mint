import os
import json
import bluemove


def getConfig():
        configFile = open("config.json", 'r')
        return list(json.load(configFile).values())


config = getConfig()

isWindows = True if os.name == 'nt' else False

if "bluemove.net" in config[0]:
    print("Found bluemove.net link")
    bluemove.mint(config, isWindows)

else:
    print("Could not recognize link")

