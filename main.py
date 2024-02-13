# To do: jumper.py Ln 89-128 Fix and improve jumping, main.py Ln 45 Make party screen, None Ln None Make text chat, main.py Ln 47 Make settings screen, None Ln None Make accounts and account screen, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
# What to send to server: Status, text

import pygame
import threading
import time

from globalVariables import globalVariables
from jumper import jumper
from drawingFunctions import  drawGameAndUpdateJumperPosition, drawDeathScreen, drawWinScreen, drawHomeScreen, drawSelectLevel, shutdownGame
from savingFunctions import updateGlobalVariables
from communications import createGameClient, sendAMessage, receiveAndManageMessages

updateGlobalVariables()
createGameClient()
threading.Thread(target=receiveAndManageMessages).start()
pygame.init()

sendAMessage({"action":"joinServer"})
clock = pygame.time.Clock()

while True:
  while globalVariables["veiwingHomeScreen"]:
    checkMouse = False
    clock.tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    nextScreenToDraw = drawHomeScreen(checkMouse)

    if nextScreenToDraw == "Game":
      globalVariables["veiwingHomeScreen"] = False
      globalVariables["playingGame"] = True
      sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"]}})
      time.sleep(0.5)
      globalVariables["status"] = "In game"
    elif nextScreenToDraw == "Level":
      drawSelectLevel()
    elif nextScreenToDraw == "Party":
      print("Party: WIP")
    elif nextScreenToDraw == "Settings":
      print("Settings: WIP")

    pygame.display.flip()

  while globalVariables["playingGame"]:
    clock.tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["playingGame"] = False
        sendAMessage({"action":"leaveGame","contents":{"username": globalVariables["username"], "lobby":globalVariables["lobby"]}})
        shutdownGame()

    if jumper.alive and not jumper.levelWon:
      drawGameAndUpdateJumperPosition(jumper)

    elif not jumper.alive:
      drawDeathScreen(jumper)

    elif jumper.levelWon:
      drawWinScreen(jumper)

    pygame.display.flip()