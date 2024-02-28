import pygame
import time

from globalVariables import globalVariables
from game.levels import levels
from client.communications import sendAMessage

sendJumpingMessage = False
text = ""

def drawGame():
  globalVariables["screen"].fill((0, 128, 128))
  
  for object in levels[globalVariables["currentLevel"]][2]:
    objectRect = levels[globalVariables["currentLevel"]][2][object]
    object.draw((objectRect[0] - globalVariables["scroll"], objectRect[1], objectRect[2], objectRect[3]))

def updateJumperPosition(jumper, keydownEvent):
  global talking
  pressedKeys = pygame.key.get_pressed()

  if globalVariables["jumping"]:
    jumper.jump()

    if not pressedKeys[pygame.K_RIGHT] and not pressedKeys[pygame.K_LEFT] and not pressedKeys[pygame.K_d] and not pressedKeys[pygame.K_a]:
      jumper.xVelocity = 0
      jumper.moveRight()
  else:
    if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_w] or pressedKeys[pygame.K_SPACE]:
      jumper.jump()

      if not pressedKeys[pygame.K_RIGHT] and not pressedKeys[pygame.K_LEFT] and not pressedKeys[pygame.K_a] and not pressedKeys[pygame.K_d]:
        jumper.xVelocity = 0
        jumper.moveRight()

      if jumper.canMove:
        sendAMessage({"action":"startJump", "contents":{"lobby":globalVariables["lobby"]}})
  
    if not pressedKeys[pygame.K_UP] and not pressedKeys[pygame.K_w] and not pressedKeys[pygame.K_SPACE]:
      jumper.stopJumping()
      sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"]}})

  if pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a]:
    jumper.moveLeft()

  if pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d]:
    jumper.moveRight()

  if not pressedKeys[pygame.K_LEFT] and not pressedKeys[pygame.K_RIGHT] and not pressedKeys[pygame.K_d] and not pressedKeys[pygame.K_a]:
    jumper.slowDownIfNotMoving()

  if pressedKeys[pygame.K_SLASH]:
    pressedKeyMods = pygame.key.get_mods()

    if pressedKeyMods & pygame.KMOD_SHIFT and pressedKeyMods & pygame.KMOD_CTRL:
      if jumper.canMove:
        jumper.canMove = False
        jumper.talking = True

  if jumper.talking:
    global text

    if keydownEvent != None:
      if keydownEvent.key == pygame.K_BACKSPACE:
        if len(text) > 0:
          text = text.removesuffix(text[-1])
      elif keydownEvent.key == pygame.K_SPACE:
        if (len(text) + 1) < 16:
          text += " "
      elif len(pygame.key.name(keydownEvent.key)) < 2:
        if (len(text) + len(pygame.key.name(keydownEvent.key))) < 16:
          text += keydownEvent.unicode

    if len(text) < 1:
      jumper.talk(" ")
    else:
      jumper.talk(text)

    if pressedKeys[pygame.K_RETURN]:
      sendAMessage({"action":"talk", "contents":{"username":globalVariables["username"], "text":text, "lobby":globalVariables["lobby"]}})
      globalVariables["timers"][str(globalVariables["username"]) + "'sTalkingTimer"] = [0, text]
      jumper.canMove = True
      jumper.talking = False
      text = ""

    if pressedKeys[pygame.K_SLASH]:
      pressedKeyMods = pygame.key.get_mods()

      if pressedKeyMods & pygame.KMOD_SHIFT and pressedKeyMods & pygame.KMOD_ALT:
        jumper.canMove = True
        jumper.talking = False
        text = ""

  jumper.experienceGravity()
  jumper.scrollScreen()
  jumper.winLevelIfTouchingGoal()
  jumper.dieIfTouchingBottom()
  jumper.drawJumper()
  sendAMessage({"action":"updatePlayer", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"], "position":(jumper.jumperXWithScroll, jumper.jumperY)}})
  
  for otherJumper in list(globalVariables["playersInLobby"].values()):
    otherJumper.drawJumper()
  
  for timer in list(globalVariables["timers"].keys()):
    if globalVariables["timers"][timer][0] < 5 * globalVariables["fps"]:
      if timer.split("'")[0] in globalVariables["playersInLobby"]:
        globalVariables["playersInLobby"][timer.split("'")[0]].talk(globalVariables["timers"][timer][1])
      elif timer.split("'")[0] == globalVariables["username"]:
        if not jumper.talking:
          jumper.talk(globalVariables["timers"][timer][1])
      else:
        globalVariables["timers"].pop(timer)

      globalVariables["timers"][timer][0] += 1
    else:
      globalVariables["timers"].pop(timer)

def drawGameAndUpdateJumperPosition(jumper, keydownEvent):
  drawGame()
  updateJumperPosition(jumper, keydownEvent)