import datetime
import typing
from types_mypy import *

from config import RED, RESET, YELLOW

# The universal utilities used by all scripts. #

def toTimestamp(ts: str):
    return datetime.datetime.timestamp(datetime.datetime.fromisoformat(ts))

_T1 = typing.TypeVar("_T1")
_T2 = typing.TypeVar("_T2")

def overlap(l1: typing.Iterable[_T1], l2: typing.Iterable[_T2]) -> typing.List[_T1|_T2]:
    return list(set(l1) & set(l2))

def exclude(l1: typing.Iterable[_T1], l2: typing.Iterable[_T2]) -> typing.List[_T1|_T2]:
    return list(set(l1).difference(set(l2)))

def error(
        *args: object, 
        sep: str | None = " ",
        end: str | None = "\n",
        file: typing.TextIO | None = None,
        flush: bool = False
    ):
    print(f"{RED}ERROR:", *args, sep=sep, end=end, file=file, flush=flush)
    print(RESET, end="")
    
def warning(
        *args: object, 
        sep: str | None = " ",
        end: str | None = "\n",
        file: typing.TextIO | None = None,
        flush: bool = False
    ):
    print(f"{YELLOW}WARNING:", *args, sep=sep, end=end, file=file, flush=flush)
    print(RESET, end="")

def convertRGBStrToTuple(RGBStr: str) -> RGBTuple:
    return (
        int(RGBStr[1:3], 16),
        int(RGBStr[3:5], 16),
        int(RGBStr[5:7], 16)
    )