import pygame

screenWidth, screenHeight = 700, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

globalVariables = {
  "clock": clock,
  "screenWidth": screenWidth,
  "screenHeight": screenHeight,
  "screen": screen,
  "fps": 80,
  "currentLevel": None,
  "discoveredLevels": None,
  "username": None,
  "party": None,
  "lobby": None,
  "status": "Not in game",
  "playingGame": False,
  "veiwingHomeScreen": True,
  "loggingIn": True,
  "playersInLobby": {},
  "playersInParty": {},
  "scroll": 0,
  "jumping": False,
  "timers": {}
}