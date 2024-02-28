import pygame

screenWidth, screenHeight = 700, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

savedVariables = {
  "currentLevel": 0,
  "discoveredLevels": 0,
  "username": None
}

globalVariables = {
  "clock": clock,
  "screenWidth": screenWidth,
  "screenHeight": screenHeight,
  "screen": screen,
  "fps": 80,
  "currentLevel": savedVariables["currentLevel"],
  "discoveredLevels": savedVariables["discoveredLevels"],
  "username": savedVariables["username"],
  "party": None,
  "lobby": None,
  "status": "Not in game",
  "playingGame": False,
  "veiwingHomeScreen": True,
  "loggingIn": True,
  "playersInLobby": {},
  "playersInParty": {savedVariables["username"]:"Not in game"},
  "scroll": 0,
  "jumping": False,
  "timers": {}
}