import typing
import time
import zipfile
from colorama import init as Colorama_Init

from config import *
from advClass import Advancement

Colorama_Init()

isAdvCached = False
advCache: typing.List[Advancement] = []
def loadAllAdv() -> typing.List[Advancement]:
    old = time.time()
    result: typing.List[Advancement] = []
    def loadAdvInDir(baseDir: str):
        for defPath in zf.namelist():
            if not (defPath.endswith(".json") and defPath.startswith(baseDir)): continue
            loadedAdv = Advancement(defPath, zf)
            if not loadedAdv.isDisplayMissing:
                result.append(loadedAdv)
            # tabPath = os.path.join(baseDir, tabName)
            # for defFileName in os.listdir(tabPath):
            #     if not defFileName.endswith(".json"): 
            #         warning("Non-AdvDef found in Tab folders")
            #     defPath = os.path.join(tabPath, defFileName)
            #     loadedAdv = Advancement(defPath, zf)
            #     if not loadedAdv.isDisplayMissing:
            #         result.append(loadedAdv)

    zf: zipfile.ZipFile = zipfile.ZipFile(DATAPACKZIP)
    loadAdvInDir(BACAP_DIR)
    loadAdvInDir(MC_DIR)
    zf.close()
    
    print(f"Finished loading all Adv, took {time.time()-old}s")
    global isAdvCached
    isAdvCached = True
    return result

def getadvCache():
    global advCache
    if not isAdvCached: advCache = loadAllAdv()
    return advCache