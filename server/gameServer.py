import eventlet.wsgi
import pygame
import socketio
import eventlet
import sys
import json
import argon2
import time
import random

playerAccounts = []
anonymousPlayers = {}
rooms = {}
server = None
onlinePlayers = {}

def createServer() -> tuple[socketio.Server, socketio.WSGIApp]:
  newServer = socketio.Server()
  newApp = socketio.WSGIApp(newServer)
  return (newServer, newApp)

def sendMessage(message, sidOrRoom: str|list, skipSid: str|list|None=None):
  global server
  print("Sending to:", sidOrRoom, "\nMessage:", message)
  server.send(message, sidOrRoom, skip_sid=skipSid)

def askToStopServer():
  stop = input("Stop Server (Y): \n")

  while stop != "Y":
    stop = input("Stop Server (Y): \n")

  shutDownServer() 

def saveAccounts():
  with open("server/accounts.JSON", "w") as file:
    file.seek(0)
    file.truncate(0)
    file.write(json.dumps(playerAccounts))

def shutDownServer():
  global playerAccounts
  print("Shutting down server...")
  saveAccounts()
  sys.exit()

def updateServer() -> dict:
  try:
    with open("server/accounts.JSON", "r") as file:
      accounts = json.loads(file.read())
  except FileNotFoundError:
    with open("server/accounts.JSON", "w") as file:
      file.write(json.dumps({}))
      accounts = {}
  
  return accounts

