# What to send to server: joinGame: Username, Position (+ scroll), lobby (lobby + level Ex. level 0 lobby 43: 430) sayingSomething: Username, position (+ scroll), lobby, text movePlayer: Username, position (+ scroll), lobby JUMP!: lobby updateStatus: username, status joinParty/leaveParty: party
import json

from gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage
from globalVariables import globalVariables

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