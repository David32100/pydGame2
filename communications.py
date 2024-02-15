import subprocess
import json
import time

from gameClient import createUdpClient, sendMessage, shutDownClient, receiveMessage
from globalVariables import globalVariables
from jumper import OtherJumpers, jumper

message = {"action":"spawnPlayer","contents":{"Username": "Player1", "playerPosition": (123, 123), "Server":10, "Status":"In game"}}
client = None
host, port = "127.0.0.1", 36848

def createGameClient():
  global client
  client = createUdpClient()

def sendAMessage(message):
  global client
  messageToSend = json.dumps(message).encode("utf-8")
  sendMessage(client, messageToSend, host, port)

def shutdownGameClient():
  global client
  shutDownClient(client)
  client = None

def receiveMessages():
  global client

  try:
    messageReceived, addressReceived = receiveMessage(client)
    decodedMessageReceived = json.loads(messageReceived.decode("utf-8"))
    return decodedMessageReceived, addressReceived
  except OSError as e:
    print("Failed to receive message:", e)
    return {"actions":None}

def check_internet_connection():
  try:
    subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
    return True
  except subprocess.CalledProcessError:
    return False
  
def receiveAndManageMessages():
  while True:
    messageReceived, addressReceived = receiveMessages()

    if messageReceived["action"] == "joinedLobby":
      globalVariables["lobby"] = messageReceived["contents"]["lobby"]

    elif messageReceived["action"] == "updatePlayer":
      if messageReceived["contents"]["username"] in globalVariables["playersInLobby"]:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]].updateJumper(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])
      else:
        globalVariables["playersInLobby"][messageReceived["contents"]["username"]] = OtherJumpers(messageReceived["contents"]["position"][0], messageReceived["contents"]["position"][1])

    elif messageReceived["action"] == "deletePlayer":
      globalVariables["playersInLobby"].pop(messageReceived["contents"]["username"])

    elif messageReceived["action"] == "JUMP!!!":
      jumper.messageInitiatedJump()

    elif messageReceived["action"] == "partyJoined":
      globalVariables["party"] = messageReceived["contents"]["party"]

    elif messageReceived["action"] == "partyFull":
      print("Cannot join, party full.")
    
    elif messageReceived["action"] == "playerJoinedParty":
      globalVariables["playersInParty"].append(messageReceived["contents"]["player"][0])
      sendAMessage({"action":"updateParty", "contents":{"username":globalVariables["username"], "address":tuple(messageReceived["contents"]["player"][1])}})

    elif messageReceived["action"] == "updatingParty":
      globalVariables["playersInParty"].append(messageReceived["contents"]["player"][0])

    elif messageReceived["action"] == "partyDeletePlayer":
      globalVariables["playersInParty"].remove(messageReceived["contents"]["player"][0])

    elif messageReceived["action"] == "joinedLobby":
      globalVariables["veiwingHomeScreen"] = False
      globalVariables["playingGame"] = True
      globalVariables["currentLevel"] = messageReceived["contents"]["lobby"].split("_")[1]
      sendAMessage({"action":"joinGame","contents":{"username": globalVariables["username"], "position":(jumper.jumperXWithScroll, jumper.jumperY), "currentLevel": globalVariables["currentLevel"], "party":None}})
      time.sleep(0.5)
      globalVariables["status"] = "In game"
