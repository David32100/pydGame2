import socket
import threading

def sendMessage(socket):
  message = input("Send a message: ").encode("utf-8")
  bytesMessage = bytearray(message)
  print("Client sending message:", message)
  socket.sendall(message)
  print("Message sent. \n")

def createTCPClient(host: str, port: int):
  print("Creating client...")
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print("Created client. \nClient connecting...")
  newSocket.connect((host, port))
  print("Client connected. \n")
  return newSocket

def receiveMessage(client):
  dataReceived = client.recv(1024)
  print("Client received:", dataReceived, "\n")
  return dataReceived

def disconnectClient(client):
  print("Client disconnecting...")
  client.close()
  print("Client disconnected.")

def waitForTCPMessage(client):
  while True:
    threading.Thread(target=sendMessage, args=(client,)).start()
    dataReceived = receiveMessage(client)

    if dataReceived == b"disconnectClient":
      disconnectClient(client)
      break

host, port = "127.0.0.1", 36848
socket1 = createTCPClient(host, port)

waitForTCPMessage(socket1)