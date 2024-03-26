import socket

def createUdpClient() -> socket.socket:
  return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendMessage(client: socket.socket, message: bytes, host: str, port: int):
  client.sendto(message, (host, port))

def receiveMessage(client: socket.socket):
  dataReceived = client.recvfrom(1024)
  return dataReceived[0], dataReceived[1]

def shutDownClient(client: socket.socket):
  print("Shutting down client...")

  try:
    client.shutdown(socket.SHUT_RDWR)
    client.close()
  except OSError:
    print("Client shut down with error.")
  else:
    print("Client shut down.")