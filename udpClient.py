import socket
import threading
import time

def createUdpClient():
  print("Creating client...")
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  print("Client created.")
  return newSocket

def sendMessage(client, message: bytes, host: str, port: int):
  print("Sending message:", message, "To:", (host, port))
  client.sendto(message, (host, port))

def receiveMessage(client):
  dataReceived = client.recvfrom(1024)
  messageReceived = dataReceived[0]
  addressReceived = dataReceived[1]
  print("Received message:", messageReceived, "From:", addressReceived)
  return messageReceived, addressReceived

def askToStopServer(client):
  stop = input("Stop Server (Y):")

  while stop != "Y":
    stop = input("Stop Server (Y):")

  print("Shutting down client")
  client.shutdown(socket.SHUT_RDWR)
  client.close()

host, port = "127.0.0.1", 36848
socket1 = createUdpClient()
threading.Thread(target=askToStopServer, args=(socket1,)).start()

try:
  while True:
    sendMessage(socket1, b"Hi", host, port)
    messageReceived, addressReceived = receiveMessage(socket1)
except:
  time.sleep(1)
  print("Client shut down.")