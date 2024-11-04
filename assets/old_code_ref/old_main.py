import json
import typing
import datetime
from old_adv_reader import BACAP_ID, advInfoSearch, allTabs, PDFILE
from utils import toTimestamp

# This file is no longer refrenced in the code, it is only left as an refrence material. #
# "Timeline" mode is a small demo on the display version #

def findLastCriteria(criteria):
    last = [("-", '2000-01-01 01:11:11 +0800')]
    for key, item in criteria.items():
        if toTimestamp(item) > toTimestamp(last[0][1]): last = [(key, item)]
        elif toTimestamp(item) == toTimestamp(last[0][1]): last.append((key, item))
    return last

def sortCriteria(defs):
    timeline = []
    for key, item in defs.items():
        if not key.startswith(BACAP_ID): continue
        if not item['done']: continue
        # print(key, item)
        last = findLastCriteria(item['criteria'])
        for name, time in item['criteria'].items():
            timeline.append((key, name, time, str((name, time) in last)))
    timeline.sort(key=lambda x: toTimestamp(x[2]))
    [print(i) for i in map(lambda x: " | ".join(x), timeline)]

print(allTabs)
mode = "timeline"
if mode == "search":
    while True:
        inp = input("Enter the Search: ")
        if inp == "": break
        advInfoSearch(inp)
elif mode == "timeline":
    with open(PDFILE, encoding="utf-8") as f:
        raw: typing.Dict[str, typing.Any] = json.load(f)
    sortCriteria(raw)
    