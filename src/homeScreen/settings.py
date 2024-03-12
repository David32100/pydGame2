import pygame
import email
import smtplib
import ssl
import shutil
import sys

from client.communications import shutdownGameClient

def sendEmail(subject:str, message:str):
  messageToSend = """\
  From: David Gross <David.Gross@rkyhs.org>
  Subject: Test message
  
  Body would go here"""

  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login("David.Gross@rkyhs.org", "")
    server.sendmail("David.Gross@rkyhs.org", "David.Gross@rkyhs.org", messageToSend)

from globalVariables import globalVariables
from drawingFunctions import shutdownGame, writeText
from client.communications import sendAMessage

boxColor = (127, 0, 0, 255)

def drawSettingsBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) + 230, (globalVariables["screenHeight"] / 2) - 230, 100, 40))
  
def drawSettingsText(writeText):
  writeText("freesansbold.ttf", 30, "Settings", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 280, (globalVariables["screenHeight"] / 2) - 210))

def settings():
  playerColors = {"Grey": (125, 125, 125), "Red": (255, 0, 0), "Green": (0, 255, 0), "Blue": (0, 0, 255), "Purple": (255, 0, 255)}
  
  for i in range(len(playerColors)):
    if list(playerColors.values())[i] == globalVariables["userSettings"]["playerColor"]:
      playerColorsIndex = i

  newUserSettings = globalVariables["userSettings"]
  changingSettings = True
  checkMouse = False
  maxScroll = 120
  scroll = 0
  settingsBoxes = ["Volume", "Report", "Reset settings", "Delete save", "Credits", "Uninstall game"]
  currentSettingsBox = None
  globalVariables["screen"].fill((0, 255, 255))

  while changingSettings:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        changingSettings = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_UP] and scroll < 0:
      scroll += 1
    elif pressedKeys[pygame.K_DOWN] and scroll > -maxScroll:
      scroll -= 1

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

    globalVariables["screen"].fill((0, 255, 255))

    for settingsBoxesIndex in range(len(settingsBoxes)):
      pygame.draw.rect(globalVariables["screen"], (0, 0, settingsBoxesIndex + 1), (75, (75 * (settingsBoxesIndex + 1)) + scroll, 200, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 0, settingsBoxesIndex + 1, 255):
        currentSettingsBox = settingsBoxes[settingsBoxesIndex]

      writeText("freesansbold.ttf", 30, settingsBoxes[settingsBoxesIndex], (255, 255, 255), (175, (75 * (settingsBoxesIndex + 1)) + scroll + 25))
    
    if currentSettingsBox == "Volume":
      writeText("freesansbold.ttf", 35, "Volume", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 10, 100))
      writeText("freesansbold.ttf", 30, "The volume of all the", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "music in the game.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      writeText("freesansbold.ttf", 30, str(newUserSettings["volume"]), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 12.5, 275))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 112, 250, 50, 50))
      pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 37, 250, 50, 50))

      if checkMouse:
        if globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255) and newUserSettings["volume"] > 0:
          newUserSettings["volume"] -= 1
        elif globalVariables["screen"].get_at((mouseX, mouseY)) == (2, 0, 0, 255) and newUserSettings["volume"] < 100:
          newUserSettings["volume"] += 1

      writeText("freesansbold.ttf", 30, "+", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 62.5, 275))
      writeText("freesansbold.ttf", 30, "-", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 86, 275))
    
    elif currentSettingsBox == "Report":
      writeText("freesansbold.ttf", 35, "Report", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Report a bug or player.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
    
    elif currentSettingsBox == "Credits":
      writeText("freesansbold.ttf", 35, "Credits", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 35, "Main programmer:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "David Gross", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      writeText("freesansbold.ttf", 35, "Main graphics designer:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))
      writeText("freesansbold.ttf", 30, "Eitan F", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 250))
      writeText("freesansbold.ttf", 35, "SFX and music:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 300))
      writeText("freesansbold.ttf", 30, "Shlomo R", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 325))
      writeText("freesansbold.ttf", 30, "Sammy A", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 350))
    
    elif currentSettingsBox == "Reset settings":
      writeText("freesansbold.ttf", 35, "Reset settings", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Are you sure you want to", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "reset all your settings?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 250, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        newUserSettings["volume"] = 100
        newUserSettings["playerColor"] = (0, 0, 255)
        newUserSettings["anonymouse"] = False
        newUserSettings["hideTextChat"] =  False

      writeText("freesansbold.ttf", 30, "Yes", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 275))
    
    elif currentSettingsBox == "Delete save":
      writeText("freesansbold.ttf", 35, "Delete save", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Are you sure you want to", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "delete your save data?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      writeText("freesansbold.ttf", 30, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        sendAMessage({"action":"deleteSave", "contents":{"username":globalVariables["username"]}})
        globalVariables["veiwingHomeScreen"] = False
        changingSettings = False

        if globalVariables["party"] != None:
          sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

        globalVariables["status"] = "Offline"
        sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
        globalVariables["loggingIn"] = True
        globalVariables["username"] = None

      writeText("freesansbold.ttf", 30, "Yes", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
    
    elif currentSettingsBox == "Uninstall game":
      writeText("freesansbold.ttf", 35, "Uninstall Game", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "This can be done manually.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "Your account will be deleted!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      writeText("freesansbold.ttf", 37, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        globalVariables["veiwingHomeScreen"] = False
        globalVariables["loggingIn"] = False
        changingSettings = False

        if globalVariables["party"] != None:
          sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

        globalVariables["status"] = "Offline"
        sendAMessage({"action":"deleteAccount", "contents":{"username":globalVariables["username"]}})
        sendAMessage({"action": "leaveServer", "contents":{"username":globalVariables["username"]}})
        sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
        shutdownGameClient()
        pygame.quit()
        # Change to pydGame2 on a copy of the game DO NOT DELETE THE ONLY COPY!!!
        shutil.rmtree("/home/david321/Documents/pydGame3")
        sys.exit()

      writeText("freesansbold.ttf", 30, "Uninstall", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
    
    elif currentSettingsBox == "Player color":
      writeText("freesansbold.ttf", 35, "Player Color", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Choose your character's color!", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 130, 250, 80, 50))
      pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 50, 250, 80, 50))

      if checkMouse:
        if globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
          if playerColorsIndex > 0:
            playerColorsIndex -= 1
          else:
            playerColorsIndex = len(playerColors) - 1
        elif globalVariables["screen"].get_at((mouseX, mouseY)) == (2, 0, 0, 255):
          if playerColorsIndex < (len(playerColors) - 1):
            playerColorsIndex += 1
          else:
            playerColorsIndex = 0

      writeText("freesansbold.ttf", 30, "Next", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 90, 275))
      writeText("freesansbold.ttf", 30, "Back", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 90, 275))
      writeText("freesansbold.ttf", 30, str(list(playerColors.keys())[playerColorsIndex]), (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 275))
      newUserSettings["playerColor"] = list(playerColors.values())[playerColorsIndex]

    elif currentSettingsBox == "Anonymous mode":
      writeText("freesansbold.ttf", 35, "Anonymous mode", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Hide your username, discovered", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "levels, and current level.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        newUserSettings["anonymous"] = not newUserSettings["anonymous"]
      
      if newUserSettings["anonymous"]:
        writeText("freesansbold.ttf", 30, "On", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
      else:
        writeText("freesansbold.ttf", 30, "Off", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))

    elif currentSettingsBox == "Hide text chat":
      writeText("freesansbold.ttf", 35, "Hide Text Chat", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Hide the text chat.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        newUserSettings["hideTextChat"] = not newUserSettings["hideTextChat"]
      
      if newUserSettings["hideTextChat"]:
        writeText("freesansbold.ttf", 30, "Hidden", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
      else:
        writeText("freesansbold.ttf", 30, "Shown", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))

    elif currentSettingsBox == "Other stuff":
      writeText("freesansbold.ttf", 35, "Other Stuff", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Other stuff, like apples.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))

    elif currentSettingsBox == "Account info":
      writeText("freesansbold.ttf", 35, "Account Information", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Username:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, str(globalVariables["username"]), (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      writeText("freesansbold.ttf", 30, "Discovered levels:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
      writeText("freesansbold.ttf", 30, str(globalVariables["discoveredLevels"]), (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))
      writeText("freesansbold.ttf", 30, "Password security:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 250))
      writeText("freesansbold.ttf", 30, "Your password is kept safe.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 275))
      writeText("freesansbold.ttf", 30, "Hackers can't access your", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 300))
      writeText("freesansbold.ttf", 30, "password and even if they do,", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 325))
      writeText("freesansbold.ttf", 30, "it is hashed and salted, so they", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 350))
      writeText("freesansbold.ttf", 30, "don't get your actual password.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 375))

    elif currentSettingsBox == "Change username":
      pass

    elif currentSettingsBox == "Change password":
      pass

    elif currentSettingsBox == "Log out":
      writeText("freesansbold.ttf", 35, "Log out", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Do you want to log out?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        globalVariables["veiwingHomeScreen"] = False
        globalVariables["loggingIn"] = True
        changingSettings = False

        if globalVariables["party"] != None:
          sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

        globalVariables["status"] = "Offline"
        sendAMessage({"action":"saveProgress", "contents":{"username":globalVariables["username"], "discoveredLevels":globalVariables["discoveredLevels"], "currentLevel":globalVariables["currentLevel"]}})
        sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
        sendAMessage({"action": "leaveServer", "contents":{"username":globalVariables["username"]}})
        globalVariables["username"] = None

      writeText("freesansbold.ttf", 30, "Log out", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))

    elif currentSettingsBox == "Delete account":
      writeText("freesansbold.ttf", 35, "Delete account", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Are you sure you want to", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
      writeText("freesansbold.ttf", 30, "delete your account?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
      writeText("freesansbold.ttf", 30, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
      pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

      if checkMouse and globalVariables["screen"].get_at((mouseX, mouseY)) == (1, 0, 0, 255):
        sendAMessage({"action":"deleteAccount", "contents":{"username":globalVariables["username"]}})
        globalVariables["veiwingHomeScreen"] = False
        changingSettings = False

        if globalVariables["party"] != None:
          sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

        globalVariables["status"] = "Offline"
        sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
        globalVariables["loggingIn"] = True
        globalVariables["username"] = None

      writeText("freesansbold.ttf", 30, "Yes", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
    
    elif currentSettingsBox == "Jumping":
      pass

    elif currentSettingsBox == "Moving left":
      pass

    elif currentSettingsBox == "Moving right":
      pass

    elif currentSettingsBox == "Talking":
      pass

    pygame.draw.line(globalVariables["screen"], (0, 0, 0), (globalVariables["screenWidth"] / 2, 0), (globalVariables["screenWidth"] / 2, globalVariables["screenHeight"]))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (0, 0, globalVariables["screenWidth"], 60))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (0, 400, globalVariables["screenWidth"], globalVariables["screenHeight"] - 400))
    pygame.draw.line(globalVariables["screen"], (0, 0, 0), (10, 60), (globalVariables["screenWidth"] - 10, 60), 2)
    pygame.draw.line(globalVariables["screen"], (0, 0, 0), (10, 400), (globalVariables["screenWidth"] - 10, 400), 2)
     
    pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 4) - 137.5, 5, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 0), ((globalVariables["screenWidth"] * (1 / 2)) - 137.5, 5, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 0, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 137.5, 5, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (127, 0, 0), (globalVariables["screenWidth"] - 137.5, 5, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 127, 0), (globalVariables["screenWidth"] * (3 / 5), 420, 125, 63))
    pygame.draw.rect(globalVariables["screen"], (0, 0, 127), (globalVariables["screenWidth"] / 4, 420, 125, 63))

    if checkMouse:
      screenColor = globalVariables["screen"].get_at((mouseX, mouseY))

      if screenColor == (255, 0, 0, 255):
        maxScroll = 120
        scroll = 0
        currentSettingsBox = None
        settingsBoxes = ["Volume", "Report", "Reset settings", "Delete save", "Credits", "Uninstall game"]
      elif screenColor == (0, 255, 0, 255):
        maxScroll = 0
        scroll = 0
        currentSettingsBox = None
        settingsBoxes = ["Player color", "Anonymous mode", "Hide text chat", "Other stuff"]
      elif screenColor == (0, 0, 255, 255):
        maxScroll = 40
        scroll = 0
        currentSettingsBox = None
        settingsBoxes = ["Account info", "Change username", "Change password", "Log out", "Delete account"]
      elif screenColor == (127, 0, 0, 255):
        maxScroll = 0
        scroll = 0
        currentSettingsBox = None
        settingsBoxes = ["Jumping", "Moving left", "Moving right", "Talking"]
      elif screenColor == (0, 127, 0, 255):
        changingSettings = False
      elif screenColor == (0, 0, 127, 255):
        changingSettings = False
        sendAMessage({"action":"updateSettings", "contents":{"settings":newUserSettings, "username":globalVariables["username"]}})

      checkMouse = False

    writeText("freesansbold.ttf", 30, "General", (0, 0, 0), ((globalVariables["screenWidth"] / 4) - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Player", (0, 0, 0), ((globalVariables["screenWidth"] * (1 / 2)) - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Account", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Controls", (0, 0, 0), (globalVariables["screenWidth"] - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Back", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 5)) + 62.5, 452))
    writeText("freesansbold.ttf", 30, "Save", (0, 0, 0), ((globalVariables["screenWidth"] / 4) + 62.5, 452))

    pygame.display.flip()

settingsEvent = (boxColor, settings)