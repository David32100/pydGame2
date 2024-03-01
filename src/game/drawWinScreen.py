import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText, leaveLobby

def drawWinScreen(jumper):
  globalVariables["screen"].fill((127, 127, 0))
  writeText("arialblack", 50, "Level Complete", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 50))
  writeText("roboto", 30, "Click r to restart and b + y + e to go to home screen", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 50))

  if globalVariables["currentLevel"] == globalVariables["discoveredLevels"]:
    globalVariables["discoveredLevels"] += 1

  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_r]:
    jumper.resetJumper()
  if pressedKeys[pygame.K_b] and pressedKeys[pygame.K_y] and pressedKeys[pygame.K_e]:
    jumper.resetJumper()
    leaveLobby(jumper)