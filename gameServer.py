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
  lobbies = {"1_2": {"1":123, "2":123, "3":123, "4":123, "5":123, "6":123, "7":123, "8":123}}

  while True:
    messageReceived, addressReceived = receiveMessage(server)

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
          sendMessage(server, json.dumps({"action":"newPlayer", "contents":{"username": messageReceived["contents"]["username"], "postition": messageReceived["contents"]["position"]}}).encode("utf-8"), player)
        else:
          sendMessage(server, json.dumps({"action":"joinedLobby", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}).encode("utf-8"), player)
      print("Player '" + str(messageReceived["contents"]["username"]) + "' joined lobby " + str(i) + "_" + str(messageReceived["contents"]["currentLevel"]) + "!")

    if messageReceived["action"] == "leaveGame":
      lobbies[messageReceived["contents"]["lobby"]].pop(messageReceived["contents"]["username"])

    if messageReceived["action"] == "leaveServer":
      playerAddresses.remove(addressReceived)

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