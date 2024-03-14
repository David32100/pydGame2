# To do: None Ln None Finish making settings work, None Ln None Do everything else needed to do, None Ln None Add SFX and music, None Ln None Add graphics and transitions, None Ln None Polish game, Final step: Setup and share the new game!!!
import pygame
import threading

from homeScreen.veiwHomeScreen import veiwHomeScreen
from client.communications import createGameClient, receiveAndManageMessages
from game.playGame import playGame
from account.loginToAccount import loginToAccount
from homeScreen.settingsScreen.settings import sendEmail
# To test when I have WIFIFIFIFI
#sendEmail("The subject", "You ra mom ma")

pygame.init()
createGameClient()
threading.Thread(target=receiveAndManageMessages).start()

while True:
  loginToAccount()
  veiwHomeScreen()
  playGame()