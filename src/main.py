# To do: gameServer.py Ln None Move save files into server, homeScreen.joinParty.py Ln 45 Finish party screen (selecting player: username, status, discovered levels, kick {username}), None Ln None Make accounts and account screen (usernames will have a maximum of 16 characters), homeScreen.settings.py Ln 12 Make settings screen (In General, Player, Account, Controlls: keybinds, account, player color, delete data, delete account, reset settings, volume, uninstall game, credits, report, etc), None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!

import pygame
import threading

from homeScreen.veiwHomeScreen import veiwHomeScreen
from savingFunctions import updateGlobalVariables
from client.communications import createGameClient, sendAMessage, receiveAndManageMessages
from game.playGame import playGame
from account.login import login
from globalVariables import globalVariables

pygame.init()
createGameClient()
threading.Thread(target=receiveAndManageMessages).start()

updateGlobalVariables()
sendAMessage({"action":"joinServer"})

while True:
  while globalVariables["loggingIn"]:
    print("signUp()")

    if globalVariables["loggingIn"]:
      login()
  
  veiwHomeScreen()
  playGame()