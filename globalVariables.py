import pygame

screenWidth, screenHeight = 700, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

savedVariables = {
  "currentLevel": 10,
  "discoveredLevels": 10,
  "username": "The best player"
}

globalVariables = {
  "screenWidth": screenWidth,
  "screenHeight": screenHeight,
  "screen": screen,
  "fps": 80,
  "groundColor": (125, 125, 0, 255),
  "goalColor": (0, 255, 0, 255),
  "scroll": 0,
  "currentLevel": savedVariables["currentLevel"],
  "playingGame": False,
  "veiwingHomeScreen": True,
  "discoveredLevels": savedVariables["discoveredLevels"],
  "party": 0,
  "username": savedVariables["username"],
  "lobby": None,
  "status": "Not in game",
  "playersInLobby": {}
}