import pygame
import sys
import time
import hashlib

from client.communications import shutdownGameClient, sendAMessage
from account.login import writeInTextBox
from globalVariables import globalVariables
from drawingFunctions import writeText

def signUp():
  currentTextBox = None
  username = ""
  password = ""
  reenteredPassword = ""
  checkMouse = False
  errorMessage = ""

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        shutdownGameClient()
        pygame.quit()
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True
      elif event.type == pygame.KEYDOWN:
        if currentTextBox == "username":
          username = writeInTextBox(username, 16, event)
        elif currentTextBox == "password":
          password = writeInTextBox(password, 24, event)
        elif currentTextBox == "reenteredPassword":
          reenteredPassword = writeInTextBox(reenteredPassword, 24, event)

    globalVariables["screen"].fill((0, 255, 255))
    pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 103, (globalVariables["screenHeight"] / 2) - 148, 356, 56), 3)
    pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 103, (globalVariables["screenHeight"] / 2) - 63, 356, 56), 3)
    pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 103, (globalVariables["screenHeight"] / 2) + 22, 356, 56), 3)
    pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] / 2) - 100, (globalVariables["screenHeight"] / 2) - 145, 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 255, 254), ((globalVariables["screenWidth"] / 2) - 100, (globalVariables["screenHeight"] / 2) - 60, 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 255, 253), ((globalVariables["screenWidth"] / 2) - 100, (globalVariables["screenHeight"] / 2) + 25, 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) - 65, (globalVariables["screenHeight"] / 2) + 100, 130, 60))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 0), ((globalVariables["screenWidth"] / 2) - 125, globalVariables["screenHeight"] - 60, 250, 25))

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
        break
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
        if password == reenteredPassword:
          sendAMessage({"action":"signUp", "contents":{"username":username, "password":hashlib.sha256(password.encode("utf-8")).hexdigest()}})
          time.sleep(0.1)

          if globalVariables["username"] != None:
            break
          else:
            errorMessage = "Account already exists."
        else:
          errorMessage = "Password doesn't match re-entered password."

      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 255, 255, 255):
        currentTextBox = "username"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 255, 254, 255):
        currentTextBox = "password"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 255, 253, 255):
        currentTextBox = "reenteredPassword"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 255, 255):
        currentTextBox = None

      checkMouse = False

    hiddenPassword = ""
    hiddenReenteredPassword = ""

    for letter in password:
      hiddenPassword += "*"

    for letter in reenteredPassword:
      hiddenReenteredPassword += "*"

    writeText("freesansbold.ttf", 25, errorMessage, (255, 0, 0), ((globalVariables["screenWidth"] / 2) + 75, (globalVariables["screenHeight"] / 2) + 8))
    writeText("freesansbold.ttf", 60, "Sign Up", (0, 0, 0), (globalVariables["screenWidth"] / 2, 50))
    writeText("freesansbold.ttf", 45, "Username:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 200, (globalVariables["screenHeight"] / 2) - 120))
    writeText("freesansbold.ttf", 43, "Password:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 200, (globalVariables["screenHeight"] / 2) - 35))
    writeText("freesansbold.ttf", 34, "Re-enter Password:", (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 225, (globalVariables["screenHeight"] / 2) + 50))
    writeText("freesansbold.ttf", 35, "Sign Up", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 130))
    writeText("freesansbold.ttf", 28, "Already have an account?", (0, 0, 0), (globalVariables["screenWidth"] / 2, globalVariables["screenHeight"] - 48))
    writeText("freesansbold.ttf", 35, username, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 50, (globalVariables["screenHeight"] / 2) - 120))
    writeText("freesansbold.ttf", 25, str(len(username)) + "/16", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 205, (globalVariables["screenHeight"] / 2) - 120))
    writeText("freesansbold.ttf", 30, hiddenPassword, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 40, (globalVariables["screenHeight"] / 2) - 30))
    writeText("freesansbold.ttf", 25, str(len(password)) + "/24", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 205, (globalVariables["screenHeight"] / 2) - 35))
    writeText("freesansbold.ttf", 30, hiddenReenteredPassword, (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 40, (globalVariables["screenHeight"] / 2) + 55))
    writeText("freesansbold.ttf", 25, str(len(reenteredPassword)) + "/24", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 205, (globalVariables["screenHeight"] / 2) + 50))
    
    pygame.display.flip()