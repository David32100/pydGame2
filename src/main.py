# To do: Make more obstacles and levels, Add sound effects and music, Add graphics and transitions, Update credits, Polish game, Make a copy of game with uninstall game working on copy, Final step: Setup and share the new game!!!
# Shai's level: [[0, 5000, "levelLayout", 100, 100], {"Ground()0": [285, 369, 71, 55], "Enemy()1": [358, 239, 0, 0], "Enemy()2": [264, 234, 33, 10], "Enemy()3": [297, 234, 22, 186], "Ground()4": [206, 221, 46, 20], "Ground()5": [206, 225, 0, 0], "Ground()6": [81, 225, 125, 218], "Enemy()7": [339, 253, 223, 1], "Ground()8": [360, 389, 77, 37], "Ground()9": [550, 408, 414, 28], "Ground()10": [459, 413, 0, 0], "Ground()11": [449, 393, 390, 20], "Ground()12": [442, 363, 387, 30], "Enemy()13": [1128, 381, 11, 49], "Ground()14": [1121, 361, 0, 2], "Enemy()15": [1488, 391, 0, 26], "Enemy()16": [715, 375, 393, 103], "Enemy()17": [1108, 375, 32, 98], "Ground()18": [823, 347, 59, 4], "Ground()19": [891, 302, 0, 0], "Ground()20": [891, 302, 192, 72], "Enemy()21": [1217, 229, 489, 86], "Ground()22": [1128, 315, 8, 9], "Ground()23": [1136, 324, 87, 4], "Ground()24": [1071, 282, 1923, 86], "Ground()25": [989, 258, 1721, 10], "Enemy()26": [2669, 254, 8, 14], "Enemy()27": [2858, 218, 0, 14], "Ground()28": [2717, 195, 0, 0], "Ground()29": [2713, 195, 5224, 0], "Ground()30": [2713, 195, 0, 0], "Ground()31": [2713, 195, 0, 0], "Ground()32": [2713, 195, 0, 0], "Ground()33": [2713, 195, 0, 0], "Ground()34": [2721, 194, 0, 0], "Ground()35": [3023, 314, 0, 0], "Ground()36": [3023, 314, 0, 0], "Ground()37": [1225, 202, 0, 0], "Ground()38": [1225, 202, 1778, 255], "Ground()39": [3003, 391, 0, 0], "Ground()40": [3003, 391, 0, 0], "Ground()41": [3003, 391, 0, 0], "Ground()42": [3003, 391, 0, 0], "Ground()43": [3003, 391, 0, 0], "Ground()44": [3003, 391, 0, 0], "Ground()45": [3020, 180, 59, 89], "Ground()46": [2991, 49, 229, 189], "Ground()47": [3008, 242, 0, 0], "Enemy()48": [3214, 239, 0, 0], "Ground()49": [5399, 111, 48, 16], "Ground()50": [5095, 122, 0, 0], "Ground()51": [5316, 105, 0, 0]}]
import pygame
import socketio
import socketio.exceptions

from homeScreen.veiwHomeScreen import veiwHomeScreen
from client.communications import createGameClient
from game.playGame import playGame
from account.loginToAccount import loginToAccount
from globalVariables import globalVariables

pygame.init()
pygame.mixer.music.load("files/music/system-notification-199277.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()

while True:
  try:
    createGameClient()
    loginToAccount()
    pygame.mixer.music.set_volume(globalVariables["userSettings"]["volume"] / 100)
    veiwHomeScreen()
    pygame.mixer.music.play()
    playGame()
  except socketio.exceptions.ConnectionError:
    print("Could not connect to server, please check your WiFi \nError #: 5-3-5")
  except ConnectionResetError:
    print("An error occured, please contact david.gross@rkyhs.org \nError #: 15/18-5")