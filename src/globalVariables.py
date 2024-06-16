import pygame

screenWidth, screenHeight = 700, 500

globalVariables = {
  "clock": pygame.time.Clock(),
  "screenWidth": screenWidth,
  "screenHeight": screenHeight,
  "screen": pygame.display.set_mode((screenWidth, screenHeight)),
  "fps": 80,
  "currentLevel": None,
  "discoveredLevels": None,
  "username": None,
  "party": None,
  "lobby": None,
  "status": "Not in game",
  "playingGame": False,
  "veiwingHomeScreen": False,
  "loggingIn": True,
  "playersInLobby": {},
  "playersInParty": {},
  "scroll": 0,
  "jumping": False,
  "timers": {},
  "userSettings": {"volume":100, "playerColor":(0, 0, 255), "anonymous":False, "hideTextChat":False, "controls":{"jump":[pygame.K_UP, pygame.K_SPACE, pygame.K_w], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d], "talk":[pygame.K_BACKQUOTE]}},
  "shownUsername": None
}