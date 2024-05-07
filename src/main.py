# To do: Make more obstacles and levels, Add SFX and music, Add graphics and transitions, Update credits, Add conection system (check if still connected to internet, check for responses), Polish game, Make a copy of game and make uninstall game work on copy, Final step: Setup and share the new game!!!
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