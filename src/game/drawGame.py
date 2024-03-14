import pygame

from globalVariables import globalVariables
from game.levels import levels
from client.communications import sendAMessage
from drawingFunctions import writeText, leaveLobby

sendJumpingMessage = False
text = ""

def drawAlphaRect(color:tuple, opacity:int, width:float, height:float, position:tuple) -> pygame.Surface:
  alphaRect = pygame.Surface((width, height))
  alphaRect.set_alpha(opacity)
  alphaRect.fill(color)
  globalVariables["screen"].blit(alphaRect, position)
  return alphaRect

def drawGame():
  globalVariables["screen"].fill((0, 128, 128))
  
  for object in levels[globalVariables["currentLevel"]][2]:
    objectRect = levels[globalVariables["currentLevel"]][2][object]
    object.draw((objectRect[0] - globalVariables["scroll"], objectRect[1], objectRect[2], objectRect[3]))

def updateJumperPosition(jumper, keydownEvent):
  global text
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
        sendAMessage({"action":"startJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})
  
    if not pressedKeys[pygame.K_UP] and not pressedKeys[pygame.K_w] and not pressedKeys[pygame.K_SPACE]:
      jumper.stopJumping()
      sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"], "username":globalVariables["username"]}})

  if pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a]:
    jumper.moveLeft()

  if pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d]:
    jumper.moveRight()

  if not pressedKeys[pygame.K_LEFT] and not pressedKeys[pygame.K_RIGHT] and not pressedKeys[pygame.K_d] and not pressedKeys[pygame.K_a]:
    jumper.slowDownIfNotMoving()

  if pressedKeys[pygame.K_SLASH]:
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
      globalVariables["timers"][str(globalVariables["username"]) + "'sTalkingTimer"] = [0, text]
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
      if timer.split("'")[0] in globalVariables["playersInLobby"] and not globalVariables["userSettings"]["hideTextChat"]:
        globalVariables["playersInLobby"][timer.split("'")[0]].talk(globalVariables["timers"][timer][1])
      elif timer.split("'")[0] == globalVariables["username"]:
        if not jumper.talking:
          jumper.talk(globalVariables["timers"][timer][1])
      else:
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