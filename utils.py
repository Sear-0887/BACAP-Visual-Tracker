import datetime
import typing

from config import RED, RESET, YELLOW

# The universal utilities used by all scripts. #

def toTimestamp(ts):
    return datetime.datetime.timestamp(datetime.datetime.fromisoformat(ts))

def overlap(l1, l2):
    return list(set(l1) & set(l2))

def exclude(l1, l2):
    return list(set(l1) - set(l2))

def error(*args, **kwargs):
    print(f"{RED}ERROR:", *args, **kwargs)
    print(RESET, end="")
    
def warning(*args, **kwargs):
    print(f"{YELLOW}WARNING:", *args, **kwargs)
    print(RESET, end="")

def nameDefaulting(name, data, default):
    if name in data.keys():
        return data[name]
    else:
        return default

def convertRGBStrToTuple(RGBStr: str) -> typing.Tuple[int, int, int]:
    return (
        int(RGBStr[1:3], 16),
        int(RGBStr[3:5], 16),
        int(RGBStr[5:7], 16)
    )