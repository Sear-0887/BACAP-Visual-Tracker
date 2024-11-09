import typing
import time
import zipfile
# import re

from config import *
from advClass import Advancement

isAdvCached = False
advCache: typing.List[Advancement] = []
def loadAllAdv() -> typing.List[Advancement]:
    old = time.time()
    result: typing.List[Advancement] = []
    basePath: zipfile.Path = zipfile.Path(DATAPACKZIP, "data/")

    for defPath in basePath.glob("*/advancements/*/*.json"):
        loadedAdv = Advancement(defPath)
        if not loadedAdv.isDisplayMissing:
            result.append(loadedAdv)
    
    print(f"Finished loading all Adv, took {time.time()-old}s")
    global isAdvCached
    isAdvCached = True
    return result

def getadvCache():
    global advCache
    if not isAdvCached: advCache = loadAllAdv()
    return advCache