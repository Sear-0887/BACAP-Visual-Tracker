import datetime
import typing
from types_mypy import *

from config import RED, RESET, YELLOW

# The universal utilities used by all scripts. #

def toTimestamp(ts: str):
    return datetime.datetime.timestamp(datetime.datetime.fromisoformat(ts))

def overlap(l1: typing.Iterable[typing.Any], l2: typing.Iterable[typing.Any]):
    return list(set(l1) & set(l2))

def exclude(l1: typing.Iterable[typing.Any], l2: typing.Iterable[typing.Any]):
    return list(set(l1) - set(l2))

def error(*args: typing.Any, **kwargs: typing.Any):
    print(f"{RED}ERROR:", *args, **kwargs)
    print(RESET, end="")
    
def warning(*args: typing.Any, **kwargs: typing.Any):
    print(f"{YELLOW}WARNING:", *args, **kwargs)
    print(RESET, end="")

_T1 = typing.TypeVar("_T1")
def nameDefaulting(name: str, data: typing.Dict[str, _T1]|JSONTextType, default: _T1):
    return data.get(name, default)

def convertRGBStrToTuple(RGBStr: str) -> RGBTuple:
    return (
        int(RGBStr[1:3], 16),
        int(RGBStr[3:5], 16),
        int(RGBStr[5:7], 16)
    )