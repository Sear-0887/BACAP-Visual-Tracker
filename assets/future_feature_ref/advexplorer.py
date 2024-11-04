import typing
from adv_class import adv
from assets.consoleBased import loadAllAdv
from config import *

advCache: typing.List[adv] = loadAllAdv()

# if anchor == "center":
#     textRect = textSurf.get_rect()
#     root.blit(textSurf, (coord[0] - textRect.w // 2, coord[1] - textRect.h // 2))
# else:
#     root.blit(textSurf, coord)
IdToAdv: typing.Dict[str, adv] = {}
for Adv in advCache: IdToAdv[Adv.id] = Adv

def searchChildren(Id: str):
    result: typing.List[adv] = []
    for Adv in advCache:
        if Adv.parentID == Id:
            result.append(Adv)
    return result

def displayChildren(Id: str, depth: int = 0):
    print("| " * depth + Id)
    for Adv in searchChildren(Id): print("| " * (depth + 1) + Adv.id)

# displayChildren("minecraft:husbandry/tactical_fishing", 0)

def displayDirectory(CurrentAdv: adv, depth: int = 0):
    print(YELLOW + "-" * depth + ">", end=" ")
    print((DONE if CurrentAdv.playerData["isDone"] else NOTDONE), CurrentAdv.title, "(Hidden)" if CurrentAdv.hidden else "")
    for Adv in searchChildren(CurrentAdv.id):
        displayDirectory(Adv, depth + 1)

displayDirectory(IdToAdv["blazeandcave:statistics/root"], 0)