import json

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
  
def receiveAndManageMessages():
  global loginFailed, globalVariables

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
      globalVariables["playersInParty"][messageReceived["contents"]["username"]][0] = messageReceived["contents"]["status"]
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
      sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"], "party":None, "lobby":messageReceived["contents"]["lobby"]}})
      globalVariables["currentLevel"] = int(messageReceived["contents"]["lobby"].split("_")[1])
      globalVariables["status"] = "In game"
    elif messageReceived["action"] == "startJump":
      globalVariables['jumping'] = True
    elif messageReceived["action"] == "stopJump":
      globalVariables["jumping"] = False
    elif messageReceived["action"] == "talk":
      globalVariables["timers"][str(messageReceived["contents"]["username"]) + "'sTalkingTimer"] = [0, messageReceived["contents"]["text"]]
    elif messageReceived["action"] == "loggedIn":
      globalVariables["username"] = messageReceived["contents"]["accountInformation"]["username"]
      globalVariables["loggingIn"] = False
      globalVariables["currentLevel"] = messageReceived["contents"]["accountInformation"]["currentLevel"]
      globalVariables["discoveredLevels"] = messageReceived["contents"]["accountInformation"]["discoveredLevels"]
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
        "timers": {}
      }