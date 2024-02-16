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
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"]}})
    globalVariables["clock"].tick_busy_loop(globalVariables["fps"])

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        leaveLobby(jumper)
        shutdownGame()

    if jumper.alive and not jumper.levelWon:
      drawGameAndUpdateJumperPosition(jumper)

    elif not jumper.alive:
      drawDeathScreen(jumper)

    elif jumper.levelWon:
      drawWinScreen(jumper)

    pygame.display.flip()