import json
import pygame

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
  jumping = False

  while True:
    messageReceived, addressReceived = receiveMessages()

    if messageReceived["action"] == "joinedLobby":
      globalVariables["lobby"] = messageReceived["contents"]["lobby"]

    elif messageReceived["action"] == "updatePlayer":
      if messageReceived["contents"]["username"] in globalVariables["playersInLobby"]:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]].updateJumper(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])
      else:
        print("New player:", globalVariables["playersInParty"])
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]] = OtherJumpers(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])

    elif messageReceived["action"] == "deletePlayer":
      globalVariables["playersInLobby"].pop(messageReceived["contents"]["username"])

    elif messageReceived["action"] == "partyJoined":
      globalVariables["party"] = messageReceived["contents"]["party"]

    elif messageReceived["action"] == "partyFull":
      print("Cannot join, party full.")
    
    elif messageReceived["action"] == "playerJoinedParty":
      globalVariables["playersInParty"].append(messageReceived["contents"]["player"][0])
      sendAMessage({"action":"updateParty", "contents":{"username":globalVariables["username"], "address":tuple(messageReceived["contents"]["player"][1])}})

    elif messageReceived["action"] == "updatingParty":
      globalVariables["playersInParty"].append(messageReceived["contents"]["player"][0])

    elif messageReceived["action"] == "partyDeletePlayer":
      globalVariables["playersInParty"].remove(messageReceived["contents"]["player"][0])

    elif messageReceived["action"] == "joinGame":
      globalVariables["veiwingHomeScreen"] = False
      globalVariables["playingGame"] = True
      globalVariables["lobby"] = messageReceived["contents"]["lobby"]
      sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"], "party":None, "lobby":messageReceived["contents"]["lobby"]}})
      globalVariables["status"] = "In game"
    
    elif messageReceived["action"] == "startJump":
      print("START THE JUMP!!!")
      jumping = True

    elif messageReceived["action"] == "stopJump":
      print("STOP THE JUMP!!!")
      jumper.stopJumping()
      jumping = False

    if jumping:
      jumper.jump()
      pressedKeys = pygame.key.get_pressed()

      if not pressedKeys[pygame.K_RIGHT] and not pressedKeys[pygame.K_LEFT]:
        jumper.moveRight()