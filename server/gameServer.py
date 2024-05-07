# Messages priority: Update player, start/stop jump, talk, update status, join/leave game, update settings, save progress, join/leave party, anonymous mode on/off, sign out, login, sign up, delete save, change username, change password, delete account, debug server
import pygame
import socket
import threading
import time
import json
import argon2

playerAccounts = []
playerAddresses = []

def createUdpServer(host: str, port: int) -> socket.socket:
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  newSocket.bind((host, port))
  return newSocket

def receiveMessage(server: socket.socket):
  messageReceived, addressReceived = server.recvfrom(1024)
  decodedMessageReceived = json.loads(messageReceived.decode("utf-8"))
  message, sender = decodedMessageReceived
  return message, (sender, addressReceived)

def sendMessage(server: socket.socket, message: str, address):
  server.sendto(json.dumps([message, address[0]]).encode("utf-8"), address[1])

def askToStopServer(server: socket.socket):
  stop = input("Stop Server (Y): \n")

  while stop != "Y":
    stop = input("Stop Server (Y): \n")

  shutDownServer(server) 

def saveAccounts():
  with open("server/accounts.JSON", "w") as file:
    file.seek(0)
    file.truncate(0)
    file.write(json.dumps(playerAccounts))

def shutDownServer(server: socket.socket):
  global playerAddresses

  for address in playerAddresses:
    sendMessage(server, {"action":"leaveServer"}, address)

  print("Shutting down server...")
  saveAccounts()
  server.shutdown(socket.SHUT_RDWR)
  server.close()

def updateServer() -> dict:
  try:
    with open("server/accounts.JSON", "r") as file:
      accounts = json.loads(file.read())
  except FileNotFoundError:
    with open("server/accounts.JSON", "w") as file:
      file.write(json.dumps({}))
      accounts = {}
  
  return accounts

