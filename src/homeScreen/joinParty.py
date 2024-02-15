import pygame
from globalVariables import globalVariables
from drawingFunctions import shutdownGame, writeText
from client.communications import sendAMessage

boxColor = (0, 0, 255, 255)

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
            sendAMessage({"action":"joinParty", "contents":{"party":code, "username":globalVariables["username"]}})
            canJoinParty = False
            choosingParty = False

        checkMouse = False

      writeText("freesansbold.ttf", 60, "Join Party", (0, 0, 0), (globalVariables["screenWidth"] / 2, 80))
      writeText("freesansbold.ttf", 35, "Join", (0, 0, 0), (120, globalVariables["screenHeight"] - 70))
      writeText("freesansbold.ttf", 35, "Back", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 230, globalVariables["screenHeight"] - 70))
      writeText("freesansbold.ttf", 50, "Code:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 230, (globalVariables["screenHeight"] / 2)))
      writeText("freesansbold.ttf", 50, code, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 60, (globalVariables["screenHeight"] / 2)))

      pygame.display.flip()

    else:
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
            choosingParty = False

          if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
            globalVariables["playersInParty"] = []
            sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})
            globalVariables["party"] = None
            choosingParty = False
            canJoinParty = True

        checkMouse = False

        writeText("freesansbold.ttf", 60, "Party", (0, 0, 0), (globalVariables["screenWidth"] / 2, 80))
        writeText("freesansbold.ttf", 35, "Leave", (0, 0, 0), (120, globalVariables["screenHeight"] - 70))
        writeText("freesansbold.ttf", 35, "Back", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 230, globalVariables["screenHeight"] - 70))

        for playerIndex in range(len(globalVariables["playersInParty"])):
          if playerIndex >= 4:
            writeText("freesansbold.ttf", 22, globalVariables["playersInParty"][playerIndex], (255, 255, 255), (237, 121 + 60 * (playerIndex - 4)))
          else:
            writeText("freesansbold.ttf", 22, globalVariables["playersInParty"][playerIndex], (255, 255, 255), (112, 121 + 60 * playerIndex))

        pygame.display.flip()

joinPartyEvent = (boxColor, joinParty)