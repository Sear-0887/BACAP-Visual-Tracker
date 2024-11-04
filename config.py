import json
from types_mypy import *
from colorama import *

init()

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

BACAP_ID = "blazeandcave:"
BACAP_DIR = config["packPath"][BACAP_ID]

MC_ID = "minecraft:"
MC_DIR = config["packPath"][MC_ID]

PDFILE = config["playerDataPath"]

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

OptionsConfig: OptionConfigType = {
    "onlyShow": {
        "type": "SelectionBox",
        "default": "all",
        "selections": ['completed', 'incompleted', 'all']
    },
    "pack": {
        "type": "SelectionBox",
        "default": "all",
        "selections": ['bacap', 'vanilla', 'all']
    },
    "caseSensitive": {
        "type": "CheckBox",
        "default": False
    }
}