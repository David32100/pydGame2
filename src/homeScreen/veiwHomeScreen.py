import pygame

from globalVariables import globalVariables
from homeScreen.drawHomeScreen import drawHomeScreen
from drawingFunctions import shutdownGame

def veiwHomeScreen():
  while globalVariables["veiwingHomeScreen"]:
    checkMouse = False
    globalVariables["clock"].tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    drawHomeScreen(checkMouse)
    pygame.display.flip()