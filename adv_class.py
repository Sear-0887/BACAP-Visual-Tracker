import json
import re
import typing
from utils import exclude, warning, nameDefaulting

from config import *

with open(PDFILE, encoding="utf-8") as f:
    raw: typing.Dict[str, typing.Any] = json.load(f)

# Main adv definition #

class Advancement:
    isBACAP: bool
    baseDir: str    # Determined solely by self.isBACAP
    baseID: str     # Determined solely by self.isBACAP
    parentID: str # 
    path: str = "???" # Bad input will cause itself to stay as "???"
    isDisplayMissing: bool = False # "display" is not present
    id: str = "???" # Determined by self.isDisplayMissing
    title: str = "???" # Determined by self.isDisplayMissing
    description: str = "???" # Determined by self.isDisplayMissing
    type: str = "task" # Determined by self.isDisplayMissing
    hidden: bool = False # Determined by self.isDisplayMissing
    # self.requirements is a array containing serval "requirement", which is an array containing the \
    # criteria for completing this "requirement".
    # Defaults as a [ <Everything listed in criteria, each criteria is an "requirement"> ]
    requirements: typing.List[typing.List[str]] = [] 
    # Stores 
    playerData: PlayerDataType = {'isDone': False, 'completed': [], "incompleted": []}

    def __init__(self, filepath: str, isBACAP: bool = False) -> None:
        self.path = filepath
        self.isBACAP = isBACAP

        if self.isBACAP:
            self.baseDir = BACAP_DIR
            self.baseID = BACAP_ID
        else:
            self.baseDir = MC_DIR
            self.baseID = MC_ID
        
        with open(self.path, encoding="utf-8") as f:
            fContent = json.loads(f.read().replace("\\'", "'"))
        self.id = re.sub(self.baseDir.replace('\\', '/') + r"/(.*)/(.*)\.json", fr"{self.baseID}\1/\2", filepath.replace("\\", "/"))
        self.isDisplayMissing = "display" not in fContent.keys()
        if self.isDisplayMissing: 
            return warning(f"No Display found for {filepath}, skipping")
        
        displayDef = fContent["display"]
        self.parentID = nameDefaulting("parent", fContent, "")
        self.title = self.translateText(displayDef["title"])
        self.titleJSON = displayDef["title"]
        self.description = self.translateText(displayDef["description"])
        self.descriptionJSON = displayDef["description"]
        self.type = nameDefaulting("frame", displayDef, "task")
        self.hidden = "hidden" in displayDef.keys() and displayDef["hidden"]
        self.requirements = nameDefaulting('requirements', fContent, list(map(lambda x: [x], fContent['criteria'])))
        self.playerData = {
            "isDone": False,
            "completed": [],
            "incompleted": []
        }
        self.updatePlayerProgress()
    
    def translateText(self, textObj):
        text = nameDefaulting("translate", textObj, nameDefaulting("text", textObj, ""))
        if "extra" in textObj.keys():
            for extra in textObj["extra"]:
                text += self.translateText(extra)
        return text

    def updatePlayerProgress(self):
        playerData = {
            "done": False,
            "criteria": {}
        }
        
        for key, item in raw.items():
            if not key.startswith(self.baseID): continue
            if self.id not in key: continue
            playerData = item
            break
        else:
            warning(f"ID {self.id} is not present in playerData. Used empty data.")

        self.playerData["isDone"] = playerData["done"]
        progressNames = playerData["criteria"].keys()
        
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
| BACAP - {self.isBACAP} | Done - {self.playerData['isDone']} | 
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


print(__name__)
if __name__ == "__main__":
    # print(str(adv(r"data\blazeandcave\advancements\weaponry\master_shieldsman.json")))
    # print(adv(r"data\blazeandcave\advancements\weaponry\master_shieldsman.json"))
    print(Advancement(r"data\blazeandcave\advancements\challenges\riddle_me_this.json"))