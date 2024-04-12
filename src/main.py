# To do: Fix talking and leaving game, Fix logout with party then shutdown server keeps player in party, Make dead players disappear, Make level maker, None Ln None Do everything else needed to do, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
import pygame
import threading

from homeScreen.veiwHomeScreen import veiwHomeScreen
from client.communications import createGameClient, receiveAndManageMessages
from game.playGame import playGame
from account.loginToAccount import loginToAccount

pygame.init()
createGameClient()
threading.Thread(target=receiveAndManageMessages).start()

while True:
  loginToAccount()
  veiwHomeScreen()
  playGame()