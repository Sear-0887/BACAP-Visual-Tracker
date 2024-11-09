import json
import zipfile
from types_mypy import *
from colorama import Fore, init as Colorama_Init

Colorama_Init()

WIDTH = 1400
HEIGHT = 860
CENTER = (WIDTH//2, HEIGHT//2)

with open("config.json", "r", encoding="utf-8") as f:
    global config 
    config = json.load(f)



RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

DONE = GREEN + config["symbols"]["done"]
NOTDONE = RED + config["symbols"]["not_done"]

BASE = config['playerModProfile']
SAVES = f"{BASE}/saves/{config['targetedSaveFile']}"
DATAPACKZIP = f"{SAVES}/datapacks/bacap.zip"

with open(f"{BASE}/usercache.json", "r", encoding="utf-8") as f:
    usercache = json.load(f)

playerUUID = ""
for entry in usercache:
    if entry["name"] == config["playerName"]: 
        playerUUID = entry["uuid"]
        break
PDFILE = f"{SAVES}/advancements/{playerUUID}.json"

BACAP_ID = "blazeandcave"
MC_ID = "minecraft"


FONTNAME = config["fontPath"]

COLOR: ColorsType = {
    "black": (0, 0, 0),
    "dark_blue": (0, 0, 170),
    "dark_green": (0, 170, 0),
    "dark_aqua": (0, 170, 170),
    "dark_red": (170, 0, 0),
    "dark_purple": (170, 0, 170),
    "gold": (255, 170, 0),
    "gray": (170, 170, 170),
    "dark_gray": (85, 85, 85),
    "blue": (85, 85, 255),
    "green": (85, 255, 85),
    "aqua": (85, 255, 255),
    "red": (255, 85, 85),
    "light_purple": (255, 85, 255),
    "yellow": (255, 255, 85),
    "white": (255, 255, 255)
}
allPacks: typing.List[str] = [p.name for p in zipfile.Path(DATAPACKZIP, "data/").iterdir()]

OptionsConfig: OptionConfigType = {
    "onlyShow": {
        "type": "SelectionBox",
        "default": "all",
        "selections": ['completed', 'incompleted', 'all']
    },
    "pack": {
        "type": "SelectionBox",
        "default": "all",
        "selections": allPacks + ["all"]
    },
    "caseSensitive": {
        "type": "CheckBox",
        "default": False
    }
}
