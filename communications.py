# What to send to server: sayingSomething: username, position (+ scroll), lobby, text status: username, status joinParty/leaveParty: username, party status: username, status
import json

from gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage
from globalVariables import globalVariables
from jumper import OtherJumpers, jumper

message = {"action":"spawnPlayer","contents":{"Username": "Player1", "playerPosition": (123, 123), "Server":10, "Status":"In game"}}
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
    return {"actions":None}

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

    elif messageReceived["action"] == "JUMP!!!":
      jumper.messageInitiatedJump()