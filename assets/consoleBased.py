import os

import typing
import time
from colorama import init as Colorama_Init

from config import *
from utils import warning
from adv_class import Advancement

Colorama_Init()

isAdvCached = False

# import profilehooks
# @profilehooks.profile(stdout=False, filename='baseline_imp.prof')
def loadAllAdv():
    old = time.time()
    result = []
    def loadAdvInDir(baseDir: str, isBACAP: bool):
        for tabName in os.listdir(baseDir):
            tabPath = os.path.join(baseDir, tabName)
            for defFileName in os.listdir(tabPath):
                if not defFileName.endswith(".json"): 
                    return warning("Non-AdvDef found in Tab folders")
                defPath = os.path.join(tabPath, defFileName)
                loadedAdv = Advancement(defPath, isBACAP)
                if not loadedAdv.isDisplayMissing:
                    result.append(loadedAdv)
    loadAdvInDir(BACAP_DIR, True)
    loadAdvInDir(MC_DIR, False)
    print(f"Finished loading all Adv, took {time.time()-old}s")
    global isAdvCached
    isAdvCached = True
    return result




def getadvCache(query: str):
    global advCache
    if not isAdvCached: advCache = loadAllAdv()
    return advCache

def consoleSearch(query: str):
    qualified = getadvCache(query)
    # print(qualified)
    print(len(qualified))
    index = 1
    for advi in qualified:
        print(YELLOW, index, DONE if advi.playerData["isDone"] else NOTDONE, advi.title, RESET)
        index += 1
    print(qualified[int(input("Enter Index: "))-1])

if __name__ == "__main__":
    advCache: typing.List[Advancement] = loadAllAdv()
    while True:
        consoleSearch(input("Enter Search: "))
