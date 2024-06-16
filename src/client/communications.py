import pygame
import sys
import threading

from client.gameClient import createClient, sendMessage, shutDownClient
from globalVariables import globalVariables
from game.jumper import jumper
from game.otherJumpers import OtherJumpers

client = None
url = "http://127.0.0.1:5000"
loginFailed = ""
changeUsernameFailed = ""
changePasswordFailed = ""
condition = threading.Condition()

def createGameClient():
  global client, url
  client = createClient()
  client.on("message", manageMessage)
  client.connect(url)

def sendAMessage(message):
  global client
  print("Sending:", message)
  sendMessage(client, message)

def shutdownGameClient():
  global client
  shutDownClient(client)
  client = None
  
def shutdownGame():
  global client

  if globalVariables["party"] != None:
    sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

  sendAMessage({"action":"anonymousModeOff", "contents":{"username":globalVariables["username"]}})
  sendAMessage({"action":"saveProgress", "contents":{"username":globalVariables["username"], "discoveredLevels":globalVariables["discoveredLevels"], "currentLevel":globalVariables["currentLevel"]}})
  sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
  globalVariables["status"] = "Offline"
  shutdownGameClient()
  pygame.quit()
  sys.exit()

def leaveLobby(jumper):
  globalVariables["veiwingHomeScreen"] = True
  sendAMessage({"action":"leaveGame", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"]}})
  globalVariables["playingGame"] = False
  jumper.resetJumper()
  globalVariables["lobby"] = None
  globalVariables["status"] = "Not in game"
  globalVariables["playersInLobby"] = {}
  globalVariables["timers"] = {}
  
def manageMessage(messageReceived):
  global globalVariables, loginFailed, changePasswordFailed, changeUsernameFailed

  if messageReceived["action"] == "joinedLobby":
    globalVariables["lobby"] = messageReceived["contents"]["lobby"]
  elif messageReceived["action"] == "updatePlayer":
    if messageReceived["contents"]["username"] in globalVariables["playersInLobby"]:
      globalVariables["playersInLobby"][messageReceived["contents"]["username"]].updateJumper(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])
    else:
      globalVariables["playersInLobby"][messageReceived["contents"]["username"]] = OtherJumpers(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1], messageReceived["contents"]["username"])
  elif messageReceived["action"] == "deletePlayer":
    globalVariables["playersInLobby"].pop(messageReceived["contents"]["username"])

    if str(messageReceived["contents"]["username"]) + "'sTalkingTimer" in globalVariables["timers"]:
      globalVariables["timers"].pop(str(messageReceived["contents"]["username"]) + "'sTalkingTimer")
      
  elif messageReceived["action"] == "updatePlayerStatus":
    if "currentLevel" in messageReceived["contents"]:
      globalVariables["playersInParty"][messageReceived["contents"]["username"]][3] = messageReceived["contents"]["currentLevel"]
    if "discoveredLevels" in messageReceived["contents"]:
      globalVariables["playersInParty"][messageReceived["contents"]["username"]][2] = messageReceived["contents"]["discoveredLevels"]
  
    globalVariables["playersInParty"][messageReceived["contents"]["username"]][1] = messageReceived["contents"]["status"]
  elif messageReceived["action"] == "partyJoined":
    globalVariables["party"] = messageReceived["contents"]["party"]
    globalVariables["playersInParty"] = messageReceived["contents"]["playersInParty"]
  elif messageReceived["action"] == "playerJoinedParty":
    globalVariables["playersInParty"] = messageReceived["contents"]["playersInParty"]
  elif messageReceived["action"] == "partyDeletePlayer":
    globalVariables["playersInParty"].pop(messageReceived["contents"]["player"][0])
  elif messageReceived["action"] == "joinGame":
    globalVariables["veiwingHomeScreen"] = False
    globalVariables["playingGame"] = True
    globalVariables["lobby"] = messageReceived["contents"]["lobby"]
    globalVariables["currentLevel"] = int(messageReceived["contents"]["lobby"].split("_")[1])
    jumper.resetJumper()
    sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"], "party":None, "lobby":messageReceived["contents"]["lobby"]}})
    globalVariables["status"] = "In game"
  elif messageReceived["action"] == "startJump":
    globalVariables['jumping'] = True
  elif messageReceived["action"] == "stopJump":
    globalVariables["jumping"] = False
  elif messageReceived["action"] == "talk":
    globalVariables["timers"][str(messageReceived["contents"]["username"]) + "'sTalkingTimer"] = [0, messageReceived["contents"]["text"]]
  elif messageReceived["action"] == "loggedIn":
    loginFailed = ""
    globalVariables["username"] = messageReceived["contents"]["accountInformation"]["username"]
    globalVariables["shownUsername"] = globalVariables["username"]
    globalVariables["loggingIn"] = False
    globalVariables["currentLevel"] = messageReceived["contents"]["accountInformation"]["currentLevel"]
    globalVariables["discoveredLevels"] = messageReceived["contents"]["accountInformation"]["discoveredLevels"]
    globalVariables["userSettings"] = messageReceived["contents"]["accountInformation"]["settings"]
  elif messageReceived["action"] == "loginFailed":
    loginFailed = messageReceived["contents"]["error"]
  elif messageReceived["action"] == "leaveServer":
    globalVariables = {
      "clock": globalVariables["clock"],
      "screenWidth": globalVariables["screenWidth"],
      "screenHeight": globalVariables["screenHeight"],
      "screen": globalVariables["screen"],
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
      "timers": {},
      "userSettings": {"volume":100, "playerColor":(0, 0, 255), "anonymous":False, "hideTextChat":False, "controls":{"jump":[pygame.K_UP, pygame.K_SPACE, pygame.K_w], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d], "talk":[pygame.K_BACKQUOTE]}},
      "shownUsername": None,
      "connectedToServer": False
    }
  elif messageReceived["action"] == "usernameChanged":
    globalVariables["username"] = messageReceived["contents"]["newUsername"]
    globalVariables["shownUsername"] = globalVariables["username"]
  elif messageReceived["action"] == "usernameChangeFailed":
    changeUsernameFailed = messageReceived["contents"]["error"]
  elif messageReceived["action"] == "passwordChangeFailed":
    changePasswordFailed = messageReceived["contents"]["error"]
  elif messageReceived["action"] == "changedVisibleUsername":
    globalVariables["shownUsername"] = messageReceived["contents"]["visibleUsername"]