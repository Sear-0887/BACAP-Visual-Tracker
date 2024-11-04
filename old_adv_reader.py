import os
import re
import json
import time
import typing
from colorama import *

from config import BACAP_DIR, BACAP_ID, DONE, GREEN, NOTDONE, RESET, YELLOW, PDFILE
from utils import error, exclude, nameDefaulting, warning

init()

# This file is no longer refrenced in the code, it is only left as an refrence material. #

allTabs: typing.List[str] = os.listdir(BACAP_DIR)

def cvPathToID(path: str):
    bacapdirNormalize = BACAP_DIR.replace('\\', '/')
    return re.sub(fr"{bacapdirNormalize}/(.*)/(.*)\.json", fr"{BACAP_ID}\1/\2", path.replace("\\", "/"))


def searchplayerData(id_: str):
    with open(PDFILE, encoding="utf-8") as f:
        raw: typing.Dict[str, typing.Any] = json.load(f)
    for key, item in raw.items():
        if not key.startswith(BACAP_ID): continue
        if id_ not in key: continue
        return (key, item)
    warning(f"ID {id_} is not present in playerData. Used empty data.")
    return (id_, {"criteria": {}, "done": False}) # Empty Player Data





def searchByNameInTab(inp: str, tabName: str):
    result = []
    if tabName not in allTabs: return error("Tab Not Found")
    tabPath = os.path.join(BACAP_DIR, tabName)
    for defFileName in os.listdir(tabPath):
        if not defFileName.endswith(".json"): 
            return warning("Non-AdvDef found in Tab folders")
        defPath = os.path.join(tabPath, defFileName)
        with open(defPath, encoding="utf-8") as f:
            rawDef: typing.Dict[str, typing.Any] = json.loads(f.read().replace("\\'", "'"))
        if "display" not in rawDef.keys(): 
            warning(f"No Display found for {defPath}, skipping")
            continue
        defName = rawDef["display"]["title"]["translate"]
        if inp.lower() in defName.lower(): 
            result.append((defName, defPath))
    return result
    
def searchByNameMass(inp: str):
    result = []
    for tabName in os.listdir(BACAP_DIR):
        result += searchByNameInTab(inp, tabName)
    return result
        
def progressionFormating(playerData, display, requirements, id_, done):
    progressNames = playerData["criteria"].keys()
    incompleted = []
    completed = []
    
    for requirement in requirements:
        completion = len(exclude(requirement, progressNames)) != len(requirement)
        if completion: completed.append(DONE    + " " + "/".join(requirement))
        else:        incompleted.append(NOTDONE + " " + "/".join(requirement))
        # print(completion, "/".join(requirement)) 
        
    color = GREEN if done else YELLOW
    name = display["title"]["translate"]
    percentage = len(completed)/len(requirements)*100
    typ = nameDefaulting("frame", display, "task")
    # typ = display["frame"] if "frame" in display.keys() else "task"
    hidden = f"{DONE} Yes" if "hidden" in display.keys() else f"{NOTDONE} No"
    desc = display["description"]["translate"]
    
    print(f"""
{color}{name} - {len(completed)}/{len(requirements)} ({round(percentage, 2)}%)
{RESET}| {id_} | Type - {typ} | Hidden - {hidden} {RESET}|
{RESET}{desc}
          """)
    print("\n".join(incompleted))
    print("\n".join(completed))

def displayAdv(advPath: str):
    id_, playerData = searchplayerData(cvPathToID(advPath))
    isAdvDone = playerData['done']
    with open(advPath, encoding="utf-8") as f:
        rawDef: typing.Dict[str, typing.Any] = json.load(f)
    progressionFormating(
        playerData, 
        rawDef["display"], 
        nameDefaulting('requirements', rawDef, list(map(lambda x: [x], rawDef['criteria']))),
        # rawDef['requirements'] if 'requirements' in rawDef else list(map(lambda x: [x], rawDef['criteria'])),
        id_,
        isAdvDone
    )
            
def advInfoSearch(inp: str):
    print(f"Searching for {inp}")
    old = time.time()
    found = searchByNameMass(inp)
    if (len(found) == 0): return print(f"No result found for \"{inp}\".")
    print(f"Found {len(found)} results for \"{inp}\":")
    for i, (name, _path) in enumerate(found):
        print(f"- [{i+1}] {name}")
    warning(f"Loaded all adv in {time.time()-old}s")
    usrindex = int(input(f"Enter the index for the correct result: "))
    _name, path = found[usrindex-1]
    displayAdv(path)
    
# Console Testing #
if __name__ == "__main__":
    while True:
        advInfoSearch(input("Enter the Search: "))