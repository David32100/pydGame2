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