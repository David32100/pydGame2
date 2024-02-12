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
  lobbies = {}

  while True:
    messageReceived, addressReceived = receiveMessage(server)
    print("Received message:", messageReceived, "From:", addressReceived)

    if messageReceived["action"] == "joinServer":
      playerAddresses.append(addressReceived)
      
    if messageReceived["action"] == "joinGame":
      searchingForLobby = True
      i = 1
      
      while searchingForLobby:
        if not (str(i) + "_" + str(messageReceived["contents"]["currentLevel"])) in lobbies:
          lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])] = {messageReceived["contents"]["username"]:addressReceived}
          searchingForLobby = False
        else:
          if len(lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])]) < 8:
            lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])][messageReceived["contents"]["username"]] = addressReceived
            searchingForLobby = False
          else:
            i += 1
      
      for player in list(lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])].values()):
        if player != addressReceived:
          sendMessage(server, json.dumps({"action":"updatePlayer", "contents": messageReceived["contents"]}).encode("utf-8"), player)
        else:
          sendMessage(server, json.dumps({"action":"joinedLobby", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}).encode("utf-8"), player)

    if messageReceived["action"] == "leaveGame":
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, json.dumps({"action":"deletePlayer", "contents":messageReceived["contents"]}).encode("utf-8"), player)

      lobbies[messageReceived["contents"]["lobby"]].pop(messageReceived["contents"]["username"])
      time.sleep(0.1)

    if messageReceived["action"] == "leaveServer":
      playerAddresses.remove(addressReceived)

    if messageReceived["action"] == "updatePlayer":
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, json.dumps({"action":messageReceived["action"], "contents":messageReceived["contents"]}).encode("utf-8"), player)

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