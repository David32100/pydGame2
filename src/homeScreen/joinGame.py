import time

from client.communications import sendAMessage, condition
from globalVariables import globalVariables
from game.jumper import jumper

boxColor = (255, 0, 0, 255)

def drawJoinGameBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) - 150, (globalVariables["screenHeight"] / 2) - 100, 300, 90))

def drawJoinGameText(writeText):
  writeText("freesansbold.ttf", 50, "Join Game", (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) - 65))
  writeText("freesansbold.ttf", 30, "Level: " + str(globalVariables["currentLevel"]), (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) - 35))

def joinGame(lobby:str=None):
  globalVariables["veiwingHomeScreen"] = False
  globalVariables["playingGame"] = True
  sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"], "party":globalVariables["party"], "lobby":lobby, "anonymous":globalVariables["userSettings"]["anonymous"]}})
  condition.acquire()
  condition.wait(1.5)
  l = 0

  while l < 3:
    if not condition.wait(1.5):
      sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"], "party":globalVariables["party"], "lobby":lobby, "anonymous":globalVariables["userSettings"]["anonymous"]}})
      l += 1
    else:
      break
  
  condition.release()

  if l == 3:
    globalVariables["veiwingHomeScreen"] = False
    globalVariables["loggingIn"] = True
    globalVariables["username"] = None
    globalVariables["connectedToServer"] = False

  globalVariables["status"] = "In game"
  jumper.resetJumper()

joinGameEvent = (boxColor, joinGame)