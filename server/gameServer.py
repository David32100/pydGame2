import socket
import threading
import time
import json
import argon2

playerAccounts = []

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
  server.sendto(message, address)

def askToStopServer(server):
  stop = input("Stop Server (Y): \n")

  while stop != "Y":
    stop = input("Stop Server (Y): \n")

  shutDownServer(server) 

def saveAccounts():
  with open("server/accounts.JSON", "w") as file:
    file.seek(0)
    file.truncate(0)
    file.write(json.dumps(playerAccounts))

def shutDownServer(server):
  global playerAccounts
  print("Shutting down server...")
  saveAccounts()
  server.shutdown(socket.SHUT_RDWR)
  server.close()

def runServer(server):
  global playerAccounts

  try:
    with open("server/accounts.JSON", "r") as file:
      accounts = json.loads(file.read())
  except FileNotFoundError:
    with open("server/accounts.JSON", "w") as file:
      file.write(json.dumps({}))
      accounts = {}
  
  playerAccounts = accounts
  playerAddresses = []
  lobbies = {}
  parties = {}

  while True:
    messageReceived, addressReceived = receiveMessage(server)

    if messageReceived["action"] == "joinServer":
      playerAddresses.append(addressReceived)
      
    elif messageReceived["action"] == "joinGame":
      if messageReceived["contents"]["lobby"] != None:
        lobbies[messageReceived["contents"]["lobby"]][messageReceived["contents"]["username"]] = addressReceived
        
        for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
          if player != addressReceived:
            sendMessage(server, json.dumps({"action":"updatePlayer", "contents": messageReceived["contents"]}).encode("utf-8"), player)
          else:
            sendMessage(server, json.dumps({"action":"joinedLobby", "contents":{"lobby":messageReceived["contents"]["lobby"]}}).encode("utf-8"), player)
      else:
        searchingForLobby = True
        i = 1
        
        while searchingForLobby:
          if not (str(i) + "_" + str(messageReceived["contents"]["currentLevel"])) in lobbies:
            lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])] = {messageReceived["contents"]["username"]: addressReceived}
            searchingForLobby = False
          else:
            if messageReceived["contents"]["party"] != None:
              if len(lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])]) < 9 - len(parties[messageReceived["contents"]["party"]]):
                lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])][messageReceived["contents"]["username"]] = addressReceived
                searchingForLobby = False
              else:
                i += 1
            else:
              if len(lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])]) < 8:
                lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])][messageReceived["contents"]["username"]] = addressReceived
                searchingForLobby = False
              else:
                i += 1

          if messageReceived["contents"]["party"] != None:
            for person in parties[messageReceived["contents"]["party"]]:
              if parties[messageReceived["contents"]["party"]][person][0] != addressReceived and parties[messageReceived["contents"]["party"]][person][1] != "In game":
                sendMessage(server, json.dumps({"action":"joinGame", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}).encode("utf-8"), parties[messageReceived["contents"]["party"]][person][0])
        
        for player in list(lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])].values()):
          if player != addressReceived:
            sendMessage(server, json.dumps({"action":"updatePlayer", "contents": messageReceived["contents"]}).encode("utf-8"), player)
          else:
            sendMessage(server, json.dumps({"action":"joinedLobby", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}).encode("utf-8"), player)

    elif messageReceived["action"] == "leaveGame":
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, json.dumps({"action":"deletePlayer", "contents":messageReceived["contents"]}).encode("utf-8"), player)

      lobbies[messageReceived["contents"]["lobby"]].pop(messageReceived["contents"]["username"])
      time.sleep(0.1)

    elif messageReceived["action"] == "leaveServer":
      playerAddresses.remove(addressReceived)

    elif messageReceived["action"] == "startJump" or messageReceived["action"] == "stopJump" or messageReceived["action"] == "updatePlayer":
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, json.dumps(messageReceived).encode("utf-8"), player)

    elif messageReceived["action"] == "updateStatus":
      if messageReceived["contents"]["party"] != None:
        for player in list(parties[messageReceived["contents"]["party"]].keys()):
          if player != messageReceived["contents"]["username"]:
            sendMessage(server, json.dumps({"action":"updatePlayerStatus", "contents":messageReceived["contents"]}).encode("utf-8"), parties[messageReceived["contents"]["party"]][player][0])
          else:
            parties[messageReceived["contents"]["party"]][messageReceived["contents"]["username"]][1] = messageReceived["contents"]["status"]

    elif messageReceived["action"] == "joinParty":
      if messageReceived["contents"]["party"] in parties:
        if len(parties[messageReceived["contents"]["party"]]) < 8:
          parties[messageReceived["contents"]["party"]][messageReceived["contents"]["username"]] = [addressReceived, messageReceived["contents"]["status"], messageReceived["contents"]["discoveredLevels"], messageReceived["contents"]["currentLevel"]]
          
          for playerInfo in list(parties[messageReceived["contents"]["party"]].values()):
            if playerInfo[0] == addressReceived:
              sendMessage(server, json.dumps({"action":"partyJoined", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":parties[messageReceived["contents"]["party"]]}}).encode("utf-8"), addressReceived)
            else:
              sendMessage(server, json.dumps({"action":"playerJoinedParty", "contents":{"party":messageReceived["contents"]["party"], "player":(messageReceived["contents"]["username"],  messageReceived["contents"]["discoveredLevels"], tuple(addressReceived))}}).encode("utf-8"), playerInfo[0])
      else:
        parties[messageReceived["contents"]["party"]] = {messageReceived["contents"]["username"]: [addressReceived, messageReceived["contents"]["status"], messageReceived["contents"]["discoveredLevels"], messageReceived["contents"]["currentLevel"]]}
        sendMessage(server, json.dumps({"action":"partyJoined", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":parties[messageReceived["contents"]["party"]]}}).encode("utf-8"), addressReceived)

    elif messageReceived["action"] == "leaveParty":
      parties[messageReceived["contents"]["party"]].pop(messageReceived["contents"]["username"])

      for player in list(parties[messageReceived["contents"]["party"]].values()):
        sendMessage(server, json.dumps({"action":"partyDeletePlayer", "contents":{"player":(messageReceived["contents"]["username"], addressReceived)}}).encode("utf-8"), player[0])

    elif messageReceived["action"] == "talk":
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, json.dumps(messageReceived).encode("utf-8"), player)

    elif messageReceived["action"] == "login":
      if messageReceived["contents"]["username"] in playerAccounts:
        if playerAccounts[messageReceived["contents"]["username"]]["loggedIn"]:
          sendMessage(server, json.dumps({"action":"loginFailed", "contents":{"error":"User already logged in"}}).encode("utf-8"), addressReceived)
        else:
          try:
            passwordMatches = argon2.PasswordHasher().verify(playerAccounts[messageReceived["contents"]["username"]]["password"], messageReceived["contents"]["password"])
          except argon2.exceptions.VerificationError or argon2.exceptions.InvalidHashError or argon2.exceptions.VerifyMismatchError:
            passwordMatches = False
          
          if passwordMatches:
            sendMessage(server, json.dumps({"action":"loggedIn", "contents":{"accountInformation":playerAccounts[messageReceived["contents"]["username"]]}}).encode("utf-8"), addressReceived)
            playerAccounts[messageReceived["contents"]["username"]]["loggedIn"] = True
    
    elif messageReceived["action"] == "signUp":
      if not messageReceived["contents"]["username"] in playerAccounts:
        playerAccounts[messageReceived["contents"]["username"]] = {"loggedIn": True, "username":messageReceived["contents"]["username"], "password":messageReceived["contents"]["password"], "discoveredLevels":0, "currentLevel":0}
        sendMessage(server, json.dumps({"action":"loggedIn", "contents":{"accountInformation":playerAccounts[messageReceived["contents"]["username"]]}}).encode("utf-8"), addressReceived)
        saveAccounts()

    elif messageReceived["action"] == "saveProgress":
      if messageReceived["contents"]["username"] in playerAccounts:
        playerAccounts[messageReceived["contents"]["username"]]["username"] = messageReceived["contents"]["username"]
        playerAccounts[messageReceived["contents"]["username"]]["discoveredLevels"] = messageReceived["contents"]["discoveredLevels"]
        playerAccounts[messageReceived["contents"]["username"]]["currentLevel"] = messageReceived["contents"]["currentLevel"]
        saveAccounts()

    elif messageReceived["action"] == "signOut":
      playerAccounts[messageReceived["contents"]["username"]]["loggedIn"] = False

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