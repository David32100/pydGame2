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
  messageReceived, addressReceived = server.recvfrom(1024)
  decodedMessageReceived = eval(messageReceived.decode("utf-8"))
  print("Received message:", messageReceived, "From:", addressReceived)
  return decodedMessageReceived, addressReceived

def sendMessage(server, message: bytes, address):
  print("Sending message:", message, "To:", address)
  server.sendto(message, address)

def askToStopServer(server):
  stop = input("Stop Server (Y): \n")

  while stop != "Y":
    stop = input("Stop Server (Y): \n")

  print("Shutting down server...")
  server.shutdown(socket.SHUT_RDWR)
  server.close()

def manageGameServer():
  host, port = "127.0.0.1", 36848
  socket1 = createUdpServer(host, port)
  threading.Thread(target=askToStopServer, args=(socket1,)).start()

  try:
    while True:
      messageReceived, addressReceived = receiveMessage(socket1)

      if messageReceived[0] != 0:
        sendMessage(socket1, [messageReceived[1], messageReceived[2]].encode("utf-8"), addressReceived)
      else:
        sendMessage(socket1, b"Hi", addressReceived)
  except OSError as e:
    print(e)

    try:
      socket1.shutdown(socket.SHUT_RDWR)
      socket1.close()
    except:
      print("Error occured: Server doesn't exist.")
    
    time.sleep(1)
    print("Server shut down.")

manageGameServer()