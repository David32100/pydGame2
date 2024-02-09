import socket
import threading
import time

def createUdpServer(host: str, port: int):
  print("Creating server...")
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  newSocket.bind((host, port))
  print("Server created.")
  return newSocket

def receiveMessage(server):
  dataReceived = server.recvfrom(1024)
  messageReceived = dataReceived[0]
  addressReceived = dataReceived[1]
  print("Received message:", messageReceived, "From:", addressReceived)
  return messageReceived, addressReceived

def sendMessage(server, message: bytes, address):
  print("Sending message:", message, "To:", address)
  server.sendto(message, address)

def askToStopServer(server):
  stop = input("Stop Server (Y):")

  while stop != "Y":
    stop = input("Stop Server (Y):")

  print("Shutting down server...")
  server.shutdown(socket.SHUT_RDWR)
  server.close()

host, port = "127.0.0.1", 36848
socket1 = createUdpServer(host, port)
threading.Thread(target=askToStopServer, args=(socket1,)).start()

try:
  while True:
    messageReceived, addressReceived = receiveMessage(socket1)
    sendMessage(socket1, b"Hi", addressReceived)
except:
  time.sleep(1)
  print("Server shut down.")