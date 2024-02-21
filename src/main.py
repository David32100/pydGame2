# To do: jumper.py Ln None Make message initiated jumping, homeScreen.joinParty.py Ln 45 Finish party screen (!Including statuses!), None Ln None Fix joining games with a party, None Ln None Make text chat/ability for players to talk, homeScreen.settings.py Ln 12 Make settings screen, None Ln None Make accounts and account screen, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
# Actions to send to server: talk: username, position (+ scroll), lobby, text
# NOTE: Notes light up blue, and usernames will have a max of 16 characters!!!

import pygame
import threading

from homeScreen.veiwHomeScreen import veiwHomeScreen
from savingFunctions import updateGlobalVariables
from client.communications import createGameClient, sendAMessage, receiveAndManageMessages
from game.playGame import playGame

pygame.init()
updateGlobalVariables()
createGameClient()
threading.Thread(target=receiveAndManageMessages).start()
sendAMessage({"action":"joinServer"})

while True:
  veiwHomeScreen()
  playGame()