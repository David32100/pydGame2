import pygame
import time

from globalVariables import globalVariables
from drawingFunctions import shutdownGame, writeText
from client.communications import sendAMessage

boxColor = (0, 0, 255, 255)
veiwingPlayer = None

def drawJoinPartyBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) - 150, (globalVariables["screenHeight"] / 2) + 120, 300, 90))
  
def drawJoinPartyText(writeText):
  writeText("freesansbold.ttf", 50, "Join Party", (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) + 167))

def joinParty():
  choosingParty = True
  code = ""
  canJoinParty = True
  checkMouse = False

  while choosingParty:
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"], "party":globalVariables["party"]}})
    
    if globalVariables["party"] == None:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          globalVariables["veiwingHomeScreen"] = False
          shutdownGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
          checkMouse = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_BACKSPACE:
            if len(code) > 0:
              code = code.removesuffix(code[-1])
          elif len(pygame.key.name(event.key)) < 2:
            if (len(code) + len(pygame.key.name(event.key))) < 16:
              code += event.unicode

      globalVariables["screen"].fill((0, 255, 255))
      pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) + 155, globalVariables["screenHeight"] - 100, 150, 60))
      pygame.draw.rect(globalVariables["screen"], (0, 255, 0), (45, globalVariables["screenHeight"] - 100, 150, 60))
      pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] / 2) - 140, (globalVariables["screenHeight"] / 2) - 25, 400, 50))
      pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 143, (globalVariables["screenHeight"] / 2) - 28, 406, 56), 3)

      if checkMouse:
        mouseX, mouseY = pygame.mouse.get_pos()

        if globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
            choosingParty = False

        if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
          if len(code) == 15 and canJoinParty:
            sendAMessage({"action":"joinParty", "contents":{"party":code, "username":globalVariables["username"], "status":globalVariables["status"], "discoveredLevels":globalVariables["discoveredLevels"], "currentLevel":globalVariables["currentLevel"]}})
            canJoinParty = False
            choosingParty = False

        checkMouse = False

      writeText("freesansbold.ttf", 60, "Join Party", (0, 0, 0), (globalVariables["screenWidth"] / 2, 80))
      writeText("freesansbold.ttf", 35, "Join", (0, 0, 0), (120, globalVariables["screenHeight"] - 70))
      writeText("freesansbold.ttf", 35, "Back", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 230, globalVariables["screenHeight"] - 70))
      writeText("freesansbold.ttf", 50, "Code:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 230, (globalVariables["screenHeight"] / 2)))
      writeText("freesansbold.ttf", 50, code, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 30, (globalVariables["screenHeight"] / 2)))
      writeText("freesansbold.ttf", 25, str(len(code)) + "/15", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 225, (globalVariables["screenHeight"] / 2)))

      pygame.display.flip()

    else:
      global veiwingPlayer

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          globalVariables["veiwingHomeScreen"] = False
          shutdownGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
          checkMouse = True
        
        globalVariables["screen"].fill((0, 255, 255))
        pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) + 155, globalVariables["screenHeight"] - 100, 150, 60))
        pygame.draw.rect(globalVariables["screen"], (0, 255, 0), (45, globalVariables["screenHeight"] - 100, 150, 60))
        
        for playerIndex in range(len(globalVariables["playersInParty"])):
          if playerIndex >= 4:
            pygame.draw.rect(globalVariables["screen"], (1, 0, playerIndex), (175, 110 + 60 * (playerIndex - 4), 125, 50))
          else:
            pygame.draw.rect(globalVariables["screen"], (1, 0, playerIndex), (50, 110 + 60 * playerIndex, 125, 50))
        
        if checkMouse:
          mouseX, mouseY = pygame.mouse.get_pos()

          if globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
            veiwingPlayer = None
            choosingParty = False

          for playerIndex in range(len(globalVariables["playersInParty"])):
            if globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, playerIndex, 255):
              veiwingPlayer = list(globalVariables["playersInParty"].keys())[playerIndex]

          if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
            veiwingPlayer = None
            sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})
            time.sleep(0.5)
            choosingParty = False
            canJoinParty = True
            globalVariables["party"] = None
            globalVariables["playersInParty"] = {globalVariables["username"]:"Not in game"}

        checkMouse = False

        if veiwingPlayer != None and veiwingPlayer in globalVariables["playersInParty"]:
          writeText("freesansbold.ttf", 35, "User: " + str(veiwingPlayer), (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 50, (globalVariables["screenHeight"] / 2) - 100), 9)
          writeText("freesansbold.ttf", 35, "Status: " + str(globalVariables["playersInParty"][veiwingPlayer][1]), (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 50, (globalVariables["screenHeight"] / 2) - 40), 9)
          writeText("freesansbold.ttf", 35, "Discovered levels: " + str(globalVariables["playersInParty"][veiwingPlayer][2]), (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 50, (globalVariables["screenHeight"] / 2) + 20), 9)
          writeText("freesansbold.ttf", 35, "Current level: " + str(globalVariables["playersInParty"][veiwingPlayer][3]), (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 50, (globalVariables["screenHeight"] / 2) + 80), 9)

        writeText("freesansbold.ttf", 60, "Party", (0, 0, 0), (globalVariables["screenWidth"] / 2, 80))
        writeText("freesansbold.ttf", 35, "Leave", (0, 0, 0), (120, globalVariables["screenHeight"] - 70))
        writeText("freesansbold.ttf", 35, "Back", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 230, globalVariables["screenHeight"] - 70))

        for playerIndex in range(len(globalVariables["playersInParty"])):
          if playerIndex >= 4:
            writeText("freesansbold.ttf", 22, list(globalVariables["playersInParty"].keys())[playerIndex], (255, 255, 255), (237, 121 + 60 * (playerIndex - 4)))
            pygame.draw.line(globalVariables["screen"], (255, 255, 255), (180, 132 + 60 * (playerIndex - 4)), (295, 132 + 60 * (playerIndex - 4)))
            writeText("freesansbold.ttf", 22, list(globalVariables["playersInParty"].values())[playerIndex][1], (255, 255, 255), (237, 146 + 60 * (playerIndex - 4)))
          else:
            writeText("freesansbold.ttf", 22, list(globalVariables["playersInParty"].keys())[playerIndex], (255, 255, 255), (112, 121 + 60 * playerIndex))
            pygame.draw.line(globalVariables["screen"], (255, 255, 255), (55, 132 + 60 * playerIndex), (170, 132 + 60 * playerIndex))
            writeText("freesansbold.ttf", 22, list(globalVariables["playersInParty"].values())[playerIndex][1], (255, 255, 255), (112, 146 + 60 * playerIndex))

        pygame.display.flip()

joinPartyEvent = (boxColor, joinParty)