import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText, leaveLobby
from homeScreen.joinGame import joinGame
from game.levels import levels
from client.communications import sendAMessage

def drawWinScreen(jumper):
  globalVariables["screen"].fill((127, 127, 0))
  writeText("arialblack", 50, "Level Complete", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 50))
  writeText("roboto", 30, "Click r to restart, space to go to next level,", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 50))
  writeText("roboto", 30, "and b + y + e to go to home screen", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 80))

  if globalVariables["currentLevel"] == globalVariables["discoveredLevels"]:
    globalVariables["discoveredLevels"] += 1
    sendAMessage({"action":"updateStatus", "contents":{"party":globalVariables["party"], "status":globalVariables["status"], "discoveredLevels":globalVariables["discoveredLevels"], "username":globalVariables["username"]}})

    if globalVariables["party"] != None:
      globalVariables["playersInParty"][globalVariables["username"]][2] = globalVariables["discoveredLevels"]

  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_r]:
    jumper.resetJumper()
  if pressedKeys[pygame.K_b] and pressedKeys[pygame.K_y] and pressedKeys[pygame.K_e]:
    jumper.resetJumper()
    leaveLobby(jumper)

    if globalVariables["currentLevel"] > globalVariables["discoveredLevels"]:
      globalVariables["currentLevel"] = globalVariables["discoveredLevels"]
      
  if pressedKeys[pygame.K_SPACE]:
    jumper.resetJumper()
    leaveLobby(jumper)

    if len(levels) > globalVariables["currentLevel"] + 1:
      globalVariables["currentLevel"] += 1
      joinGame()