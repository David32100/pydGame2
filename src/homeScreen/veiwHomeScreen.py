import pygame

from globalVariables import globalVariables
from homeScreen.drawHomeScreen import drawHomeScreen
from client.communications import sendAMessage, shutdownGame

def veiwHomeScreen():
  while globalVariables["veiwingHomeScreen"]:
    globalVariables["clock"].tick_busy_loop(globalVariables["fps"])
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"], "party":globalVariables["party"]}})
    checkMouse = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    drawHomeScreen(checkMouse)
    pygame.display.flip()