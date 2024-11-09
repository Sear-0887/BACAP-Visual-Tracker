# If you wish to use this version, please drag this file to the same level as main.py. #

from colorama import init as Colorama_Init

from config import *
from fileReader import getadvCache

Colorama_Init()

def consoleSearch(query: str):
    qualified = list(filter(lambda x: x.title == query, getadvCache()))
    # print(qualified)
    print(len(qualified))
    index = 1
    for advi in qualified:
        print(YELLOW, index, DONE if advi.playerData["isDone"] else NOTDONE, advi.title, RESET)
        index += 1
    print(qualified[int(input("Enter Index: "))-1])

if __name__ == "__main__":
    while True:
        consoleSearch(input("Enter Search: "))
