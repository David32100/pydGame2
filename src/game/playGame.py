import pygame

from game.drawDeathScreen import drawDeathScreen
from game.drawGame import drawGameAndUpdateJumperPosition
from game.drawWinScreen import drawWinScreen
from globalVariables import globalVariables
from game.jumper import jumper
from drawingFunctions import shutdownGame
from drawingFunctions import leaveLobby
from client.communications import sendAMessage

def playGame():
  while globalVariables["playingGame"]:
    keydownEvent = None
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"], "party":globalVariables["party"], "anonymous":globalVariables["userSettings"]["anonymous"]}})
    globalVariables["clock"].tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        if globalVariables["lobby"] != None:
          sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
        
        leaveLobby(jumper)
        shutdownGame()
      if event.type == pygame.KEYDOWN:
        keydownEvent = event

    if jumper.alive and not jumper.levelWon:
      drawGameAndUpdateJumperPosition(jumper, keydownEvent)

    elif not jumper.alive:
      sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
      drawDeathScreen(jumper)

    elif jumper.levelWon:
      drawWinScreen(jumper)

    pygame.display.flip()