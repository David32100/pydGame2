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
  global sendJumpingMessage
  pressedKeys = pygame.key.get_pressed()

  for key in list(jumper.keyBinds.keys()):
    if pressedKeys[key]:
      jumper.keyBinds[key](jumper.speed)

  if not pressedKeys[pygame.K_UP] and not pressedKeys[pygame.K_SPACE] and not pressedKeys[pygame.K_w]:
    jumper.dontJump()
    sendJumpingMessage = False
  else:
    if jumper.checkJumperCollision()["Bottom"]:
      sendJumpingMessage = True
    
    jumper.jump(jumper.speed)

  if sendJumpingMessage:
    sendAMessage({"action":"JUMP!!!", "contents":{"lobby":globalVariables["lobby"]}})

  jumper.scrollScreen(jumper.speed)
  jumper.experienceGravity()
  jumper.winLevelIfTouchingGoal()
  jumper.drawJumper()
  sendAMessage({"action":"updatePlayer", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"], "position":(jumper.jumperXWithScroll, jumper.jumperY)}})
  
  for otherJumper in list(globalVariables["playersInLobby"].values()):
    otherJumper.drawJumper()

def drawGameAndUpdateJumperPosition(jumper):
  drawGame()
  updateJumperPosition(jumper)