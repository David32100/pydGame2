import pygame

screenWidth, screenHeight = 700, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

savedVariables = {
  "currentLevel": 10,
  "discoveredLevels": 10,
  "username": "The best player"
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
  "playersInLobby": {},
  "playersInParty": [],
  "scroll": 0
}