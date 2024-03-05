import pygame

from globalVariables import globalVariables
from game.levels import levels
from drawingFunctions import shutdownGame, writeText
from client.communications import sendAMessage

boxColor = (0, 255, 0, 255)

def drawSelectLevelBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) - 150, (globalVariables["screenHeight"] / 2) + 10, 300, 90))
  
def drawSelectLevelText(writeText):
  writeText("freesansbold.ttf", 50, "Level Select", (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) + 57))
  
def drawLevels(levelScroll):
  for g in range(256):
    for r in range(256):
      if (g * 255) + r <= len(levels) - 1 and (g * 255) + r <= globalVariables["discoveredLevels"]:
        if ((g * 255) + r) % 2 == 0:
          pygame.draw.rect(globalVariables["screen"], (r, g, 0), ((((g * 255) + r) * 75) + 10 - levelScroll, (globalVariables["screenHeight"] / 2) - 100, 75, 75))
        else:
          pygame.draw.rect(globalVariables["screen"], (r, g, 0), (((((g * 255) + r) - 1) * 75) + 10 - levelScroll, (globalVariables["screenHeight"] / 2) + 50, 75, 75))      

def drawSelectLevel():
  selectingLevel = True
  levelScroll = int(globalVariables["currentLevel"] / 10) * (globalVariables["screenWidth"] + 50)
  checkMouse = False

  while selectingLevel:
    sendAMessage({"action":"updateStatus", "contents":{"username": globalVariables["username"], "status":globalVariables["status"], "party":globalVariables["party"]}})
  
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        selectingLevel = False
        globalVariables["veiwingHomeScreen"] = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    globalVariables["screen"].fill((0, 255, 255))
    drawLevels(levelScroll)
    pygame.draw.rect(globalVariables["screen"], (0, 0, 255, 255), ((globalVariables["screenWidth"] / 2) - 75, (globalVariables["screenHeight"] / 2) + 150, 150, 75))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and levelScroll < 177725:
      levelScroll += 5
    if keys[pygame.K_LEFT] and levelScroll > 0:
      levelScroll -= 5
    if keys[pygame.K_d] and keys[pygame.K_b] and keys[pygame.K_u] and keys[pygame.K_g]:
      sendAMessage({"action":"debugServer"})

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 0, 255, 255):
        selectingLevel = False

      for g in range(255):
        for r in range(255):
          if globalVariables["screen"].get_at((mouseX, mouseY)) == (r, g, 0, 255):
            globalVariables["currentLevel"] = (g * 255) + r
            sendAMessage({"action":"updateStatus", "contents":{"party":globalVariables["party"], "status":globalVariables["status"], "currentLevel":globalVariables["currentLevel"], "username":globalVariables["username"]}})
            globalVariables["playersInParty"][globalVariables["username"]][3] = globalVariables["currentLevel"]
            selectingLevel = False

      checkMouse = False
        
    writeText("freesansbold.ttf", 35, "Back", (255, 255, 255, 255), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 187))
    writeText("freesansbold.ttf", 50, "Select a level", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 200))
    writeText("freesansbold.ttf", 30, "Use the arrow keys to move through the levels", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 150))

    for levelIndex in range(0, len(levels)):
      if levelIndex <= globalVariables["discoveredLevels"]:
        if levelIndex % 2 == 0:
          writeText("freesansbold.ttf", 30, str(levelIndex), (255, 255, 255), (((levelIndex) * 75) + 48 - levelScroll, (globalVariables["screenHeight"] / 2) - 62))
        else:
          writeText("freesansbold.ttf", 30, str(levelIndex), (255, 255, 255), (((levelIndex - 1) * 75) + 48 - levelScroll, (globalVariables["screenHeight"] / 2) + 88))
      
    pygame.display.flip()

selectLevelEvent = (boxColor, drawSelectLevel)