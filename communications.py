# What to send to server: joinGame: Username, Position (+ scroll), lobby (lobby + level Ex. level 0 lobby 43: 430) sayingSomething: Username, position (+ scroll), lobby, text movePlayer: Username, position (+ scroll), lobby JUMP!: lobby updateStatus: username, status joinParty/leaveParty: party
from gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage

message = {"action":"spawnPlayer","payload":{"Username": "Player1", "playerPosition": (123, 123), "Server":10, "Status":"In game"}}
client = None
host, port = "127.0.0.1", 36848

def createGameClient():
  global client
  client = createUdpClient()

def sendAMessage(message):
  messageToSend = str(message).encode("utf-8")
  sendMessage(client, messageToSend, host, port)

def shutdownGameClient():
  shutDownClient(client)

def receiveAMessage():
  messageReceived, addressReceived = receiveMessage(client)
  decodedMessageReceived = eval(messageReceived)
  return decodedMessageReceived