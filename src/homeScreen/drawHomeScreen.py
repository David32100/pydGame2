import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText
from homeScreen.joinGame import joinGameEvent, drawJoinGameBox, drawJoinGameText
from homeScreen.selectLevel import selectLevelEvent, drawSelectLevelBox, drawSelectLevelText
from homeScreen.joinParty import joinPartyEvent, drawJoinPartyBox, drawJoinPartyText
from homeScreen.settings import settingsEvent, drawSettingsBox, drawSettingsText

def drawHomeScreen(checkMouseEvent: bool):
  globalVariables["screen"].fill((0, 255, 255))
  drawJoinGameBox(pygame.draw.rect)
  drawSelectLevelBox(pygame.draw.rect)
  drawJoinPartyBox(pygame.draw.rect)
  drawSettingsBox(pygame.draw.rect)
  
  if checkMouseEvent:
    mouseX, mouseY = pygame.mouse.get_pos()
    allEvents = (joinGameEvent, selectLevelEvent, joinPartyEvent, settingsEvent)

    for event in allEvents:
      if checkColor(mouseX, mouseY) == event[0]:
        event[1]()

    checkMouseEvent = False

  writeText("freesansbold.ttf", 75, "Game Title", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 175))
  writeText("freesansbold.ttf", 30, "By: David G", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 70, (globalVariables["screenHeight"] / 2) - 145))
  drawJoinGameText(writeText)
  drawSelectLevelText(writeText)
  drawJoinPartyText(writeText)
  drawSettingsText(writeText)

def checkColor(x: float, y: float) -> tuple:
  return globalVariables["screen"].get_at((x, y))