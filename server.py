import socket
import threading

def createTCPServer(host: str, port: int):
  print("Creating server...")
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  newSocket.bind((host, port))
  print("Server created! \n")
  newSocket.listen()
  print("Searching for connection...")
  return newSocket

def disconnectServer(server, connections):
  print("Server disconnecting...")
  print("Disconnecting clients")
  for connection in connections:
    sendMessage(connection, b"disconnectClient")
    connection.close()

  print("Clients disconnected.")
  server.shutdown(socket.SHUT_RDWR)
  server.close()
  print("Server disconnected. \n")

def receiveMessage(connection):
  dataReceived = connection.recv(1024)
  print("Server received:", dataReceived)
  return dataReceived

def sendMessage(connection, message: bytes):
  print("Server sending:", message, "\n")
  connection.sendall(message)

def waitForTCPMessage(server, connection, connections):
  with connection:
    while True:
      dataReceived = receiveMessage(connection)

      if dataReceived == b"7":
        sendMessage(connection, dataReceived)
      elif dataReceived == b"disconnectClient":
        sendMessage(connection, dataReceived)
        connections.remove(connection)
        break
      elif dataReceived == b"disconnectServer":
        if len(connections) > 1:
          sendMessage(connection, b"Cannot disconnect server: Too many clients connected")
        else:
          disconnectServer(server, connections)
          break
      elif dataReceived == b"Hi":
        sendMessage(connections[0], b"Hi")
        sendMessage(connection, b"Sent 'Hi' to connection 1")
      else:
        sendMessage(connection, b"Rejected")

connections = []
addressInfo = {}
host, port = "127.0.0.1", 36848
socket1 = createTCPServer(host, port)

try:
  while True:
    connection, address = socket1.accept()
    connections.append(connection)
    addressInfo[address] = ["Lobby 10", "Pos (3000, 40)"]
    print("Client connected!")
    print("Connected through:", address, "\n")
    threading.Thread(target=waitForTCPMessage, args=(socket1, connection, connections)).start()
except OSError:
  print("Server fully disconnected. It may take a while for the address to become available again.")