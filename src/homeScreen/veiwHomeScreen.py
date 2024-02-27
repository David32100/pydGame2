import pygame

from globalVariables import globalVariables
from homeScreen.drawHomeScreen import drawHomeScreen
from drawingFunctions import shutdownGame
from client.communications import sendAMessage

def veiwHomeScreen():
  while globalVariables["veiwingHomeScreen"]:
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"], "party":globalVariables["party"]}})
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