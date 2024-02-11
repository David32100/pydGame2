# What to send to server: joinGame: Username, Position (+ scroll), lobby (lobby + level Ex. level 0 lobby 43: 430) sayingSomething: Username, position (+ scroll), lobby, text movePlayer: Username, position (+ scroll), lobby JUMP!: lobby updateStatus: username, status joinParty/leaveParty: party
from gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage

message = {"action":"spawnPlayer","payload":{"Username": "Player1", "playerPosition": (123, 123), "Server":10, "Status":"In game"}}
client = None
host, port = "127.0.0.1", 36848

def createGameClient():
  global client
  client = createUdpClient()

def sendAMessage(message):
  global client
  messageToSend = str(message).encode("utf-8")
  sendMessage(client, messageToSend, host, port)

def shutdownGameClient():
  global client
  shutDownClient(client)
  client = None

def receiveMessages():
  global client

  while True:
    try:
      messageReceived, addressReceived = receiveMessage(client)
      decodedMessageReceived = messageReceived.decode("utf-8")
      yield decodedMessageReceived
    except OSError as e:
      print("Failed to receive message:", e)
      break