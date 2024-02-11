import socket

def createUdpClient():
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  return newSocket

def sendMessage(client, message: bytes, host: str, port: int):
  client.sendto(message, (host, port))

def receiveMessage(client):
  dataReceived = client.recvfrom(1024)
  return dataReceived[0], dataReceived[1]

def shutDownClient(client):
  print("Shutting down client...")

  try:
    client.shutdown(socket.SHUT_RDWR)
    client.close()
  except OSError:
    print("Client shut down.")