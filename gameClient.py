import socket
import threading
import time

from globalVariables import globalVariables
from jumper import jumper

def createUdpClient():
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  return newSocket

def sendMessage(client, message: bytes, host: str, port: int):
  client.sendto(message, (host, port))

def receiveMessage(client):
  dataReceived = client.recvfrom(1024)
  return dataReceived[0], dataReceived[1]

def askToStopServer(client):
  while not globalVariables["killClient"]:
    time.sleep(1)

  shutDownClient(client)

def shutDownClient(client):
  print("Shutting down client...")
  client.shutdown(socket.SHUT_RDWR)
  client.close()

def sendAndReceiveMessages(client, host, port):
  while True:
      messageToSend = str([globalVariables["party"], jumper.jumperXWithScroll, jumper.jumperY]).encode("utf-8")
      sendMessage(client, messageToSend, host, port)
      messageReceived, addressReceived = receiveMessage(client)
      time.sleep(0.1)

def manageGameClient():
  host, port = "127.0.0.1", 36848
  socket1 = createUdpClient()
  threading.Thread(target=askToStopServer, args=(socket1,)).start()

  try:
    sendAndReceiveMessages(socket1, host, port)
  except:
    try:
      shutDownClient(socket1)
    except:
      print("Error occured: Client doesn't exist.")

    time.sleep(0.1)
    print("Client shut down.")