# To do: jumper.py Ln All Introduce acceleration for jumping and falling, jumper.py Ln 112 Fix message initiated jummping main.py Ln 45 Finish party screen, None Ln None None Fix joining games with a party, Ln None Make text chat/ability for players to talk, main.py Ln 47 Make settings screen, None Ln None Make accounts and account screen, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
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