import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText, leaveLobby

def drawDeathScreen(jumper):
  globalVariables["screen"].fill((255, 0, 0))
  writeText("arialblack", 50, "Game Over", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 50))
  writeText("roboto", 25, "Click Space to restart and b + y + e to go to home screen", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 50))

  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_SPACE]:
    jumper.resetJumper()
  elif pressedKeys[pygame.K_b] and pressedKeys[pygame.K_y] and pressedKeys[pygame.K_e]:
    jumper.resetJumper()
    leaveLobby(jumper)