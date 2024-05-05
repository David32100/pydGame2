# To do: Make error messages for change username and password, Make game title and update report and credits, Make more obstacles and levels, Add SFX and music, Add graphics and transitions, Polish game, Make a copy of game and make uninstall game work on copy, Final step: Setup and share the new game!!!
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