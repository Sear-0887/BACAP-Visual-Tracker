import json
import zipfile
import re
import typing
from utils import exclude, warning

from config import *

raw: typing.Dict[str, rawAdvDatatype] = {}
def RefreshRaw():
    global raw
    raw = {}
    with open(PDFILE, encoding="utf-8") as f:
        raw = json.load(f)

# Main adv definition #

class Advancement:
    path: str = "???" # Bad input will cause itself to stay as "???"
    modpackID: str     # Determined by path
    parentID: str 
    tab: str
    name: str
    isDisplayMissing: bool = False # "display" is not present
    id: str = "???" # Determined by self.isDisplayMissing
    title: str = "???" # Determined by self.isDisplayMissing
    titleJSON: JSONTextType = {"text": "???"}
    description: str = "???" # Determined by self.isDisplayMissing
    descriptionJSON: JSONTextType = {"text": "???"}
    type: str = "task" # Determined by self.isDisplayMissing
    hidden: bool = False # Determined by self.isDisplayMissing
    # self.requirements is a array containing serval "requirement", which is an array containing the \
    # criteria for completing this "requirement".
    # Defaults as a [ <Everything listed in criteria, each criteria is an "requirement"> ]
    requirements: typing.List[typing.List[str]] = [] 
    playerData: PlayerDataType = {
        'isDone': False, 
        'completed': [], 
        "incompleted": [],
        "criteriaTimeStamp": {}
    }

    def __init__(self, filepath: zipfile.Path) -> None:
        self.path = str(filepath)
        extracted = re.match(
            rf".*/data/(.*)/advancements/(.*)/(.*)\.json",
            self.path
        )

        if extracted is None: return warning(f"Bad Path {self.path}")
        self.modpackID, self.tab, self.name = extracted.groups()
        self.id = f"{self.modpackID}:{self.tab}/{self.name}"

        fContent = json.loads(filepath.read_text(encoding="utf-8").replace("\\'", "'"))

        self.isDisplayMissing = "display" not in fContent.keys()
        if self.isDisplayMissing: 
            return warning(f"No Display found for {filepath}, skipping")
        
        displayDef = fContent["display"]
        self.parentID = fContent.get("parent", "")
        self.title = self.translateText(displayDef["title"])
        self.titleJSON = displayDef["title"]
        self.description = self.translateText(displayDef["description"])
        self.descriptionJSON = displayDef["description"]
        self.type = displayDef.get("frame", "task")
        self.hidden = "hidden" in displayDef.keys() and displayDef["hidden"]
        criterias: typing.List[str] = fContent['criteria']
        self.requirements = fContent.get('requirements', list(map(lambda x: [x], criterias))) # type: ignore
        self.playerData = {
            "isDone": False,
            "completed": [],
            "incompleted": [],
            "criteriaTimeStamp": {}
        }
        self.updatePlayerProgress()
    
    def translateText(self, textObj: JSONTextType) -> str:
        text: str = textObj.get("translate", textObj.get("text", ""))
        for extra in textObj.get("extra", []):
            text += self.translateText(extra)
        return text

    def updatePlayerProgress(self) -> None:
        rawPlayerData: rawAdvDatatype = {
            "done": False,
            "criteria": {}
        }
        
        for key, item in raw.items():
            if not key.startswith(self.modpackID + ":"): continue
            if self.id not in key: continue
            rawPlayerData = item
            break
        else:
            warning(f"ID {self.id} is not present in playerData. Used empty data.")

        self.playerData["isDone"] = rawPlayerData["done"]
        self.playerData["completed"] = []
        self.playerData["incompleted"] = []
        self.playerData["criteriaTimeStamp"] = rawPlayerData["criteria"]
        progressNames = rawPlayerData["criteria"].keys()
        
        for requirement in self.requirements:
            completion = len(exclude(requirement, progressNames)) != len(requirement)
            if completion: self.playerData["completed"].append(requirement)
            else:        self.playerData["incompleted"].append(requirement)
    
    # Displaying
    def __repr__(self) -> str:
        if len(self.requirements) > 0:
            percentage = len(self.playerData["completed"])/len(self.requirements)*100
        else:
            percentage = 100
        color = GREEN if self.playerData["isDone"] else YELLOW
        incompleted = map(lambda x: NOTDONE + " " + "/".join(x), self.playerData["incompleted"])
        completed   = map(lambda x: DONE    + " " + "/".join(x), self.playerData["completed"])
        return f""" {color}
{self.title} - {len(self.playerData["completed"])}/{len(self.requirements)} ({round(percentage, 2)}%)
| ID - {self.id} | Type - {self.type} | Hidden - {self.hidden} |
| BaseID - {self.modpackID} | Done - {self.playerData['isDone']} | 
| PATH - {self.path} |
{self.description}

{"\n".join(incompleted)}
{"\n".join(completed)}
          """
# for Internal Testing 
# {"\n".join(DONE + "/".join(self.playerData["completed"]))}
#     def __str__(self) -> str:
#         if not self: return ""
#         return f"""
# Path | {self.path}
# ID   | {self.id}
# Name | {self.title}
# Desc | {self.description}
# type | {self.type}
# Hide | {self.hidden}
# Req  | {self.requirements}
# PD   | {self.playerData}
# """