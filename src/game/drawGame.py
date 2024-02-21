import pygame

from globalVariables import globalVariables
from game.levels import levels
from client.communications import sendAMessage

sendJumpingMessage = False

def drawGame():
  globalVariables["screen"].fill((0, 128, 128))
  
  for object in levels[globalVariables["currentLevel"]][2]:
    objectRect = levels[globalVariables["currentLevel"]][2][object]
    object.draw((objectRect[0] - globalVariables["scroll"], objectRect[1], objectRect[2], objectRect[3]))

def updateJumperPosition(jumper):
  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_LEFT]:
    jumper.moveLeft()

  if pressedKeys[pygame.K_RIGHT]:
    jumper.moveRight()

  if not pressedKeys[pygame.K_LEFT] and not pressedKeys[pygame.K_RIGHT]:
    jumper.slowDownIfNotMoving()
  
  if pressedKeys[pygame.K_UP]:
    jumper.jump()

    if not pressedKeys[pygame.K_RIGHT] and not pressedKeys[pygame.K_LEFT]:
      jumper.moveRight()

    sendAMessage({"action":"startJump", "contents":{"lobby":globalVariables["lobby"]}})
  
  if not pressedKeys[pygame.K_UP]:
    if jumper.canJump:
      jumper.stopJumping()
      sendAMessage({"action":"stopJump", "contents":{"lobby":globalVariables["lobby"]}})

  jumper.experienceGravity()
  jumper.scrollScreen()
  jumper.winLevelIfTouchingGoal()
  jumper.dieIfTouchingBottom()
  jumper.drawJumper()
  sendAMessage({"action":"updatePlayer", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"], "position":(jumper.jumperXWithScroll, jumper.jumperY)}})
  
  for otherJumper in list(globalVariables["playersInLobby"].values()):
    otherJumper.drawJumper()

def drawGameAndUpdateJumperPosition(jumper):
  drawGame()
  updateJumperPosition(jumper)