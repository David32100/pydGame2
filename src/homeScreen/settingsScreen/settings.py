import pygame

from game.jumper import jumper
from account.login import writeInTextBox
from globalVariables import globalVariables
from drawingFunctions import writeText
from client.communications import sendAMessage, shutdownGame, condition
from homeScreen.settingsScreen.generalSettings import drawVolumeScreen, drawReportScreen, drawCreditsScreen, drawResetSettingsScreen, drawDeleteSaveScreen, drawUninstallGameScreen
from homeScreen.settingsScreen.playerSettings import drawPlayerColorScreen, drawAnonymousModeScreen, drawHideTextChatScreen
from homeScreen.settingsScreen.accountSettings import drawAccountInfoScreen, drawChangeUsernameScreen, drawChangePasswordScreen, drawLogOutScreen, drawDeleteAccountScreen
from homeScreen.settingsScreen.controlsSettings import drawJumpingScreen, drawMovingLeftScreen, drawMovingRightScreen, drawTalkingScreen

boxColor = (127, 0, 0, 255)

def drawSettingsBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) + 230, (globalVariables["screenHeight"] / 2) - 230, 100, 40))
  
def drawSettingsText(writeText):
  writeText("freesansbold.ttf", 30, "Settings", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 280, (globalVariables["screenHeight"] / 2) - 210))

