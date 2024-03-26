import pygame
import shutil
import sys

from globalVariables import globalVariables
from drawingFunctions import writeText
from client.communications import sendAMessage, shutdownGameClient

emailPeices = []

def drawVolumeScreen(checkMouse, newUserSettings):
  writeText("freesansbold.ttf", 35, "Volume", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 10, 100))
  writeText("freesansbold.ttf", 30, "The volume of all the", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "music in the game.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 30, str(newUserSettings["volume"]), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 12.5, 275))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 112, 250, 50, 50))
  pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 37, 250, 50, 50))

  if checkMouse:
    screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())
    if screenColor == (1, 0, 0, 255) and newUserSettings["volume"] > 0:
      newUserSettings["volume"] -= 1
    elif screenColor == (2, 0, 0, 255) and newUserSettings["volume"] < 100:
      newUserSettings["volume"] += 1

  writeText("freesansbold.ttf", 30, "+", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 62.5, 275))
  writeText("freesansbold.ttf", 30, "-", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 86, 275))

def drawReportScreen():
  writeText("freesansbold.ttf", 35, "Reoprt", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "To report a bug or player,", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "send an email to:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 30, "david.gross@rkyhs.org", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 205))
  writeText("freesansbold.ttf", 30, "with the subject:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 235))
  writeText("freesansbold.ttf", 30, "GameTitle Report", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 265))

def drawCreditsScreen():
  writeText("freesansbold.ttf", 35, "Credits", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 35, "Main programmer:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "David Gross", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 35, "Main graphics designer:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))
  writeText("freesansbold.ttf", 30, "Eitan F", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 250))
  writeText("freesansbold.ttf", 35, "SFX and music:", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 300))
  writeText("freesansbold.ttf", 30, "Shlomo R", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 325))
  writeText("freesansbold.ttf", 30, "Sammy A", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 350))

def drawResetSettingsScreen(checkMouse, newUserSettings):
  writeText("freesansbold.ttf", 35, "Reset settings", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Are you sure you want to", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "reset all your settings?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 250, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    newUserSettings["volume"] = 100
    newUserSettings["playerColor"] = (0, 0, 255)
    newUserSettings["anonymouse"] = False
    newUserSettings["hideTextChat"] =  False
    newUserSettings["controls"] = {"jump":[pygame.K_UP, pygame.K_SPACE, pygame.K_w], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d], "talk":[pygame.K_BACKQUOTE]}

  writeText("freesansbold.ttf", 30, "Reset", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 275))

def drawDeleteSaveScreen(checkMouse):
  writeText("freesansbold.ttf", 35, "Delete save", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "Are you sure you want to", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "delete your save data?", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 30, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    sendAMessage({"action":"deleteSave", "contents":{"username":globalVariables["username"]}})
    globalVariables["veiwingHomeScreen"] = False

    if globalVariables["party"] != None:
      sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

    globalVariables["status"] = "Offline"
    sendAMessage({"action": "signOut", "contents":{"username":globalVariables["username"]}})
    globalVariables["loggingIn"] = True
    globalVariables["username"] = None
    return False

  writeText("freesansbold.ttf", 30, "Delete", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), 300))
  return True

def drawUninstallGameScreen(checkMouse):
  writeText("freesansbold.ttf", 35, "Uninstall Game", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
  writeText("freesansbold.ttf", 30, "This can be done manually.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
  writeText("freesansbold.ttf", 30, "Your account will be deleted!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))
  writeText("freesansbold.ttf", 37, "This can't be undone!", (255, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 200))
  pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 50, 275, 100, 50))

  if checkMouse and globalVariables["screen"].get_at(pygame.mouse.get_pos()) == (1, 0, 0, 255):
    globalVariables["veiwingHomeScreen"] = False
    globalVariables["loggingIn"] = False

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