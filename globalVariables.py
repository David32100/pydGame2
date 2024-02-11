import pygame
import ast

screenWidth, screenHeight = 700, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

savedVariables = {
  "currentLevel": 0,
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
  "lobby": 20000
}

def updateGlobalVariables():
  try:
    with open("'" + str(globalVariables["username"]) + "'GameProgress.txt", "r") as readFile:
      savedGameProgress = readFile.read()
      savedVariables = ast.literal_eval(savedGameProgress)

      for key in savedVariables:
        globalVariables[key] = savedVariables[key]

  except FileNotFoundError:
    with open("'" + str(globalVariables["username"]) + "'GameProgress.txt", "w") as writeFile:
      writeFile.write(str(savedVariables))

def updateGameProgress():
  for key in list(savedVariables.keys()):
    savedVariables[key] = globalVariables[key]

  with open("'" + str(globalVariables["username"]) + "'GameProgress.txt", "w") as writeFile:
    writeFile.write(str(savedVariables))