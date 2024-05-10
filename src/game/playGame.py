import pygame

from game.drawDeathScreen import drawDeathScreen
from game.drawGame import drawGameAndUpdateJumperPosition
from game.drawWinScreen import drawWinScreen
from globalVariables import globalVariables
from game.jumper import jumper
from client.communications import sendAMessage, shutdownGame, leaveLobby, condition

def playGame():
  while globalVariables["playingGame"]:
    keydownEvent = None
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"], "party":globalVariables["party"], "anonymous":globalVariables["userSettings"]["anonymous"]}})
    globalVariables["clock"].tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        if globalVariables["lobby"] != None:
          sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
          condition.acquire()
          l = 0

          while l < 4:
            if not condition.wait(1):
              sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
              l += 1
            else:
              break
          
          condition.release()

          if l == 4:
            globalVariables["playingGame"] = False
            globalVariables["loggingIn"] = True
            globalVariables["username"] = None
            globalVariables["connectedToServer"] = False

        leaveLobby(jumper)
        shutdownGame()
      if event.type == pygame.KEYDOWN:
        keydownEvent = event

    if jumper.alive and not jumper.levelWon:
      drawGameAndUpdateJumperPosition(jumper, keydownEvent)

    elif not jumper.alive:
      sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
      condition.acquire()
      l = 0

      while l < 4:
        if not condition.wait(1):
          sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
          l += 1
        else:
          break
      
      condition.release()

      if l == 4:
        globalVariables["playingGame"] = False
        globalVariables["loggingIn"] = True
        globalVariables["username"] = None
        globalVariables["connectedToServer"] = False
        
      drawDeathScreen(jumper)

    elif jumper.levelWon:
      drawWinScreen(jumper)

    pygame.display.flip()