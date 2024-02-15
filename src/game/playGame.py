import pygame

from game.drawDeathScreen import drawDeathScreen
from game.drawGame import drawGameAndUpdateJumperPosition
from game.drawWinScreen import drawWinScreen
from globalVariables import globalVariables
from game.jumper import jumper
from drawingFunctions import shutdownGame
from drawingFunctions import leaveLobby

def playGame():
  while globalVariables["playingGame"]:
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