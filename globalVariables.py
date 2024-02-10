import pygame

screenWidth, screenHeight = 700, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

globalVariables = {
  "screenWidth": screenWidth,
  "screenHeight": screenHeight,
  "screen": screen,
  "fps": 80,
  "groundColor": (125, 125, 0, 255),
  "goalColor": (0, 255, 0, 255),
  "scroll": 0,
  "currentLevel": 0,
  "playingGame": False,
  "veiwingHomeScreen": True,
  "discoveredLevels": 10,
  "party": 0
}