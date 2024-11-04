import pygame
import typing

from config import *

from advmain import getadvCache, adv
from displayGuiModule import CheckBox, GuiElement, Button, InputBox, JSONTextBox, RectBox, SelectionBox, TextBox

pygame.init()
pygame.key.set_repeat(500, 50)


WIDTH = 1400
HEIGHT = 860
CENTER = (WIDTH//2, HEIGHT//2)

root = pygame.display.set_mode((WIDTH, HEIGHT))
RUNNING = True

class SelBoxOptions(typing.TypedDict):
    type: typing.Literal["SelectionBox"]
    default: str
    selections: typing.List[str]

class CheckBoxOptions(typing.TypedDict):
    type: typing.Literal["CheckBox"]
    default: bool

OptionsConfig: typing.Dict[str, typing.Union[SelBoxOptions, CheckBoxOptions]] = {
    "onlyShow": {
        "type": "SelectionBox",
        "default": "all",
        "selections": ['completed', 'incompleted', 'all']
    },
    "pack": {
        "type": "SelectionBox",
        "default": "all",
        "selections": ['bacap', 'vanilla', 'all']
    },
    "caseSensitive": {
        "type": "CheckBox",
        "default": False
    }
}
# currentOptions = {
# "onlyShow": "completed"
#}
currentOptions = dict(map(lambda x: (x[0], x[1]["default"]), OptionsConfig.items()))
print(currentOptions)
def displayAdv(advName: str, allQualified: typing.List[adv]):
    GuiElement.deleteGuiElementById("adv_display_.*")
    for Adv in allQualified:
        if advName != Adv.title: continue
        print(Adv)
        cursorx, cursory = 300, 100
        titleBox = JSONTextBox("adv_display_title", (cursorx, cursory), Adv.titleJSON)
        cursory += titleBox.textSurface.get_height() + 10
        descBox = JSONTextBox("adv_display_desc", (300, cursory), Adv.descriptionJSON)
        cursory += descBox.textSurface.get_height()

        for l, criterion in enumerate(Adv.playerData["incompleted"]):
            TextBox(f"adv_display_incomp_line_{l}", (300, cursory), "/".join(criterion), REDRGB)
            cursory += 32
        for l, criterion in enumerate(Adv.playerData["completed"]):
            TextBox(f"adv_display_comp_line_{l}", (300, cursory), "/".join(criterion), GREENRGB)
            cursory += 32

def Filter(x: adv, query: str) -> bool:
    if OptionsConfig["pack"]["type"] != "SelectionBox": return False
    if OptionsConfig["onlyShow"]["type"] != "SelectionBox": return False
    if OptionsConfig["caseSensitive"]["type"] != "CheckBox": return False
    if type(currentOptions["caseSensitive"]) != bool: return False
    print(x.title, query)
    onlyShowSelected = currentOptions["onlyShow"]
    packSelected = currentOptions["pack"]
    isCaseSensitive = currentOptions["caseSensitive"]
    caseSensitiveCheck = (
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
    onlyShowCheck = (
        (onlyShowSelected in ["completed",   "all"] and     x.playerData["isDone"]) or
        (onlyShowSelected in ["incompleted", "all"] and not x.playerData["isDone"])
    )
    PackCheck = (
        (packSelected     in ["bacap",       "all"] and     x.isBACAP             ) or
        (packSelected     in ["vanilla",     "all"] and not x.isBACAP             ) 
    )
    return caseSensitiveCheck and PackCheck and onlyShowCheck

def setFilterOptions(x: SelectionBox | CheckBox):
    id_ = x.id.split("_")[1]
    if isinstance(x, SelectionBox):
        print(f"setting {id_} to {x.selection[x.selectedIndex]}")
        currentOptions[id_] = x.selection[x.selectedIndex]
    elif isinstance(x, CheckBox):
        print(f"setting {id_} to {x.checked}")
        currentOptions[id_] = x.checked

def ToggleFilterPopup():
    if GuiElement.getElementExist("advfilter_baseplate"):
        GuiElement.deleteGuiElementById("advfilter_.*")
        return
    cursorx, cursory = 300, 32
    RectBox("advfilter_baseplate", (cursorx, cursory), (200, 64), BLACKRGB)
    for optionName, option in OptionsConfig.items():
        label = TextBox(f"advfilter_{optionName}_label", (cursorx, cursory), optionName)
        if option["type"] == "SelectionBox":
            SelectionBox(
                f"advfilter_{optionName}_sel", 
                (cursorx + label.textSurface.get_width() + 40, cursory), 
                (0, 32), 
                option["selections"], 
                setFilterOptions, 
                option["selections"].index(currentOptions[optionName])
                )
        elif option["type"] == "CheckBox":
            CheckBox(
                f"advfilter_{optionName}_sel", 
                (cursorx + label.textSurface.get_width() + 40, cursory), 
                (32, 32), 
                setFilterOptions,
                )
        cursory += 32


def searchAdv(query):
    GuiElement.deleteGuiElementById("adv_found_text")
    GuiElement.deleteGuiElementById("qualified_adv_.*")
    print(query)
    allQualified = list(filter(lambda x: Filter(x, query), getadvCache(query)))
    TextBox("adv_found_text", (0, 32), f"Found {len(allQualified)} matching Advancement:")
    for i, Adv in enumerate(allQualified):
        Button(f"qualified_adv_{Adv.id}", (0, 36*i+36+32), (0, 32), 
        Adv.title, lambda x: displayAdv(x.text, allQualified))

InputBox("advsearchbox", (0, 0), (140, 32), "Search...", lambda self: searchAdv(self["text"]))
Button("advsearchbtn", (230, 0), (70, 32), "Search", lambda self: searchAdv(GuiElement.getElementById("advsearchbox")["text"]))
Button("advsearchfilterbtn", (300, 0), (0, 32), "Filter", lambda x: ToggleFilterPopup())
CheckBox("testchk", (300, 300), (16, 16), lambda x: print(x["checked"]))
SelectionBox("testselbox", (350, 350), (0, 32), ["Test1", "Test2"], lambda x: print("aaa"))

def processesAllInput(allEvents):
    for element in GuiElement.getAllGuiElement():
        for event in allEvents:
            element.handle_event(event)
        element.update()
        element.draw(root)

# JSONTextBox(
#     "testJsonText",
#     (400, 400, 10, 10),
#     json.loads(r'{"color":"#FF2A2A","translate":"The first is to smith a compass that vanishes","extra":[{"text":"\n"},{"color":"#FF2A2A","translate":"The second is to slay a corpse that fishes"},{"text":"\n"},{"color":"#FF2A2A","translate":"The third is to travel on an upside-down mount"},{"text":"\n"},{"color":"#FF2A2A","translate":"The fourth is to take a temple tripwire into account"},{"text":"\n"},{"color":"#FF2A2A","translate":"The fifth is to be invisible yet be visible everywhere"},{"text":"\n"},{"color":"#FF2A2A","translate":"The sixth is to return the product of a fowl in mid-air"},{"text":"\n"},{"color":"#FF2A2A","translate":"The seventh is to allow a child to commit the act of stealing"},{"text":"\n"},{"color":"#FF2A2A","translate":"The eighth is to smite a Wither with splash healing"},{"text":"\n"},{"color":"#FF2A2A","translate":"The ninth is to be a pirate; parrot, spyglass, map, and boat"},{"text":"\n"},{"color":"#FF2A2A","translate":"The tenth, if you can achieve it, you will be the G.O.A.T."}]}'.replace("\'", "'"))
#     )

while RUNNING:
    root.fill(BLACKRGB)
    allEvents = pygame.event.get()
    processesAllInput(allEvents)
    for event in allEvents:
        if event.type == pygame.QUIT:
            RUNNING = False
    pygame.display.flip()