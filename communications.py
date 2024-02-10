from gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage

message = {"action":"","payload":{}}
client = None
host, port = "127.0.0.1", 36848

def createGameClient():
  global client
  client = createUdpClient()

def sendAMessage(message):
  sendMessage(client, message, host, port)

def shutdownGameClient():
  shutDownClient(client)

def receiveAMessage():
  messageReceived, addressReceived = receiveMessage(client)
  decodedMessageReceived = eval(messageReceived)
  return decodedMessageReceived