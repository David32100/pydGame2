import json

from client.gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage
from globalVariables import globalVariables
from game.jumper import jumper
from game.otherJumpers import OtherJumpers

client = None
host, port = "127.0.0.1", 36848

def createGameClient():
  global client
  client = createUdpClient()

def sendAMessage(message):
  global client
  messageToSend = json.dumps(message).encode("utf-8")
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
    return decodedMessageReceived, addressReceived
  except OSError as e:
    print("Failed to receive message:", e)
    return ({"actions":None}, None)
  
def receiveAndManageMessages():
  while True:
    messageReceived, addressReceived = receiveMessages()

    if messageReceived["action"] == "joinedLobby":
      globalVariables["lobby"] = messageReceived["contents"]["lobby"]
    elif messageReceived["action"] == "updatePlayer":
      if messageReceived["contents"]["username"] in globalVariables["playersInLobby"]:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]].updateJumper(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])
      else:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]] = OtherJumpers(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])
    elif messageReceived["action"] == "deletePlayer":
      globalVariables["playersInLobby"].pop(messageReceived["contents"]["username"])
    elif messageReceived["action"] == "updatePlayerStatus":
      globalVariables["playersInParty"][messageReceived["contents"]["username"]] = messageReceived["contents"]["status"]
    elif messageReceived["action"] == "partyJoined":
      globalVariables["party"] = messageReceived["contents"]["party"]
    elif messageReceived["action"] == "partyFull":
      print("Cannot join, party full.")
    elif messageReceived["action"] == "playerJoinedParty":
      globalVariables["playersInParty"][messageReceived["contents"]["player"][0]] = None
      sendAMessage({"action":"updateParty", "contents":{"username":globalVariables["username"], "address":tuple(messageReceived["contents"]["player"][1])}})
    elif messageReceived["action"] == "updatingParty":
      globalVariables["playersInParty"][messageReceived["contents"]["player"][0]] = None
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
      print("Updating globalVariables")
      globalVariables["username"] = messageReceived["contents"]["accountInformation"]["username"]
      globalVariables["loggingIn"] = False
      globalVariables["currentLevel"] = messageReceived["contents"]["accountInformation"]["currentLevel"]
      globalVariables["discoveredLevels"] = messageReceived["contents"]["accountInformation"]["discoveredLevels"]