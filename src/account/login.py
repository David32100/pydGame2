import pygame
import sys
import time

from globalVariables import globalVariables
from drawingFunctions import writeText
from client.communications import shutdownGameClient, sendAMessage

def writeInTextBox(originalText:str, maxCharacters:int, keydownEvent:pygame.event.Event):
  if keydownEvent.key == pygame.K_BACKSPACE:
    if len(originalText) > 0:
      originalText = originalText.removesuffix(originalText[-1])
  elif keydownEvent.key == pygame.K_SPACE:
    if (len(originalText) + 1) <= maxCharacters:
      originalText += " "
  elif len(pygame.key.name(keydownEvent.key)) < 2:
    if (len(originalText) + len(pygame.key.name(keydownEvent.key))) <= maxCharacters:
      originalText += keydownEvent.unicode
  
  return originalText

def login():
  checkMouse = False
  username = ""
  password = ""
  currentTextBox = None
  failedToLogin = False

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        shutdownGameClient()
        pygame.quit()
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True
      if event.type == pygame.KEYDOWN:
        if currentTextBox == "username":
          username = writeInTextBox(username, 16, event)
        elif currentTextBox == "password":
          password = writeInTextBox(password, 24, event)
    
    globalVariables["screen"].fill((0, 255, 255))
    pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] / 2) - 100, (globalVariables["screenHeight"] / 2) - 100, 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 255, 254), ((globalVariables["screenWidth"] / 2) - 100, (globalVariables["screenHeight"] / 2), 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) - 65, (globalVariables["screenHeight"] / 2) + 100, 130, 60))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 0), ((globalVariables["screenWidth"] / 2) - 115, globalVariables["screenHeight"] - 60, 230, 25))

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
        break
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
        sendAMessage({"action":"login", "contents":{"username":username, "password":password}})
        time.sleep(0.1)

        if globalVariables["username"] != None:
          break
        else:
          failedToLogin = True

      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 255, 255, 255):
        currentTextBox = "username"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 255, 254, 255):
        currentTextBox = "password"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 255, 255):
        currentTextBox = None

      checkMouse = False

    hiddenPassword = ""

    for letter in password:
      hiddenPassword += "*"

    if failedToLogin:
      writeText("freesansbold.ttf", 25, "Username or password is incorrect.", (255, 0, 0), ((globalVariables["screenWidth"] / 2) + 75, (globalVariables["screenHeight"] / 2) - 25))
    
    writeText("freesansbold.ttf", 60, "Login", (0, 0, 0), (globalVariables["screenWidth"] / 2, 75))
    writeText("freesansbold.ttf", 45, "Username:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 200, (globalVariables["screenHeight"] / 2) - 75))
    writeText("freesansbold.ttf", 43, "Password:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 200, (globalVariables["screenHeight"] / 2) + 25))
    writeText("freesansbold.ttf", 35, "Login", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 130))
    writeText("freesansbold.ttf", 28, "Don't have an account?", (0, 0, 0), (globalVariables["screenWidth"] / 2, globalVariables["screenHeight"] - 48))
    writeText("freesansbold.ttf", 40, username, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 50, (globalVariables["screenHeight"] / 2) - 75))
    writeText("freesansbold.ttf", 25, str(len(username)) + "/16", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 205, (globalVariables["screenHeight"] / 2) - 75))
    writeText("freesansbold.ttf", 40, hiddenPassword, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 40, (globalVariables["screenHeight"] / 2) + 30))
    writeText("freesansbold.ttf", 25, str(len(password)) + "/24", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 205, (globalVariables["screenHeight"] / 2) + 25))
    
    pygame.display.flip()