# To do: jumper.py Ln All Introduce acceleration, main.py Ln 45 Make party screen, None Ln None Make text chat, main.py Ln 47 Make settings screen, None Ln None Make accounts and account screen, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
# What to send to server: Status, text
# What to send to server: sayingSomething: username, position (+ scroll), lobby, text status: username, status joinParty/leaveParty: username, party status: username, status

import pygame
import threading
import time
import json

from globalVariables import globalVariables
from jumper import jumper
from drawingFunctions import  drawGameAndUpdateJumperPosition, drawDeathScreen, drawWinScreen, drawHomeScreen, drawSelectLevel, shutdownGame, writeText
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
      choosingParty = True
      typing = False
      code = ""
      upperKey = False
      canJoinParty = True

      while choosingParty:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            selectingLevel = False
            globalVariables["veiwingHomeScreen"] = False
            shutdownGame()
          if event.type == pygame.MOUSEBUTTONDOWN:
            checkMouse = True
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
              if len(code) > 0:
                code = code.removesuffix(code[-1])
            elif len(pygame.key.name(event.key)) < 2:
              if (len(code) + len(pygame.key.name(event.key))) < 16:
                code += event.unicode

        globalVariables["screen"].fill((0, 255, 255))
        pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) + 155, globalVariables["screenHeight"] - 100, 150, 60))
        pygame.draw.rect(globalVariables["screen"], (0, 255, 0), (45, globalVariables["screenHeight"] - 100, 150, 60))
        pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] / 2) - 140, (globalVariables["screenHeight"] / 2) - 75, 400, 50))
        pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 143, (globalVariables["screenHeight"] / 2) - 78, 406, 56), 3)
        
        if checkMouse:
          mouseX, mouseY = pygame.mouse.get_pos()

          if globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
            choosingParty = False

          if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
            if len(code) == 15 and canJoinParty:
              sendAMessage({"action":"joinParty", "contents":{"party":code, "username":globalVariables["username"]}})
              canJoinParty = False

          checkMouse = False

        writeText("freesansbold.ttf", 60, "Join Party", (0, 0, 0), (globalVariables["screenWidth"] / 2, 75))
        writeText("freesansbold.ttf", 35, "Join", (0, 0, 0), (120, globalVariables["screenHeight"] - 70))
        writeText("freesansbold.ttf", 35, "Back", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 230, globalVariables["screenHeight"] - 70))
        writeText("freesansbold.ttf", 50, "Code:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 230, (globalVariables["screenHeight"] / 2) - 50))
        writeText("freesansbold.ttf", 50, code, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 60, (globalVariables["screenHeight"] / 2) - 50))

        pygame.display.flip()


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