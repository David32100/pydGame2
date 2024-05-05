import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText
from client.communications import sendAMessage

def drawAccountInfoScreen():
  writeText("freesansbold.ttf", 35, "Account Information", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Username:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, str(globalVariables["username"]), (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 30, "Discovered levels:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
  writeText("freesansbold.ttf", 30, str(globalVariables["discoveredLevels"]), (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))
  writeText("freesansbold.ttf", 30, "Password security:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 250))
  writeText("freesansbold.ttf", 30, "Your password is kept safe.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 275))
  writeText("freesansbold.ttf", 30, "Hackers can't access your", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 300))
  writeText("freesansbold.ttf", 30, "password and even if they do,", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 325))
  writeText("freesansbold.ttf", 30, "it is encrypted, so they", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 350))
  writeText("freesansbold.ttf", 30, "don't get your actual password.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 375))

def drawChangeUsernameScreen(checkMouse, password, newUsername, currentTextBox):
  writeText("freesansbold.ttf", 35, "Change Username", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Change your username.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 125))
  writeText("freesansbold.ttf", 30, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  pygame.draw.rect(globalVariables["screen"], (255, 255, 254), ((globalVariables["screenWidth"] * (3 / 4)) - 35, 185, 180, 35))
  pygame.draw.rect(globalVariables["screen"], (255, 255, 253), ((globalVariables["screenWidth"] * (3 / 4)) - 35, 260, 180, 35))
  pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 36, 184, 182, 37), 1)
  pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 36, 259, 182, 37), 1)
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 325, 100, 50))
  
  if checkMouse:
    screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())
    
  hiddenPassword = ""

  for letter in password:
    hiddenPassword += "*"

  writeText("freesansbold.ttf", 25, str(hiddenPassword), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 55, 205))
  writeText("freesansbold.ttf", 25, str(newUsername), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 55, 275))
  writeText("freesansbold.ttf", 25, "Password:", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 105, 200))
  writeText("freesansbold.ttf", 25, "New username:", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 105, 275))
  writeText("freesansbold.ttf", 30, "Change", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 350))

  if checkMouse:
    if screenColor == (255, 255, 254, 255):
      return "password"
    elif screenColor == (255, 255, 253, 255):
      return "newUsername"
    elif screenColor == (1, 0, 0, 255):
      if globalVariables["party"] == None:
        sendAMessage({"action":"changeUsername", "contents":{"password":password, "newUsername":newUsername, "username":globalVariables["username"]}})
        return None
    else:
      return ""
    
  return currentTextBox

def drawChangePasswordScreen(checkMouse, oldPassword, newPassword, currentTextBox):
  writeText("freesansbold.ttf", 35, "Change password", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Change your password.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 125))
  writeText("freesansbold.ttf", 30, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  pygame.draw.rect(globalVariables["screen"], (255, 255, 254), ((globalVariables["screenWidth"] * (3 / 4)) - 35, 185, 200, 35))
  pygame.draw.rect(globalVariables["screen"], (255, 255, 253), ((globalVariables["screenWidth"] * (3 / 4)) - 35, 260, 200, 35))
  pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 36, 184, 202, 37), 1)
  pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 36, 259, 202, 37), 1)
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 325, 100, 50))

  if checkMouse:
    screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())
    
  writeText("freesansbold.ttf", 20, str(oldPassword), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 65, 200))
  writeText("freesansbold.ttf", 20, str(newPassword), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 65, 275))
  writeText("freesansbold.ttf", 25, "Old password:", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 105, 200))
  writeText("freesansbold.ttf", 25, "New password:", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 105, 275))
  writeText("freesansbold.ttf", 30, "Change", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 350))
  
  if checkMouse:
    if screenColor == (255, 255, 254, 255):
      return "oldPassword"
    elif screenColor == (255, 255, 253, 255):
      return "newPassword"
    elif screenColor == (1, 0, 0, 255):
      sendAMessage({"action":"changePassword", "contents":{"oldPassword":oldPassword, "newPassword":newPassword, "username":globalVariables["username"]}})
      return None
    else:
      return ""

  return currentTextBox

def drawLogOutScreen(checkMouse):
  writeText("freesansbold.ttf", 35, "Log out", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Do you want to log out?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    globalVariables["veiwingHomeScreen"] = False
    globalVariables["loggingIn"] = True

    if globalVariables["party"] != None:
      sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})
      globalVariables["party"] = None

    globalVariables["status"] = "Offline"
    sendAMessage({"action":"saveProgress", "contents":{"username":globalVariables["username"], "discoveredLevels":globalVariables["discoveredLevels"], "currentLevel":globalVariables["currentLevel"]}})
    sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
    sendAMessage({"action": "leaveServer", "contents":{"username":globalVariables["username"]}})
    globalVariables["username"] = None
    return False

  writeText("freesansbold.ttf", 30, "Log out", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
  return True

def drawDeleteAccountScreen(checkMouse):
  writeText("freesansbold.ttf", 35, "Delete account", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Are you sure you want to", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "delete your account?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 30, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    if globalVariables["party"] != None:
      sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

    sendAMessage({"action":"deleteAccount", "contents":{"username":globalVariables["username"]}})
    globalVariables["veiwingHomeScreen"] = False
    globalVariables["status"] = "Offline"
    globalVariables["loggingIn"] = True
    globalVariables["username"] = None
    return False

  writeText("freesansbold.ttf", 30, "Delete", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
  return True