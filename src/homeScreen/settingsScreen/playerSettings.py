import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText

playerColors = {"Grey": (125, 125, 125), "Red": (255, 0, 0), "Lime": (0, 255, 0), "Blue": (0, 0, 255), "Pink": (255, 0, 255)}

for i in range(len(playerColors)):
  if list(playerColors.values())[i] == globalVariables["userSettings"]["playerColor"]:
    playerColorsIndex = i
    break

def drawPlayerColorScreen(checkMouse, newUserSettings):
  global playerColorsIndex
  
  writeText("freesansbold.ttf", 35, "Player Color", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Choose your character's color!", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 130, 250, 80, 50))
  pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 50, 250, 80, 50))

  if checkMouse:
    if globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
      if playerColorsIndex > 0:
        playerColorsIndex -= 1
      else:
        playerColorsIndex = len(playerColors) - 1
    elif globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (2, 0, 0, 255):
      if playerColorsIndex < (len(playerColors) - 1):
        playerColorsIndex += 1
      else:
        playerColorsIndex = 0

  writeText("freesansbold.ttf", 30, "Next", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 90, 275))
  writeText("freesansbold.ttf", 30, "Back", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 90, 275))
  writeText("freesansbold.ttf", 30, str(list(playerColors.keys())[playerColorsIndex]), (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 275))
  newUserSettings["playerColor"] = list(playerColors.values())[playerColorsIndex]

def drawAnonymousModeScreen(checkMouse, newUserSettings):
  writeText("freesansbold.ttf", 35, "Anonymous mode", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Hide your username, discovered", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "levels, and current level.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    newUserSettings["anonymous"] = not newUserSettings["anonymous"]
  
  if newUserSettings["anonymous"]:
    writeText("freesansbold.ttf", 30, "On", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
  else:
    writeText("freesansbold.ttf", 30, "Off", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))

def drawHideTextChatScreen(checkMouse, newUserSettings):
  writeText("freesansbold.ttf", 35, "Hide Text Chat", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Hide the text chat.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    newUserSettings["hideTextChat"] = not newUserSettings["hideTextChat"]
  
  if newUserSettings["hideTextChat"]:
    writeText("freesansbold.ttf", 30, "Hidden", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
  else:
    writeText("freesansbold.ttf", 30, "Shown", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
