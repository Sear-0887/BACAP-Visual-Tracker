import pygame
import typing

from config import *

from fileReader import getadvCache, loadAllAdv
from adv_class import Advancement, RefreshRaw
from displayGuiModule import CheckBox, GuiElement, Button, InputBox, JSONText, RectBox, SelectionBox, Text
from types_mypy import *

pygame.init()
pygame.key.set_repeat(500, 50)

root = pygame.display.set_mode((WIDTH, HEIGHT))
Running: bool = True

currentOptions = dict(map(lambda x: (x[0], x[1]["default"]), OptionsConfig.items()))

def displayAdv(advName: str, allQualified: typing.List[Advancement]):
    GuiElement.deleteGuiElementById("adv_display_.*")
    for Adv in allQualified:
        if advName != Adv.title: continue
        cursorx, cursory = 300, 100
        titleBox = JSONText("adv_display_title", (cursorx, cursory), Adv.titleJSON)
        cursory += titleBox.textSurface.get_height() + 10
        descBox = JSONText("adv_display_desc", (300, cursory), Adv.descriptionJSON)
        cursory += descBox.textSurface.get_height()

        for l, criterion in enumerate(Adv.playerData["incompleted"]):
            Text(f"adv_display_incomp_line_{l}", (300, cursory), "/".join(criterion), COLOR["red"])
            cursory += 32
        for l, criterion in enumerate(Adv.playerData["completed"]):
            Text(f"adv_display_comp_line_{l}", (300, cursory), "/".join(criterion), COLOR["green"])
            cursory += 32

def filtering(x: Advancement, query: str) -> bool:
    onlyShowSelected = currentOptions["onlyShow"]
    packSelected = currentOptions["pack"]
    isCaseSensitive = currentOptions["caseSensitive"]
    caseSensitiveCheck = bool(
        (
            not isCaseSensitive and (
                query.lower() in x.title.lower() or
                query.lower() in x.description.lower() or
                query.lower() in x.id.lower()
            )
        ) or (
            isCaseSensitive and (
                query in x.title or
                query in x.description or
                query in x.id
            )
        )
    )
    onlyShowCheck = bool(
        (onlyShowSelected in ["completed", "all"] and x.playerData["isDone"]) or
        (onlyShowSelected in ["incompleted", "all"] and not x.playerData["isDone"])
    )
    PackCheck = bool(
        packSelected in [x.baseID, "all"]
    )

    return caseSensitiveCheck and PackCheck and onlyShowCheck

def setFilterOptions(x: SelectionBox | CheckBox):
    id_ = x.id.split("_")[1]
    if isinstance(x, SelectionBox):
        print(f"setting {id_} to {x.selection[x.selectedIndex]}")
        currentOptions[id_] = x.selection[x.selectedIndex]
    elif isinstance(x, CheckBox): # type: ignore
        print(f"toggling {id_} to {x.checked}")
        currentOptions[id_] = x.checked

def ToggleFilterPopup(_: Button):
    if GuiElement.getElementExist("advfilter_baseplate"):
        GuiElement.deleteGuiElementById("advfilter_.*")
        return
    cursorx, cursory = 300, 32
    RectBox("advfilter_baseplate", (cursorx, cursory), (210, 32*len(OptionsConfig.items())), COLOR["black"])
    for optionName, option in OptionsConfig.items():
        label = Text(f"advfilter_{optionName}_label", (cursorx, cursory), optionName)
        if option["type"] == "SelectionBox":
            SelectionBox(
                f"advfilter_{optionName}_sel", 
                (cursorx + label.textSurface.get_width() + 40, cursory), 
                (0, 32), 
                option["selections"], 
                setFilterOptions, 
                option["selections"].index(str(currentOptions[optionName]))
            )
        elif option["type"] == "CheckBox":
            CheckBox(
                f"advfilter_{optionName}_sel", 
                (cursorx + label.textSurface.get_width() + 40, cursory), 
                (32, 32), 
                setFilterOptions,
            )
        cursory += 32


def searchAdv(query: str):
    GuiElement.deleteGuiElementById("adv_found_text")
    GuiElement.deleteGuiElementById("qualified_adv_.*")
    allQualified = list(filter(lambda x: filtering(x, query), getadvCache()))
    Text("adv_found_text", (0, 32), f"Found {len(allQualified)} matching Advancement:")
    for i, Adv in enumerate(allQualified):
        Button(
            f"qualified_adv_{Adv.id}", 
            (0, 36*i+36+32), (0, 32), 
            Adv.title, 
            lambda x: displayAdv(x.text, allQualified) # type: ignore
        )

def Refresh(_: Button):
    RefreshRaw()
    loadAllAdv()

InputBox("advsearchbox", (0, 0), (140, 32), "Search...", lambda self: searchAdv(self["text"])) # type: ignore
Button(
    "advsearchbtn", (230, 0), (70, 32), "Search", 
    lambda _: searchAdv(GuiElement.getElementById("advsearchbox")["text"]) # type: ignore
    )
Button(
    "advsearchfilterbtn", (300, 0), (0, 32), "Filter", 
    ToggleFilterPopup
    )
Button(
    "advrefreshbtn", (400, 0), (0, 32), "Refresh",
    Refresh
)

def processesAllInput(allEvents: typing.List[pygame.event.Event]):
    for element in GuiElement.getAllGuiElement():
        for event in allEvents:
            element.handle_event(event)
        element.update()
        element.draw(root)

RefreshRaw()
while Running:
    root.fill(COLOR["black"])
    allEvents = pygame.event.get()
    processesAllInput(allEvents)
    for event in allEvents:
        if event.type == pygame.QUIT:
            Running = False
    pygame.display.flip()