# rooms = {"party (no ' _ ') ":{sid:[usrnm, stts, DL, CL], sid:[usrnm, stts, DL, CL]}, "lobby":[(usrnm, sid), (usrnm, sid)]}, anonymousPlayers = {"usrnm":"anon+#"}
def manageMessage(sid: str, messageReceived):
  global playerAccounts, rooms, anonymousPlayers, onlinePlayers

  if messageReceived["action"] == "updatePlayer":
    sendMessage(messageReceived, messageReceived["contents"]["lobby"], sid)

  elif messageReceived["action"] == "login":
    if messageReceived["contents"]["username"] in playerAccounts:
      if playerAccounts[messageReceived["contents"]["username"]]["banned"] != False:
        sendMessage({"action":"loginFailed", "contents":{"error":"Banned: " + playerAccounts[messageReceived["contents"]["username"]]["banned"]}}, sid)
      elif playerAccounts[messageReceived["contents"]["username"]]["loggedIn"]:
        sendMessage({"action":"loginFailed", "contents":{"error":"User already logged in"}}, sid)
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
          sendMessage({"action":"loggedIn", "contents":{"accountInformation":playerAccounts[messageReceived["contents"]["username"]]}}, sid)
          playerAccounts[messageReceived["contents"]["username"]]["loggedIn"] = True
          onlinePlayers[sid] = messageReceived["contents"]["username"]
        else:
          sendMessage({"action":"loginFailed", "contents":{"error":"Username or password is incorrect"}}, sid)
    else:
      time.sleep(random.randint(1, 5))
      sendMessage({"action":"loginFailed", "contents":{"error":"Username or password is incorrect"}}, sid)

  elif messageReceived["action"] == "signUp":
    if not messageReceived["contents"]["username"] in playerAccounts and len(messageReceived["contents"]["password"]) > 0:
      playerAccounts[messageReceived["contents"]["username"]] = {"banned": False, "loggedIn": True, "username":messageReceived["contents"]["username"], "password":messageReceived["contents"]["password"], "discoveredLevels":0, "currentLevel":0, "settings":{"volume":100, "playerColor":(0, 0, 255), "anonymous":False, "hideTextChat":False, "controls":{"jump":[pygame.K_UP, pygame.K_SPACE, pygame.K_w], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d], "talk":[pygame.K_BACKQUOTE]}}}
      onlinePlayers[sid] = messageReceived["contents"]["username"]
      sendMessage({"action":"loggedIn", "contents":{"accountInformation":playerAccounts[messageReceived["contents"]["username"]]}}, sid)
      saveAccounts()

  elif messageReceived["action"] == "anonymousModeOn":
    i = 0

    while True:
      if not "anonymousPlayer" + str(i) in list(anonymousPlayers.values()):
        anonymousPlayers[messageReceived["contents"]["username"]] = "anonymousPlayer" + str(i)
        sendMessage({"action":"changedVisibleUsername", "contents":{"visibleUsername":"anonymousPlayer" + str(i)}}, sid)
        break
      
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
    if messageReceived["contents"]["lobby"] == None:
      i = 0

      while True:
        if not str(i) + "_" + str(messageReceived["contents"]["currentLevel"]) in rooms:
          server.enter_room(sid, str(i) + "_" + str(messageReceived["contents"]["currentLevel"]))
          rooms[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])] = [(messageReceived["contents"]["username"], sid)]
          break
        else:
          if messageReceived["party"] == None:
            if len(rooms[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])]) < 8:
              server.enter_room(sid, str(i) + "_" + str(messageReceived["contents"]["currentLevel"]))
              rooms[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])].append((messageReceived["contents"]["username"], sid))
              break
          elif len(rooms[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])]) <= 8 - len(rooms[messageReceived["contents"]["party"]]):
            server.enter_room(sid, str(i) + "_" + str(messageReceived["contents"]["currentLevel"]))
            rooms[str(i) + "_" + str(messageReceived["contents"]["currentLevel"])].append((messageReceived["contents"]["username"], sid))
            break
        
        i += 1
      
      if messageReceived["contents"]["party"] != None:
        for person in rooms[messageReceived["contents"]["party"]]:
          if person != sid and rooms[messageReceived["contents"]["party"]][person][1] != "In game":
            sendMessage({"action":"joinGame", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}, person)

      sendMessage({"action":"joinedLobby", "contents":{"lobby":str(i) + "_" + str(messageReceived["contents"]["currentLevel"])}}, sid)
      messageReceived["contents"]["lobby"] = str(i) + "_" + str(messageReceived["contents"]["currentLevel"])
    else:
      server.enter_room(sid, messageReceived["contents"]["lobby"])
      rooms[messageReceived["contents"]["lobby"]] = [(messageReceived["contents"]["username"], sid)]
      sendMessage({"action":"joinedLobby", "contents":{"lobby":messageReceived["contents"]["lobby"]}}, sid)

    if messageReceived["contents"]["username"] in anonymousPlayers:
      messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]

    sendMessage({"action":"updatePlayer", "contents": messageReceived["contents"]}, rooms[messageReceived["contents"]["lobby"]], sid)
  elif messageReceived["action"] == "leaveGame":
    server.leave_room(sid, messageReceived["contents"]["lobby"])
    rooms[messageReceived["contents"]["lobby"]].remove((messageReceived["contents"]["username"], sid))

    if messageReceived["contents"]["username"] in anonymousPlayers:
      messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]
    
    sendMessage({"action":"deletePlayer", "contents":messageReceived["contents"]}, messageReceived["contents"]["lobby"], sid)
    sendMessage({"action":"leftGame"}, sid)

  elif messageReceived["action"] == "startJump" or messageReceived["action"] == "stopJump":
    sendMessage(messageReceived, messageReceived["contents"]["lobby"], sid)
    sendMessage({"action":"jumped"}, sid)

  elif messageReceived["action"] == "updateStatus":
    if messageReceived["contents"]["party"] != None:
      messageReceived["contents"]["username"] = sid
      sendMessage({"action":"updatePlayerStatus", "contents":messageReceived["contents"]}, messageReceived["contents"]["party"], sid)
 
      if "currentLevel" in messageReceived["contents"]:
        rooms[messageReceived["contents"]["party"]][sid][3] = messageReceived["contents"]["currentLevel"]
      if "discoveredLevels" in messageReceived["contents"]:
        rooms[messageReceived["contents"]["party"]][sid][2] = messageReceived["contents"]["discoveredLevels"]
      
      rooms[messageReceived["contents"]["party"]][sid][1] = messageReceived["contents"]["status"]
      
  elif messageReceived["action"] == "joinParty":
    if messageReceived["contents"]["party"] in rooms:
      if len(rooms[messageReceived["contents"]["party"]]) < 8:
        server.enter_room(sid, messageReceived["contents"]["party"])
        rooms[messageReceived["contents"]["party"]][sid] = [messageReceived["contents"]["username"], messageReceived["contents"]["status"], messageReceived["contents"]["discoveredLevels"], messageReceived["contents"]["currentLevel"]]
        sendMessage({"action":"partyJoined", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":rooms[messageReceived["contents"]["party"]]}}, sid)
        sendMessage({"action":"playerJoinedParty", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":rooms[messageReceived["contents"]["party"]]}}, messageReceived["contents"]["party"], sid)
    else:
      server.enter_room(sid, messageReceived["contents"]["party"])
      rooms[messageReceived["contents"]["party"]] = {sid: [messageReceived["contents"]["username"], messageReceived["contents"]["status"], messageReceived["contents"]["discoveredLevels"], messageReceived["contents"]["currentLevel"]]}
      sendMessage({"action":"partyJoined", "contents":{"party":messageReceived["contents"]["party"], "playersInParty":rooms[messageReceived["contents"]["party"]]}}, sid)

  elif messageReceived["action"] == "leaveParty":
    server.leave_room(sid, messageReceived["contents"]["party"])
    rooms[messageReceived["contents"]["party"]].pop(sid)
    sendMessage({"action":"partyLeft"}, sid)
    sendMessage({"action":"partyDeletePlayer", "contents":{"party":rooms[messageReceived["contents"]["party"]]}}, messageReceived["contents"]["party"])

  elif messageReceived["action"] == "talk":
    if messageReceived["contents"]["username"] in anonymousPlayers:
      messageReceived["contents"]["username"] = anonymousPlayers[messageReceived["contents"]["username"]]
      sendMessage(messageReceived, messageReceived["contents"]["lobby"], sid)
      sendMessage({"action":"talking"}, sid)

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
        saveAccounts()
        sendMessage({"action":"usernameChanged", "contents":{"newUsername":messageReceived["contents"]["newUsername"]}}, sid)
      else:
        sendMessage({"action":"usernameChangeFailed", "contents":{"error":"Password is incorrect"}}, sid)
    else:
      sendMessage({"action":"usernameChangeFailed", "contents":{"error":"Username already exists"}}, sid)

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
        sendMessage({"action":"passwordChanged"}, sid)
      else:
        sendMessage({"action":"passwordChangeFailed", "contents":{"error":"Password is incorrect"}}, sid)

  elif messageReceived["action"] == "deleteAccount":
    playerAccounts.pop(messageReceived["contents"]["username"])
    saveAccounts()

  elif messageReceived["action"] == "updateSettings":
    playerAccounts[messageReceived["contents"]["username"]]["settings"] = messageReceived["contents"]["settings"]
    saveAccounts()

  elif messageReceived["action"] == "anonymousModeOff":
    if messageReceived["contents"]["username"] in anonymousPlayers:
      anonymousPlayers.pop(messageReceived["contents"]["username"])

    sendMessage({"action":"changedVisibleUsername", "contents":{"visibleUsername":messageReceived["contents"]["username"]}}, sid)

def startServer(app: socketio.WSGIApp, host: str, port: int):
  eventlet.wsgi.server(eventlet.listen((host, port)), app)

def protectedMessageManager(sid, messageReceived):
  global onlinePlayers, playerAccounts

  try:
    manageMessage(sid, messageReceived)
  except OSError as e:
    print(e, "\nAttempting to kick out players...")

    try:
      for username in list(onlinePlayers.values()):
        if username != None:
          playerAccounts[username]["loggedIn"] = False
      
      saveAccounts()
    except:
      print("Attempt failed.")
  except:
    print("An unknown error occured: gameServer.py startServer() \nAttempting to kick out players...")

    try:
      for username in list(onlinePlayers.values()):
        if username != None:
          playerAccounts[username]["loggedIn"] = False
      
      saveAccounts()
    except:
      print("Attempt failed.")

def logPlayer(sid, _, __):
  global onlinePlayers
  onlinePlayers[sid] = None

def removePlayer(sid):
  global onlinePlayers
  onlinePlayers.pop(sid)

def manageGameServer():
  global server
  global playerAccounts
  playerAccounts = updateServer()
  server, app = createServer()

  server.on("connect", logPlayer)
  server.on("disconnect", removePlayer)
  server.on("message", protectedMessageManager)
  startServer(app, "", 5000)

manageGameServer()