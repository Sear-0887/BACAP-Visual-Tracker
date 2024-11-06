import typing
from colorama import init as Colorama_Init

from config import *
from fileReader import getadvCache, loadAllAdv
from adv_class import Advancement

Colorama_Init()

isAdvCached = False

def consoleSearch(query: str):
    qualified = getadvCache()
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
