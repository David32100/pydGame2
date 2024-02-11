# To do: None Ln None Make game multiplayer online, main.py Ln None Make party screen, main.py Ln None Make text chat, main.py Ln None Make settings screen and accounts, main.py Ln None Add SFX and music, main.py Ln None Add graphics and transitions, None Ln None Polish game, None Ln None Setup and share the new game!!!
# What to send to server: Username, Party, Status, while in game - position (+ scroll), lobby (lobby + level Ex. level 0 lobby 43: 430), text

import pygame
import threading

from globalVariables import globalVariables, updateGlobalVariables
from jumper import jumper
from systemFunctions import drawGameAndUpdateJumperPosition, drawDeathScreen, drawWinScreen, drawHomeScreen, drawSelectLevel, shutdownGame
from communications import createGameClient, sendAMessage, receiveMessages

updateGlobalVariables()
pygame.init()
createGameClient()
threading.Thread(target=receiveMessages).start()

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
      sendAMessage({"action":"joinGame","contents":{"Username": globalVariables["username"], "Position":(jumper.jumperXWithScroll, jumper.jumperY), "lobby": globalVariables["lobby"]}})
      sendAMessage({"action":"updateStatus","contents":{"Username": globalVariables["username"], "Status":"In game"}})
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
        sendAMessage({"action":"leaveGame","contents":{"Username": globalVariables["username"], "lobby":globalVariables["lobby"]}})
        shutdownGame()

    if jumper.alive and not jumper.levelWon:
      drawGameAndUpdateJumperPosition(jumper)

    elif not jumper.alive:
      drawDeathScreen(jumper)

    elif jumper.levelWon:
      drawWinScreen(jumper)

    pygame.display.flip()