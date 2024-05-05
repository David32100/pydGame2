import pygame
import sys
import time

from globalVariables import globalVariables
from drawingFunctions import writeText
from client.communications import shutdownGameClient, sendAMessage, loginFailed, condition

backspaceKeyPressed = False

def writeInTextBox(originalText:str, maxCharacters:int, keyEvents:pygame.event.Event, deleteTextLoop:bool=False):
  """
  To use in an event loop
  deleteTextLoop: boolean - If there is a deleteTextLoop() function for this text box, default is False
  """
  global backspaceKeyPressed

  if keyEvents.type == pygame.KEYDOWN:
    if keyEvents.key == pygame.K_BACKSPACE:
      if len(originalText) > 0 and not deleteTextLoop:
        originalText = originalText.removesuffix(originalText[-1])
    elif keyEvents.key == pygame.K_SPACE and (len(originalText) + 1) <= maxCharacters:
      originalText += " "
    elif len(pygame.key.name(keyEvents.key)) < 2 and (len(originalText) + len(pygame.key.name(keyEvents.key))) <= maxCharacters:
      originalText += keyEvents.unicode
  else:
    print("ERROR: keyEvents is not a pygame.KEYDOWN event! src/account/login.py Ln 23 \nOriginal text:", originalText, "\nMax characters:", maxCharacters)

  return originalText

def deleteTextLoop(originalText:str):
  """
  To use with writeInTextBox() outside of event loop
  """
  global backspaceKeyPressed

  if pygame.key.get_pressed()[pygame.K_BACKSPACE] and len(originalText) > 0:
    originalText = originalText.removesuffix(originalText[-1])
    time.sleep(0.1)

  return originalText  

def login():
  global loginFailed
  checkMouse = False
  username = ""
  password = ""
  currentTextBox = None
  error = ""

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
    pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 103, (globalVariables["screenHeight"] / 2) - 103, 356, 56), 3)
    pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 103, (globalVariables["screenHeight"] / 2) - 3, 356, 56), 3)
    pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] / 2) - 100, (globalVariables["screenHeight"] / 2) - 100, 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 255, 254), ((globalVariables["screenWidth"] / 2) - 100, globalVariables["screenHeight"] / 2, 350, 50))
    pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) - 65, (globalVariables["screenHeight"] / 2) + 100, 130, 60))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 0), ((globalVariables["screenWidth"] / 2) - 115, globalVariables["screenHeight"] - 60, 230, 25))

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
        break
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
        sendAMessage({"action":"login", "contents":{"username":username, "password":password}})
        condition.acquire()
        condition.wait(1.5)

        if globalVariables["username"] != None:
          globalVariables["veiwingHomeScreen"] = True
          break
        else:
          from client.communications import loginFailed
          error = loginFailed

        condition.release()
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

    writeText("freesansbold.ttf", 25, error, (255, 0, 0), ((globalVariables["screenWidth"] / 2) + 75, (globalVariables["screenHeight"] / 2) - 25))
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