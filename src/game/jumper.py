import pygame

from globalVariables import globalVariables
from game.collision import collisionCheck
from game.levels import levels
from game.obstacles import groundColor, goalColor

def checkIfTouchingColor(spriteX, spriteY, spriteWidth, spriteHeight, colorToCheckFor):
  for xPos in range(int(spriteX), int(spriteX + spriteWidth)):
    for yPos in range(int(spriteY), int(spriteY + spriteHeight)):
      if globalVariables["screen"].get_at((xPos, yPos)) == colorToCheckFor:
        return True
      
  return False

class Jumper():
  def __init__(self):
    self.jumperColor = (0, 0, 255)
    self.jumperX, self.jumperY = 300, 410
    self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]
    self.jumperWidth, self.jumperHeight = 20, 40
    self.jumperHeadRadius = 10
    self.speed = 3
    self.alive = True
    self.gravity = 3
    self.levelWon = False
    self.scrollThreshold = globalVariables["screenWidth"] / 2
    self.canJump = False
    self.canMessageInitiatedJump = False
    # Figure out how to get rid of jumpTimer and messageInitiatedJumpTimer
    self.jumpTimer = 1
    self.messageInitiatedJumpTimer = 1

    self.keyBinds = {
      pygame.K_a: self.moveLeft,
      pygame.K_LEFT: self.moveLeft,
      pygame.K_d: self.moveRight,
      pygame.K_RIGHT: self.moveRight
    }
    
  def drawJumper(self):
    jumperBody = (self.jumperX, self.jumperY, self.jumperWidth, self.jumperHeight)
    jumperHead = (self.jumperX + (self.jumperWidth / 2), self.jumperY - self.jumperHeadRadius)

    if not self.alive:
      self.jumperColor = (255, 0, 0)

    pygame.draw.rect(globalVariables["screen"], self.jumperColor, jumperBody)
    pygame.draw.circle(globalVariables["screen"], self.jumperColor, jumperHead, self.jumperHeadRadius)


  def __move(self, moveInXAxis: bool, speed: float):
    deltaX = 0
    deltaY = 0

    if moveInXAxis:
      deltaX += speed
    else:
      deltaY += speed

    if deltaY < 0:
      if self.jumperY - (2 * self.jumperHeadRadius) + deltaY > 0 and not self.checkJumperCollision()["Top"]:
        self.jumperY += deltaY
    elif deltaY > 0:
      if self.jumperY + self.jumperHeight + deltaY < globalVariables["screenHeight"] and not self.checkJumperCollision()["Bottom"]:
        self.jumperY += deltaY
      elif self.jumperY + self.jumperHeight + deltaY >= globalVariables["screenHeight"]:
        self.alive = False

    if deltaX < 0:
      if self.jumperX + deltaX > 0 and not self.checkJumperCollision(xDisplacement=deltaX)["Left"]:
        self.jumperX += deltaX
    elif deltaX > 0:
      if self.jumperX + self.jumperWidth + deltaX < globalVariables["screenWidth"] and not self.checkJumperCollision(xDisplacement=deltaX)["Right"]:
        self.jumperX += deltaX

    self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]

  def moveLeft(self, speed: float):
    if self.alive:
      self.__move(True, -speed)
  
  def moveRight(self, speed: float):
    if self.alive:
      self.__move(True, speed)
    
  def experienceGravity(self):
    if self.alive:
      self.__move(False, self.gravity)

  def jump(self, speed : int):
    if self.alive:
      if self.canJump:
        if self.jumpTimer <= (1 * globalVariables["fps"]):
          if self.checkJumperCollision(self.gravity - speed + (self.jumpTimer * speed)/(1 * globalVariables["fps"]))["Top"] or (self.jumperY - (self.jumperHeadRadius * 2) - self.gravity - speed + (self.jumpTimer * speed)/(1 * globalVariables["fps"])) <= 0:
            self.jumpTimer = 1.1 * globalVariables["fps"]
          
          self.__move(False, -self.gravity - speed + (self.jumpTimer * (speed))/(1 * globalVariables["fps"]))
          self.jumpTimer += 1
    
        if self.jumpTimer > 1:
          self.__move(True, self.speed / 2)

        if self.checkJumperCollision()["Bottom"]:
          self.jumpTimer = 1
          self.canJump = False
      else:
        if self.checkJumperCollision()["Bottom"]:
          self.canJump = True

  def dontJump(self):
    self.canJump = False

  def messageInitiatedJump(self):
    if self.alive:
      if self.canMessageInitiatedJump:
        if self.messageInitiatedJumpTimer <= (1 * globalVariables["fps"]):
          if self.checkJumperCollision(self.gravity - self.speed + (self.jumpTimer * self.speed)/(1 * globalVariables["fps"]))["Top"] or (self.jumperY - (self.jumperHeadRadius * 2) - self.gravity - self.speed + (self.jumpTimer * self.speed)/(1 * globalVariables["fps"])) <= 0:
            self.jumpTimer = 1.1 * globalVariables["fps"]
          
          self.__move(False, -self.gravity - self.speed + (self.jumpTimer * (self.speed))/(1 * globalVariables["fps"]))
          self.messageInitiatedJumpTimer += 1

          if self.messageInitiatedJumpTimer > 1:
            self.__move(True, self.speed / 2)

        if self.checkJumperCollision()["Bottom"]:
          self.messageInitiatedJumpTimer = 1
          self.canMessageInitiatedJump = False
        else:
          self.canMessageInitiatedJump = False
    
        if self.checkJumperCollision()["Bottom"]:
          self.messageInitiatedJumpTimer = 1
      else:
        if self.checkJumperCollision()["Bottom"]:
          self.canMessageInitiatedJump = True

  def checkJumperCollision(self, xDisplacement: float=0, yDisplacement: float=0):
    if self.jumperY + self.jumperHeight + self.gravity < globalVariables["screenHeight"]:
      return collisionCheck(self.jumperX + xDisplacement, self.jumperY - (self.jumperHeadRadius * 2) + yDisplacement, self.jumperWidth, (self.jumperHeight + (self.jumperHeadRadius * 2)), self.gravity, groundColor)
    else:
      self.alive = False
      return {"Top": True, "Bottom": True, "Left": True, "Right": True}
    
  def scrollScreen(self, speed: float):
    if self.jumperX > self.scrollThreshold:
      if globalVariables["scroll"] < levels[globalVariables["currentLevel"]][1]:
        globalVariables["scroll"] += speed
        self.jumperX = self.scrollThreshold

    elif self.jumperX < self.scrollThreshold:
      if globalVariables["scroll"] > 0:
        globalVariables["scroll"] -= speed
        self.jumperX = self.scrollThreshold

  def resetJumper(self):
    self.jumperColor = (0, 0, 255)
    self.jumperX, self.jumperY = 300, 410
    globalVariables["scroll"] = 0
    self.alive = True
    self.levelWon = False

  def winLevelIfTouchingGoal(self):
    self.levelWon = checkIfTouchingColor(self.jumperX, self.jumperY - (self.jumperHeadRadius * 2), self.jumperWidth, self.jumperHeight + (self.jumperHeadRadius * 2), goalColor)

jumper = Jumper()