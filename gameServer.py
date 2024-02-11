import socket
import threading
import time
import json

def createUdpServer(host: str, port: int):
  print("Creating server...")
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  newSocket.bind((host, port))
  print("Server created.")
  return newSocket

def receiveMessage(server):
  messageReceived, addressReceived = server.recvfrom(1024)
  decodedMessageReceived = json.loads(messageReceived.decode("utf-8"))
  print("Received message:", decodedMessageReceived, "From:", addressReceived)
  return decodedMessageReceived, addressReceived

def sendMessage(server, message: bytes, address):
  print("Sending message:", message, "To:", address)
  server.sendto(message, address)

def askToStopServer(server):
  stop = input("Stop Server (Y): \n")

  while stop != "Y":
    stop = input("Stop Server (Y): \n")

  shutDownServer(server)  

def shutDownServer(server):
  print("Shutting down server...")
  server.shutdown(socket.SHUT_RDWR)
  server.close()

def runServer(server):
  playerAddresses = []

  while True:
      messageReceived, addressReceived = receiveMessage(server)

      if messageReceived["action"] == "joinServer":
        playerAddresses.append(addressReceived)

      if messageReceived["action"] == "updateStatus" and messageReceived["contents"]["status"] == "Offline":
        playerAddresses.remove(addressReceived)

      print(playerAddresses)

def manageGameServer():
  host, port = "127.0.0.1", 36848
  socket1 = createUdpServer(host, port)
  threading.Thread(target=askToStopServer, args=(socket1,)).start()

  try:
    runServer(socket1)
  except OSError as e:
    print(e)

    try:
      shutDownServer(socket1)
    except:
      print("Error occured: Server doesn't exist.")
    
    time.sleep(1)
    print("Server shut down.")

manageGameServer()