def settings():
  global error
  newUserSettings = globalVariables["userSettings"]
  changingSettings = True
  checkMouse = False
  maxScroll = 120
  scroll = 0
  settingsBoxes = ["Volume", "Report", "Reset settings", "Delete save", "Credits", "Uninstall game"]
  currentSettingsBox = None
  globalVariables["screen"].fill((0, 255, 255))
  currentTextBox = None
  oldPassword = ""
  newPassword = ""
  password = ""
  newUsername = ""
  addingButton = False
  buttonPressed = False

  while changingSettings:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        changingSettings = False
        shutdownGame()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True
      elif event.type == pygame.KEYDOWN:
        if currentTextBox == "password":
          password = writeInTextBox(password, 16, event)
        elif currentTextBox == "newUsername":
          newUsername = writeInTextBox(newUsername, 16, event)
        elif currentTextBox == "oldPassword":
          oldPassword = writeInTextBox(oldPassword, 24, event)
        elif currentTextBox == "newPassword":
          newPassword = writeInTextBox(newPassword, 24, event)
        
        if addingButton:
          buttonPressed = event.key

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

      if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (0, 0, settingsBoxesIndex + 1, 255):
        currentSettingsBox = settingsBoxes[settingsBoxesIndex]

      writeText("freesansbold.ttf", 30, settingsBoxes[settingsBoxesIndex], (255, 255, 255), (175, (75 * (settingsBoxesIndex + 1)) + scroll + 25))
    
    if currentSettingsBox == "Volume":
      drawVolumeScreen(checkMouse, newUserSettings)
    elif currentSettingsBox == "Report":
      drawReportScreen()  
    elif currentSettingsBox == "Credits":
      drawCreditsScreen()
    elif currentSettingsBox == "Reset settings":
      drawResetSettingsScreen(checkMouse, newUserSettings)
    elif currentSettingsBox == "Delete save":
      changingSettings = drawDeleteSaveScreen(checkMouse)
    elif currentSettingsBox == "Uninstall game":
      drawUninstallGameScreen(checkMouse)
    elif currentSettingsBox == "Player color":
      drawPlayerColorScreen(checkMouse, newUserSettings)
    elif currentSettingsBox == "Anonymous mode":
      drawAnonymousModeScreen(checkMouse, newUserSettings)
    elif currentSettingsBox == "Hide text chat":
      drawHideTextChatScreen(checkMouse, newUserSettings)
    elif currentSettingsBox == "Other stuff":
      writeText("freesansbold.ttf", 35, "Other Stuff", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
      writeText("freesansbold.ttf", 30, "Other stuff, like apples.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
    elif currentSettingsBox == "Account info":
      drawAccountInfoScreen()
    elif currentSettingsBox == "Change username":
      currentTextBox = drawChangeUsernameScreen(checkMouse, password, newUsername, currentTextBox)

      if currentTextBox == None:
        password = ""
        newUsername = ""
      elif currentTextBox == "break":
        break

    elif currentSettingsBox == "Change password":
      currentTextBox = drawChangePasswordScreen(checkMouse, oldPassword, newPassword, currentTextBox)

      if currentTextBox == None:
        oldPassword = ""
        newPassword = ""
      elif currentTextBox == "break":
        break

    elif currentSettingsBox == "Log out":
      changingSettings = drawLogOutScreen(checkMouse)
    elif currentSettingsBox == "Delete account":
      changingSettings = drawDeleteAccountScreen(checkMouse)
    elif currentSettingsBox == "Jumping":
      addingButton = drawJumpingScreen(checkMouse, newUserSettings, addingButton, buttonPressed)
    elif currentSettingsBox == "Moving left":
      addingButton = drawMovingLeftScreen(checkMouse, newUserSettings, addingButton, buttonPressed)
    elif currentSettingsBox == "Moving right":
      addingButton = drawMovingRightScreen(checkMouse, newUserSettings, addingButton, buttonPressed)
    elif currentSettingsBox == "Talking":
      addingButton = drawTalkingScreen(checkMouse, newUserSettings, addingButton, buttonPressed)

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
    buttonPressed = None

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
        password = ""
        newUsername = ""
        currentTextBox = None
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
        condition.acquire()
        l = 0

        while l < 4:
          if not condition.wait(1):
            sendAMessage({"action":"updateSettings", "contents":{"settings":newUserSettings, "username":globalVariables["username"]}})
            l += 1
          else:
            break
        
        condition.release()
        
        if l == 4:
          globalVariables["veiwingHomeScreen"] = False
          globalVariables["loggingIn"] = True
          globalVariables["username"] = None
          globalVariables["connectedToServer"] = False
          break
        
        globalVariables["userSettings"] = newUserSettings
        pygame.mixer.music.set_volume(globalVariables["userSettings"]["volume"] / 100)
        
        if globalVariables["userSettings"]["anonymous"]:
          sendAMessage({"action":"anonymousModeOn", "contents":{"username":globalVariables["username"]}})
          condition.acquire()
          l = 0

          while l < 4:
            if not condition.wait(1):
              sendAMessage({"action":"anonymousModeOn", "contents":{"username":globalVariables["username"]}})
              l += 1
            else:
              break
          
          condition.release()
          
          if l == 4:
            globalVariables["veiwingHomeScreen"] = False
            globalVariables["loggingIn"] = True
            globalVariables["username"] = None
            globalVariables["connectedToServer"] = False
            break

        else:
          sendAMessage({"action":"anonymousModeOff", "contents":{"username":globalVariables["username"]}})
          condition.acquire()
          l = 0

          while l < 4:
            if not condition.wait(1):
              sendAMessage({"action":"anonymousModeOff", "contents":{"username":globalVariables["username"]}})
              l += 1
            else:
              break
          
          condition.release()
          
          if l == 4:
            globalVariables["veiwingHomeScreen"] = False
            globalVariables["loggingIn"] = True
            globalVariables["username"] = None
            globalVariables["connectedToServer"] = False
            break

        jumper.resetJumper()

      checkMouse = False

    writeText("freesansbold.ttf", 30, "General", (0, 0, 0), ((globalVariables["screenWidth"] / 4) - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Player", (0, 0, 0), ((globalVariables["screenWidth"] * (1 / 2)) - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Account", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Controls", (0, 0, 0), (globalVariables["screenWidth"] - 87.5, 28))
    writeText("freesansbold.ttf", 30, "Back", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 5)) + 62.5, 452))
    writeText("freesansbold.ttf", 30, "Save", (0, 0, 0), ((globalVariables["screenWidth"] / 4) + 62.5, 452))
    pygame.display.flip()

settingsEvent = (boxColor, settings)