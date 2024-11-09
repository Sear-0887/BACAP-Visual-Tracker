

import typing
import pygame
import re
from config import *
from utils import convertRGBStrToTuple

pygame.font.init()
font = pygame.font.Font(FONTNAME, 16)

LEFTCLICK = 1
MIDDLECLICK = 2
RIGHTCLICK = 3
SCROLLUP = 4
SCROLLDOWN = 5

cbType = typing.Callable[..., typing.Any]

def emptyFunc(): return

def displayText(text: str, color: RGBTuple, background: RGBTuple | None = None) -> pygame.Surface:
    return font.render(text, True, color, background)

def displayJSONText(textObj: JSONTextType) -> pygame.Surface:
    allTextObj = [textObj] + textObj.get("extra", [])
    textBuffer = pygame.surface.Surface((2000, 2000)).convert_alpha()
    maxw, maxh = 0, 0
    curx, cury = 0, 0
    for textObj in allTextObj:
        textColor: RGBTuple = COLOR["white"]
        objcolor = textObj.get("color", "white")
        if objcolor.startswith("#"): 
            textColor = convertRGBStrToTuple(objcolor)
        else:
            if objcolor not in ColorKeys: continue
            textColor = COLOR.get(objcolor, COLOR["white"])
        
        textT = textObj.get("translate", textObj.get("text", ""))
        textS = displayText(textT.replace("\n", ""), textColor)
        textBuffer.blit(textS, (curx, cury))
        cury += textS.get_height() * textT.count("\n")
        curx += textS.get_width()
        if textT.count("\n") > 0: curx = 0
        maxw, maxh = max(maxw, curx), max(maxh, cury + textS.get_height())
    result = pygame.Surface((maxw, maxh))
    result.blit(textBuffer, (0, 0))
    return result

class GuiElement:
    def __init__(self, id_: str, coord: Vector2, text: str="", callback: cbType = emptyFunc):
        self.id: str = id_
        self.coord: Vector2 = coord
        self.text: str = text
        self.callback: cbType = callback
        allGuiElements.append(self)
    
    @staticmethod
    def getElementById(query: str): # -> GuiElement 
        for element in allGuiElements:
            if element.id == query:
                return element
        raise ValueError(f"Cannot find element from query {query}.")
        
    @staticmethod
    def getElementExist(query: str) -> bool:
        for element in allGuiElements:
            if element.id == query:
                return True
        return False

    @staticmethod   
    def getAllGuiElement(): # -> typing.List[GuiElement]
        return allGuiElements
    
    def getProperties(self):
        return vars(self)
    
    def getProperty(self, key: str): # This has the same effect as self.key
        return self.getProperties()[key]
    
    @staticmethod
    def deleteGuiElementById(query: str) -> None:
        global allGuiElements
        allGuiElements = list(filter(lambda element: not re.match(query, element.id), allGuiElements))

    def __getitem__(self, index: str):
        return self.getProperty(index)
    
    def handle_event(self, event: pygame.event.Event):
        pass
    
    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass

allGuiElements: typing.List[GuiElement] = []

class InputBox(GuiElement):
    def __init__(self, id_: str, coord: Vector2, dim: Vector2, placeholder: str, callback: cbType):
        super().__init__(id_, coord, "", callback)
        self.active = False
        self.placeholder = placeholder
        self.color = COLOR["gray"]
        self.rect = pygame.Rect(coord[0], coord[1], dim[0], dim[1])
        self.textSurface = font.render("", True, self.color)
        self.textRect = self.textSurface.get_rect()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFTCLICK:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.callback(self)
                    self.text = ""
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.textSurface = font.render(self.text, True, self.color)
        if self.text == "":
            self.textSurface = font.render(self.placeholder, True, (128, 128, 128))

    def update(self):
        self.rect.w = max(200, self.textSurface.get_width()+10)

    def draw(self, screen: pygame.Surface):
        self.color = COLOR["white"] if self.active else COLOR["gray"]
        screen.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button(GuiElement):
    def __init__(self, id_: str, coord: Vector2, dim: Vector2, text: str, callback: cbType):
        super().__init__(id_, coord, text, callback)
        self.rect: pygame.Rect = pygame.Rect(coord[0], coord[1], dim[0], dim[1])
        self.textSurface: pygame.Surface = displayText(self.text, COLOR["white"])
        
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFTCLICK:
            if not self.rect.collidepoint(event.pos): return
            self.callback(self)
        
    def update(self):
        width = self.textSurface.get_width()+10
        self.rect.w = width

    def draw(self, screen: pygame.Surface):
        self.textRect = self.textSurface.get_rect()
        dest = (
          self.rect.x + max(0, (self.rect.w - self.textRect.w) // 2), 
          self.rect.y + max(0, (self.rect.h - self.textRect.h) // 2)
        )
        screen.blit(self.textSurface, dest)
        pygame.draw.rect(screen, COLOR["gray"], self.rect, 2)

class Text(GuiElement):
    def __init__(self, id_: str, coord: Vector2, text: str, color: RGBTuple=COLOR["white"]):
        super().__init__(id_, coord, text)
        self.color = color
        self.textSurface = displayText(self.text,self.color)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.textSurface, self.coord)

class JSONText(GuiElement):
    def __init__(self, id_: str, coord: Vector2, textJSON: JSONTextType):
        super().__init__(id_, coord)
        self.textJSON = textJSON
        self.textSurface = displayJSONText(self.textJSON)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.textSurface, self.coord)

class RectBox(GuiElement):
    def __init__(self, id_: str, coord: Vector2, dim: Vector2, color: RGBTuple=COLOR["white"]):
        super().__init__(id_, coord)
        self.rect = pygame.Rect(coord[0], coord[1], dim[0], dim[1])
        self.color = color

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, COLOR["gray"], self.rect, 2)

class CheckBox(GuiElement):
    def __init__(self, id_: str, coord: Vector2, dim: Vector2, callback: cbType):
        super().__init__(id_, coord, "", callback)
        self.checked = False
        self.rect = pygame.Rect(coord[0], coord[1], dim[0], dim[1])
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFTCLICK:
            if not self.rect.collidepoint(event.pos): return
            self.checked = not self.checked
            self.callback(self)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLOR["green"] if self.checked else COLOR["red"], self.rect)
        pygame.draw.rect(screen, COLOR["gray"], self.rect, 2)

class SelectionBox(Button):
    def __init__(
            self, id_: str, 
            coord: Vector2, dim: Vector2, 
            selection: typing.List[str], 
            callback: cbType = emptyFunc, 
            initalIndex: int = 0,
            setInstant: bool = True
        ):
        super().__init__(id_, coord, dim, selection[0], callback)
        self.selection = selection
        self.selectedIndex = initalIndex
        self.text = self.selection[self.selectedIndex]
        self.textSurface: pygame.Surface = displayText(self.text, COLOR["white"])
        self.setInstant = setInstant
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos): return
            if event.button == SCROLLUP:
                self.selectedIndex = max(0, self.selectedIndex-1)
                # print(self.selectedIndex)
                if self.setInstant: self.callback(self)
            elif event.button == SCROLLDOWN:
                self.selectedIndex = min(self.selectedIndex + 1, len(self.selection)-1)
                # print(self.selectedIndex)
                if self.setInstant: self.callback(self)
            elif event.button == LEFTCLICK:
                self.callback(self)

    def update(self):
        super().update()
        self.text = "↓" if self.selectedIndex == 0 else ("↑" if self.selectedIndex == len(self.selection)-1 else "↕")
        self.text += self.selection[self.selectedIndex]
        self.textSurface = displayText(self.text, COLOR["white"])
        