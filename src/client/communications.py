import pygame
import json
import time
import sys

from client.gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage
from globalVariables import globalVariables
from game.jumper import jumper
from game.otherJumpers import OtherJumpers

client = None
host, port = "127.0.0.1", 36848
loginFailed = False

def createGameClient():
  global client
  client = createUdpClient()

def sendAMessage(message):
  global client
  messageToSend = json.dumps([message, globalVariables["username"]]).encode("utf-8")
  sendMessage(client, messageToSend, host, port)

def shutdownGameClient():
  global client
  shutDownClient(client)
  client = None

def receiveMessages():
  global client

  try:
    messageReceived, addressReceived = receiveMessage(client)
    decodedMessageReceived = json.loads(messageReceived.decode("utf-8"))
    message, sender = decodedMessageReceived

    if sender == globalVariables["username"]:
      return message, addressReceived
    else:
      return ({"actions":None}, None)
  except OSError as e:
    print("Failed to receive message:", e)
    return ({"actions":None}, None)
  
def shutdownGame():
  sendAMessage({"action":"anonymousModeOff", "contents":{"username":globalVariables["username"]}})
  
  if globalVariables["party"] != None:
    sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

  globalVariables["status"] = "Offline"
  sendAMessage({"action":"saveProgress", "contents":{"username":globalVariables["username"], "discoveredLevels":globalVariables["discoveredLevels"], "currentLevel":globalVariables["currentLevel"]}})
  sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
  sendAMessage({"action": "leaveServer", "contents":{"username":globalVariables["username"]}})
  shutdownGameClient()
  pygame.quit()
  sys.exit()

def leaveLobby(jumper):
  globalVariables["veiwingHomeScreen"] = True
  globalVariables["playingGame"] = False
  jumper.resetJumper()
  sendAMessage({"action":"leaveGame", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"]}})
  globalVariables["lobby"] = None
  globalVariables["status"] = "Not in game"
  globalVariables["playersInLobby"] = {}
  globalVariables["timers"] = {}
  
def receiveAndManageMessages():
  global globalVariables

  while True:
    messageReceived, addressReceived = receiveMessages()

    if messageReceived["action"] == "joinedLobby":
      globalVariables["lobby"] = messageReceived["contents"]["lobby"]
    elif messageReceived["action"] == "updatePlayer":
      if messageReceived["contents"]["username"] in globalVariables["playersInLobby"]:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]].updateJumper(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])
      else:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]] = OtherJumpers(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1], messageReceived["contents"]["username"])
    elif messageReceived["action"] == "deletePlayer":
      globalVariables["playersInLobby"].pop(messageReceived["contents"]["username"])
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
      time.sleep(0.5)
      globalVariables["status"] = "In game"
    elif messageReceived["action"] == "startJump":
      globalVariables['jumping'] = True
    elif messageReceived["action"] == "stopJump":
      globalVariables["jumping"] = False
    elif messageReceived["action"] == "talk":
      globalVariables["timers"][str(messageReceived["contents"]["username"]) + "'sTalkingTimer"] = [0, messageReceived["contents"]["text"]]
    elif messageReceived["action"] == "loggedIn":
      globalVariables["username"] = messageReceived["contents"]["accountInformation"]["username"]
      globalVariables["shownUsername"] = globalVariables["username"]
      globalVariables["loggingIn"] = False
      globalVariables["currentLevel"] = messageReceived["contents"]["accountInformation"]["currentLevel"]
      globalVariables["discoveredLevels"] = messageReceived["contents"]["accountInformation"]["discoveredLevels"]
      globalVariables["userSettings"] = messageReceived["contents"]["accountInformation"]["settings"]
    elif messageReceived["action"] == "loginFailed":
      loginFailed = True
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
        "shownUsername": None
      }
    elif messageReceived["action"] == "usernameChanged":
      globalVariables["username"] = messageReceived["contents"]["newUsername"]
      globalVariables["shownUsername"] = globalVariables["username"]
    elif messageReceived["action"] == "changedVisibleUsername":
      globalVariables["shownUsername"] = messageReceived["contents"]["visibleUsername"]