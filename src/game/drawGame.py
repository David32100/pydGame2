import pygame

from globalVariables import globalVariables
from game.levels import levels
from client.communications import sendAMessage, leaveLobby, condition
from drawingFunctions import writeText
 
sendJumpingMessage = False
text = ""
moveLeftSpeed = 0.5
moveRightSpeed = 0.5
jumpHeight = 0.8

def drawAlphaRect(color:tuple, opacity:int, width:float, height:float, position:tuple) -> pygame.Surface:
  alphaRect = pygame.Surface((width, height))
  alphaRect.set_alpha(opacity)
  alphaRect.fill(color)
  globalVariables["screen"].blit(alphaRect, position)
  return alphaRect

def drawGame():
  globalVariables["screen"].fill((0, 128, 128))
  
  for object in levels[globalVariables["currentLevel"]][2]:
    object.draw(levels[globalVariables["currentLevel"]][2][object])

def updateJumperPosition(jumper, keydownEvent:pygame.event.Event):
  global text, moveLeftSpeed, moveRightSpeed, jumpHeight
  keyPressed = {"talk":False, "right":False, "left":False, "jump":False}
  pressedKeys = pygame.key.get_pressed()
  keyMods = pygame.key.get_mods()

  for keygroup in globalVariables["userSettings"]["controls"]:
    for key in globalVariables["userSettings"]["controls"][keygroup]:
      if pressedKeys[key]:
        keyPressed[keygroup] = True

  if globalVariables["jumping"]:
    jumper.jump(1)

    if not keyPressed["left"] and not keyPressed["right"]:
      jumper.xVelocity = 0
      jumper.moveRight(1)
  else:
    if keyPressed["jump"]:
      if jumper.canMove:
        sendAMessage({"action":"startJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
        condition.acquire()
        l = 0

        while l < 2:
          if not condition.wait(0.25):
            sendAMessage({"action":"startJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
            l += 1
          else:
            break
        
        condition.release()

        if l == 2:
          globalVariables["playingGame"] = False
          globalVariables["loggingIn"] = True
          globalVariables["username"] = None
          globalVariables["connectedToServer"] = False

      if keyMods & pygame.KMOD_SHIFT and jumper.checkJumperCollision(yDisplacement=1)["Bottom"]:
        jumpHeight = 1
      elif not keyMods & pygame.KMOD_SHIFT and jumper.checkJumperCollision(yDisplacement=1)["Bottom"]:
        jumpHeight = 0.8

      jumper.jump(jumpHeight)

      if not keyPressed["left"] and not keyPressed["right"]:
        jumper.xVelocity = 0
        jumper.moveRight(1)
    else:
      jumper.stopJumping()
      sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
      condition.acquire()
      l = 0

      while l < 2:
        if not condition.wait(0.3):
          sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
          l += 1
        else:
          break
      
      condition.release()

      if l == 2:
        globalVariables["playingGame"] = False
        globalVariables["loggingIn"] = True
        globalVariables["username"] = None
        globalVariables["connectedToServer"] = False

  if keyPressed["left"]:
    if keyMods & pygame.KMOD_SHIFT and jumper.checkJumperCollision(yDisplacement=1)["Bottom"]:
      moveLeftSpeed = 1
    elif not keyMods & pygame.KMOD_SHIFT and jumper.checkJumperCollision(yDisplacement=1)["Bottom"]:
      moveLeftSpeed = 0.5

    jumper.moveLeft(moveLeftSpeed)

  if keyPressed["right"]:
    if keyMods & pygame.KMOD_SHIFT and jumper.checkJumperCollision(yDisplacement=1)["Bottom"]:
      moveRightSpeed = 1
    elif not keyMods & pygame.KMOD_SHIFT and jumper.checkJumperCollision(yDisplacement=1)["Bottom"]:
      moveRightSpeed = 0.5

    jumper.moveRight(moveRightSpeed)

  if not keyPressed["left"] and not keyPressed["right"]:
    jumper.slowDownIfNotMoving()

  if keydownEvent != None:
    if keyPressed["talk"]:
      if jumper.canMove and not globalVariables["userSettings"]["hideTextChat"]:
        jumper.canMove = False
        jumper.talking = True
      elif jumper.talking:
        jumper.canMove = True
        jumper.talking = False
        text = ""

  if jumper.talking:
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
      condition.acquire()
      l = 0

      while l < 4:
        if not condition.wait(0.5):
          sendAMessage({"action":"talk", "contents":{"username":globalVariables["username"], "text":text, "lobby":globalVariables["lobby"]}})
          l += 1
        else:
          break
      
      condition.release()

      if l == 4:
        globalVariables["playingGame"] = False
        globalVariables["loggingIn"] = True
        globalVariables["username"] = None
        globalVariables["connectedToServer"] = False

      globalVariables["timers"][str(globalVariables["username"]) + "'sTalkingTimer"] = [0, text]
      jumper.canMove = True
      jumper.talking = False
      text = ""

  jumper.experienceGravity()
  jumper.scrollScreen()
  jumper.winLevelIfTouchingGoal()
  jumper.dieIfTouchingEnemy()
  jumper.dieIfTouchingBottom()
  jumper.drawJumper()
  sendAMessage({"action":"updatePlayer", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"], "position":(jumper.jumperXWithScroll, jumper.jumperY)}})

  for otherJumper in list(globalVariables["playersInLobby"].values()):
    otherJumper.drawJumper()

  if not globalVariables["userSettings"]["hideTextChat"]:
    for timer in list(globalVariables["timers"].keys()):
      if globalVariables["timers"][timer][0] < 5 * globalVariables["fps"]:
        if timer[:-14] in globalVariables["playersInLobby"]:
          globalVariables["playersInLobby"][timer[:-14]].talk(globalVariables["timers"][timer][1])
        elif timer[:-14] == globalVariables["username"]:
          if not jumper.talking:
            jumper.talk(globalVariables["timers"][timer][1])
        else:
          print("Error: Player with timer", timer, "is not in the lobby.")
          globalVariables["timers"].pop(timer)

        globalVariables["timers"][timer][0] += 1
      else:
        globalVariables["timers"].pop(timer)

def drawPauseScreen(jumper):
  if not jumper.veiwingPauseScreen:
    pygame.draw.rect(globalVariables["screen"], (255, 255, 254), (globalVariables["screenWidth"] - 65, 25, 40, 40))

    if pygame.mouse.get_pressed()[0]:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 255, 254, 255):
        jumper.canMove = False
        jumper.veiwingPauseScreen = True
    
    writeText("freesansbold.ttf", 40, "||", (0, 0, 0), (globalVariables["screenWidth"] - 45, 45))
  else:
    drawAlphaRect((0, 0, 0), 150, globalVariables["screenWidth"], globalVariables["screenHeight"], (0, 0))
    pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 2) - 125, (globalVariables["screenHeight"] / 2) - 100, 250, 75))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 0), ((globalVariables["screenWidth"] / 2) - 125, globalVariables["screenHeight"] / 2, 250, 75))
    pygame.draw.rect(globalVariables["screen"], (0, 0, 255), ((globalVariables["screenWidth"] / 2) - 125, (globalVariables["screenHeight"] / 2) + 100, 250, 75))

    if pygame.mouse.get_pressed()[0]:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
        jumper.canMove = True
        jumper.veiwingPauseScreen = False
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
        jumper.resetJumper()
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 0, 255, 255):
        leaveLobby(jumper)

    writeText("freesansbold.ttf", 70, "Pause", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 150))
    writeText("freesansbold.ttf", 50, "Resume", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 62.5))
    writeText("freesansbold.ttf", 50, "Restart", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 37.5))
    writeText("freesansbold.ttf", 50, "Leave", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 137.5))

def drawGameAndUpdateJumperPosition(jumper, keydownEvent):
  drawGame()
  updateJumperPosition(jumper, keydownEvent)
  drawPauseScreen(jumper)