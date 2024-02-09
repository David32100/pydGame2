import pygame

from globalVariables import globalVariables
from collision import collisionCheck
from systemFunctions import checkIfTouchingColor
from levels import levels

class Jumper():
  def __init__(self):
    self.jumperColor = (0, 0, 255)
    self.jumperX, self.jumperY = 300, 410
    self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]
    self.jumperWidth, self.jumperHeight = 20, 40
    self.jumperHeadRadius = 10
    self.speed = 3
    self.jumpTimer = 1
    self.alive = True
    self.gravity = 3
    self.levelWon = False
    self.scrollThreshold = globalVariables["screenWidth"] / 2

    self.keyBinds = {
      pygame.K_a: self.moveLeft,
      pygame.K_d: self.moveRight,
      pygame.K_LEFT: self.moveLeft,
      pygame.K_RIGHT: self.moveRight,
      pygame.K_UP: self.jump,
      pygame.K_SPACE: self.jump,
      pygame.K_w: self.jump
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
      if self.jumperY - (2 * self.jumperHeadRadius) + deltaY > 0 and not self.__checkCollision()["Top"]:
        self.jumperY += deltaY
    elif deltaY > 0:
      if self.jumperY + self.jumperHeight + deltaY < globalVariables["screenHeight"] and not self.__checkCollision()["Bottom"]:
        self.jumperY += deltaY
      elif self.jumperY + self.jumperHeight + deltaY >= globalVariables["screenHeight"]:
        self.alive = False

    if deltaX < 0:
      if self.jumperX + deltaX > 0 and not self.__checkCollision()["Left"]:
        self.jumperX += deltaX
    elif deltaX > 0:
      if self.jumperX + self.jumperWidth + deltaX < globalVariables["screenWidth"] and not self.__checkCollision()["Right"]:
        self.jumperX += deltaX

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
      if self.jumpTimer <= (0.5 * globalVariables["fps"]):
        if self.__checkCollision()["Top"] or (self.jumperY - (2 * self.jumperHeadRadius) - speed) <= self.gravity:
          self.jumpTimer = 0.51 * globalVariables["fps"]
        
        self.__move(False, -self.gravity - speed)
        self.__move(True, speed / 2)
        self.jumpTimer += 1
    
      if self.__checkCollision()["Bottom"]:
        self.jumpTimer = 1
    

  def __checkCollision(self):
    if self.jumperY + self.jumperHeight + self.gravity < globalVariables["screenHeight"]:
      return collisionCheck(self.jumperX, self.jumperY - (self.jumperHeadRadius * 2), self.jumperWidth, (self.jumperHeight + (self.jumperHeadRadius * 2)), self.gravity)
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
    self.levelWon = checkIfTouchingColor(self.jumperX, self.jumperY - (self.jumperHeadRadius * 2), self.jumperWidth, self.jumperHeight + (self.jumperHeadRadius * 2), globalVariables["goalColor"])

jumper = Jumper()