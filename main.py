# To do: None Ln None Make game multiplayer online, main.py Ln None Make party screen, main.py Ln None Make text chat, main.py Ln None Make settings screen and accounts, main.py Ln None Add SFX and music, main.py Ln None Add graphics and transitions, None Ln None Polish game, None Ln None Setup and share the new game!!!
# What to send to server: Username, Party, Status, while in game - position (+ scroll), lobby (lobby + level Ex. level 0 lobby 43: 430), text

import sys
import pygame

from globalVariables import globalVariables
from jumper import jumper
from systemFunctions import drawGameAndUpdateJumperPosition, drawDeathScreen, drawWinScreen, drawHomeScreen, drawSelectLevel
from communications import createGameClient, shutdownGameClient, sendAMessage

pygame.init()
createGameClient()
clock = pygame.time.Clock()

while True:
  while globalVariables["veiwingHomeScreen"]:
    checkMouse = False
    clock.tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        sendAMessage({"action":"updateStatus","contents":{"Username": "Player1", "Status":"Offline"}})
        shutdownGameClient()
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    nextScreenToDraw = drawHomeScreen(checkMouse)

    if nextScreenToDraw == "Game":
      globalVariables["veiwingHomeScreen"] = False
      globalVariables["playingGame"] = True
      sendAMessage({"action":"joinGame","contents":{"Username": "Player1", "Position":(123, 456), "lobby": 10}})
      sendAMessage({"action":"updateStatus","contents":{"Username": "Player1", "Status":"In game"}})
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
        sendAMessage({"action":"leaveGame","contents":{"Username": "Player1", "lobby":10}})
        sendAMessage({"action":"updateStatus","contents":{"Username": "Player1", "Status":"Offline"}})
        shutdownGameClient()
        pygame.quit()
        sys.exit()

    if jumper.alive and not jumper.levelWon:
      drawGameAndUpdateJumperPosition(jumper)

    elif not jumper.alive:
      drawDeathScreen(jumper)

    elif jumper.levelWon:
      drawWinScreen(jumper)

    pygame.display.flip()