# To do: gameServer Ln 64-180 Change server to know which device talking to it, homeScreen.settings.py Ln 12 Make settings screen (In General, Player, Account, Controlls: keybinds, account, player color, delete data, delete account, reset settings, volume, uninstall game, credits, report, etc), None Ln None Do everything else needed to do, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
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