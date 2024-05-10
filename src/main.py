# To do: Make more obstacles and levels, Finish conection system (gameServer.py), Add sound effects and music, Add graphics and transitions, Update credits, Polish game, Make a copy of game and make uninstall game work on copy, Final step: Setup and share the new game!!!
import pygame
import threading

from homeScreen.veiwHomeScreen import veiwHomeScreen
from client.communications import createGameClient, receiveAndManageMessages
from game.playGame import playGame
from account.loginToAccount import loginToAccount
from globalVariables import globalVariables

pygame.init()
createGameClient()
threading.Thread(target=receiveAndManageMessages).start()

pygame.mixer.music.load("files/music/system-notification-199277.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()

while True:
  loginToAccount()
  pygame.mixer.music.set_volume(globalVariables["userSettings"]["volume"] / 100)
  veiwHomeScreen()
  pygame.mixer.music.play()
  playGame()