def runServer(server: socket.socket):
  global playerAccounts, playerAddresses
  playerAccounts = updateServer()
  lobbies = {}
  parties = {}
  anonymousPlayers = {}

  while True:
    messageReceived, addressReceived = receiveMessage(server)

    if messageReceived["action"] == "updatePlayer":
      if messageReceived["contents"]["username"] in anonymousPlayers:
        messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]
          
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, messageReceived, player)

    elif messageReceived["action"] == "login":
      if messageReceived["contents"]["username"] in playerAccounts:
        if playerAccounts[messageReceived["contents"]["username"]]["banned"] != False:
          sendMessage(server, {"action":"loginFailed", "contents":{"error":"Banned: " + playerAccounts[messageReceived["contents"]["username"]]["banned"]}}, addressReceived)
        elif playerAccounts[messageReceived["contents"]["username"]]["loggedIn"]:
          sendMessage(server, {"action":"loginFailed", "contents":{"error":"User already logged in"}}, addressReceived)
        else:
          try:
            passwordMatches = argon2.PasswordHasher().verify(playerAccounts[messageReceived["contents"]["username"]]["password"], messageReceived["contents"]["password"])
          except argon2.exceptions.VerificationError:
            passwordMatches = False
          except argon2.exceptions.InvalidHashError:
            passwordMatches = False
          except argon2.exceptions.VerifyMismatchError:
            passwordMatches = False
          
          if passwordMatches:
            sendMessage(server, {"action":"loggedIn", "contents":{"accountInformation":playerAccounts[messageReceived["contents"]["username"]]}}, addressReceived)
            playerAccounts[messageReceived["contents"]["username"]]["loggedIn"] = True
          else:
            sendMessage(server, {"action":"loginFailed", "contents":{"error":"Username or password is incorrect"}}, addressReceived)
      else:
        sendMessage(server, {"action":"loginFailed", "contents":{"error":"Username or password is incorrect"}}, addressReceived)

    elif messageReceived["action"] == "signUp":
      if not messageReceived["contents"]["username"] in playerAccounts:
        playerAccounts[messageReceived["contents"]["username"]] = {"banned": False, "loggedIn": True, "username":messageReceived["contents"]["username"], "password":messageReceived["contents"]["password"], "discoveredLevels":0, "currentLevel":0, "settings":{"volume":100, "playerColor":(0, 0, 255), "anonymous":False, "hideTextChat":False, "controls":{"jump":[pygame.K_UP, pygame.K_SPACE, pygame.K_w], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d], "talk":[pygame.K_BACKQUOTE]}}}
        sendMessage(server, {"action":"loggedIn", "contents":{"accountInformation":playerAccounts[messageReceived["contents"]["username"]]}}, addressReceived)
        saveAccounts()

    elif messageReceived["action"] == "joinServer":
      playerAddresses.append(addressReceived)

    elif messageReceived["action"] == "anonymousModeOn":
      i = 0

      while True:
        if not "anonymousPlayer" + str(i) in list(anonymousPlayers.values()):
          anonymousPlayers[messageReceived["contents"]["username"]] = "anonymousPlayer" + str(i)
          sendMessage(server, {"action":"changedVisibleUsername", "contents":{"visibleUsername":"anonymousPlayer" + str(i)}}, addressReceived)
          break
        else:
          i += 1

    elif messageReceived["action"] == "debugServer":
      try:
        try:
          with open("server/fixServer.txt", "r") as file:
            program = eval(file.read())

          try:
            func = program["action"]
            args = program["args"]
            try:
              func(*args)
            except UnboundLocalError:
              print("Debug error: Could not run function:", type(func), func, "with args:", type(args), args)
              print(e)
          except OSError as e:
            print("Debug error: Function or arguments not found in:", type(program), program)
            print(e)
        except FileNotFoundError:
          print("Debug error: File not found")
      except:
        print("Debug error: An unknown error occured.")
        
    elif messageReceived["action"] == "joinGame":
      if messageReceived["contents"]["lobby"] != None:
        lobbies[messageReceived["contents"]["lobby"]][messageReceived["contents"]["username"]] = addressReceived

        if messageReceived["contents"]["username"] in anonymousPlayers:
          messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]
        
        for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
          if player != addressReceived:
            sendMessage(server, {"action":"updatePlayer", "contents": messageReceived["contents"]}, player)
          else:
            sendMessage(server, {"action":"joinedLobby", "contents":{"lobby":messageReceived["contents"]["lobby"]}}, player)
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
                sendMessage(server, {"action":"joinGame", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}, parties[messageReceived["contents"]["party"]][person][0])
        
        for player in list(lobbies[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])].values()):
          if player != addressReceived:
            if messageReceived["contents"]["username"] in anonymousPlayers:
              messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]
            sendMessage(server, {"action":"updatePlayer", "contents": messageReceived["contents"]}, player)
          else:
            sendMessage(server, {"action":"joinedLobby", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}, player)

    elif messageReceived["action"] == "leaveGame":
      lobbies[messageReceived["contents"]["lobby"]].pop(messageReceived["contents"]["username"])

      if messageReceived["contents"]["username"] in anonymousPlayers:
        messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]
      
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        sendMessage(server, {"action":"deletePlayer", "contents":messageReceived["contents"]}, player)
        
      time.sleep(0.1)

    elif messageReceived["action"] == "leaveServer":
      playerAddresses.remove(addressReceived)

    elif messageReceived["action"] == "startJump" or messageReceived["action"] == "stopJump":
      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, messageReceived, player)
    elif messageReceived["action"] == "updateStatus":
      if messageReceived["contents"]["party"] != None:
        for player in list(parties[messageReceived["contents"]["party"]].keys()):
          if player != messageReceived["contents"]["username"]:
            sendMessage(server, {"action":"updatePlayerStatus", "contents":messageReceived["contents"]}, parties[messageReceived["contents"]["party"]][player][0])
          else:
            if "currentLevel" in messageReceived["contents"]:
              parties[messageReceived["contents"]["party"]][messageReceived["contents"]["username"]][3] = messageReceived["contents"]["currentLevel"]
            if "discoveredLevels" in messageReceived["contents"]:
              parties[messageReceived["contents"]["party"]][messageReceived["contents"]["username"]][2] = messageReceived["contents"]["discoveredLevels"]
            
            parties[messageReceived["contents"]["party"]][messageReceived["contents"]["username"]][1] = messageReceived["contents"]["status"]
            
    elif messageReceived["action"] == "joinParty":
      if messageReceived["contents"]["party"] in parties:
        if len(parties[messageReceived["contents"]["party"]]) < 8:
          parties[messageReceived["contents"]["party"]][messageReceived["contents"]["username"]] = [addressReceived, messageReceived["contents"]["status"], messageReceived["contents"]["discoveredLevels"], messageReceived["contents"]["currentLevel"]]
          
          for playerInfo in list(parties[messageReceived["contents"]["party"]].values()):
            if playerInfo[0] == addressReceived:
              sendMessage(server, {"action":"partyJoined", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":parties[messageReceived["contents"]["party"]]}}, addressReceived)
            else:
              sendMessage(server, {"action":"playerJoinedParty", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":parties[messageReceived["contents"]["party"]]}}, playerInfo[0])
      else:
        parties[messageReceived["contents"]["party"]] = {messageReceived["contents"]["username"]: [addressReceived, messageReceived["contents"]["status"], messageReceived["contents"]["discoveredLevels"], messageReceived["contents"]["currentLevel"]]}
        sendMessage(server, {"action":"partyJoined", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":parties[messageReceived["contents"]["party"]]}}, addressReceived)

    elif messageReceived["action"] == "leaveParty":
      parties[messageReceived["contents"]["party"]].pop(messageReceived["contents"]["username"])

      for player in list(parties[messageReceived["contents"]["party"]].values()):
        sendMessage(server, {"action":"partyDeletePlayer", "contents":{"player":(messageReceived["contents"]["username"], addressReceived)}}, player[0])

    elif messageReceived["action"] == "talk":
      if messageReceived["contents"]["username"] in anonymousPlayers:
        messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]

      for player in list(lobbies[messageReceived["contents"]["lobby"]].values()):
        if player != addressReceived:
          sendMessage(server, messageReceived, player)

    elif messageReceived["action"] == "saveProgress":
      if messageReceived["contents"]["username"] in playerAccounts:
        playerAccounts[messageReceived["contents"]["username"]]["username"] = messageReceived["contents"]["username"]
        playerAccounts[messageReceived["contents"]["username"]]["discoveredLevels"] = messageReceived["contents"]["discoveredLevels"]
        playerAccounts[messageReceived["contents"]["username"]]["currentLevel"] = messageReceived["contents"]["currentLevel"]
        playerAccounts[messageReceived["contents"]["username"]]["settings"]["anonymous"] = False
        saveAccounts()

    elif messageReceived["action"] == "signOut":
      playerAccounts[messageReceived["contents"]["username"]]["loggedIn"] = False

    elif messageReceived["action"] == "deleteSave":
      playerAccounts[messageReceived["contents"]["username"]]["discoveredLevels"] = 0
      playerAccounts[messageReceived["contents"]["username"]]["currentLevel"] = 0
      saveAccounts()

    elif messageReceived["action"] == "changeUsername":
      if messageReceived["contents"]["username"] in playerAccounts and not messageReceived["contents"]["newUsername"] in playerAccounts:
        try:
          passwordMatches = argon2.PasswordHasher().verify(playerAccounts[messageReceived["contents"]["username"]]["password"], messageReceived["contents"]["password"])
        except argon2.exceptions.VerificationError:
          passwordMatches = False
        except argon2.exceptions.InvalidHashError:
          passwordMatches = False
        except argon2.exceptions.VerifyMismatchError:
          passwordMatches = False

        if passwordMatches:
          playerAccounts[messageReceived["contents"]["newUsername"]] = playerAccounts[messageReceived["contents"]["username"]]
          playerAccounts[messageReceived["contents"]["newUsername"]]["username"] = messageReceived["contents"]["newUsername"]
          playerAccounts.pop(messageReceived["contents"]["username"])
          playerAddresses.remove(addressReceived)
          playerAddresses.append((messageReceived["contents"]["newUsername"], addressReceived[1]))
          saveAccounts()
          sendMessage(server, {"action":"usernameChanged", "contents":{"newUsername":messageReceived["contents"]["newUsername"]}}, addressReceived)
        else:
          sendMessage(server, {"action":"usernameChangeFailed", "contents":{"error":"Password is incorrect"}}, addressReceived)
      else:
        sendMessage(server, {"action":"usernameChangeFailed", "contents":{"error":"Username already exists"}}, addressReceived)

    elif messageReceived["action"] == "changePassword":
      if messageReceived["contents"]["username"] in playerAccounts:
        try:
          passwordMatches = argon2.PasswordHasher().verify(playerAccounts[messageReceived["contents"]["username"]]["password"], messageReceived["contents"]["oldPassword"])
        except argon2.exceptions.VerificationError:
          passwordMatches = False
        except argon2.exceptions.InvalidHashError:
          passwordMatches = False
        except argon2.exceptions.VerifyMismatchError:
          passwordMatches = False

        if passwordMatches:
          playerAccounts[messageReceived["contents"]["username"]]["password"] = messageReceived["contents"]["newPassword"]
          saveAccounts()
          sendMessage(server, {"action":"passwordChanged"}, addressReceived)
        else:
          sendMessage(server, {"action":"passwordChangeFailed", "contents":{"error":"Password is incorrect"}}, addressReceived)

    elif messageReceived["action"] == "deleteAccount":
      playerAddresses.remove(addressReceived)
      playerAccounts.pop(messageReceived["contents"]["username"])
      saveAccounts()

    elif messageReceived["action"] == "updateSettings":
      playerAccounts[messageReceived["contents"]["username"]]["settings"] = messageReceived["contents"]["settings"]
      saveAccounts()

    elif messageReceived["action"] == "anonymousModeOff":
      if messageReceived["contents"]["username"] in anonymousPlayers:
        anonymousPlayers.pop(messageReceived["contents"]["username"])
        sendMessage(server, {"action":"changedVisibleUsername", "contents":{"visibleUsername":messageReceived["contents"]["username"]}}, addressReceived)

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