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
    globalVariables["scroll"] = 500
    self.jumperColor = (0, 0, 255)
    self.jumperX, self.jumperY = 400, 200
    self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]
    self.jumperWidth, self.jumperHeight = 20, 40
    self.jumperHeadRadius = 10
    self.alive = True
    self.levelWon = False
    self.scrollThreshold = globalVariables["screenWidth"] / 2
    self.xVelocity = 0
    self.xAcceleration = 0
    
  def drawJumper(self):
    jumperBody = (self.jumperX, self.jumperY, self.jumperWidth, self.jumperHeight)
    jumperHead = (self.jumperX + (self.jumperWidth / 2), self.jumperY - self.jumperHeadRadius)

    if not self.alive:
      self.jumperColor = (255, 0, 0)

    pygame.draw.rect(globalVariables["screen"], self.jumperColor, jumperBody)
    pygame.draw.circle(globalVariables["screen"], self.jumperColor, jumperHead, self.jumperHeadRadius)

  def moveLeft(self):
    if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Left"] and (self.jumperX + self.xVelocity) > 0:
      if self.xVelocity > 0:
        if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Right"] and (self.jumperX + self.jumperWidth + self.xVelocity) < globalVariables["screenWidth"]:
          self.jumperX += self.xVelocity
      else:
        self.jumperX += self.xVelocity

      if self.xVelocity > -5:
        self.xAcceleration -= 1
        self.xVelocity += self.xAcceleration / globalVariables["fps"]
        print("Acceleration:", self.xAcceleration, "Velocity:", self.xVelocity)
      else:
        self.xAcceleration = 0
    else:
      self.xAcceleration = 0
      self.xVelocity = 0

  def moveRight(self):
    if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Right"] and (self.jumperX + self.jumperWidth + self.xVelocity) < globalVariables["screenWidth"]:
      if self.xVelocity < 0:
        if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Left"] and (self.jumperX + self.xVelocity) > 0:
          self.jumperX += self.xVelocity
      else:
        self.jumperX += self.xVelocity

      if self.xVelocity < 5:
        self.xAcceleration += 1
        self.xVelocity += self.xAcceleration / globalVariables["fps"]
        print("Acceleration:", self.xAcceleration, "Velocity:", self.xVelocity)
      else:
        self.xAcceleration = 0
    else:
      self.xAcceleration = 0
      self.xVelocity = 0

  def slowDownIfNotMoving(self):
    self.xAcceleration = 0

    if self.xVelocity > 0 and not self.checkJumperCollision(xDisplacement=self.xVelocity)["Right"] and (self.jumperX + self.jumperWidth + self.xVelocity) < globalVariables["screenWidth"]:
      self.jumperX += self.xVelocity
    elif self.xVelocity < 0 and not self.checkJumperCollision(xDisplacement=self.xVelocity)["Left"] and (self.jumperX + self.xVelocity) > 0:
      self.jumperX += self.xVelocity

    if self.xVelocity > 1 or self.xVelocity < -1:
      self.xVelocity += (self.xVelocity * -3) / globalVariables["fps"]
    else:
      self.xVelocity = 0

  def checkJumperCollision(self, xDisplacement: float=0, yDisplacement: float=0) -> dict:
    if self.jumperY + self.jumperHeight < globalVariables["screenHeight"]:
      return collisionCheck(self.jumperX + xDisplacement, self.jumperY - (self.jumperHeadRadius * 2) + yDisplacement, self.jumperWidth, (self.jumperHeight + (self.jumperHeadRadius * 2)), groundColor)
    else:
      self.alive = False
      return {"Top": True, "Bottom": True, "Left": True, "Right": True}
    
  def scrollScreen(self):
    if levels[globalVariables["currentLevel"]][1] > (globalVariables["scroll"] + self.jumperX - self.scrollThreshold) > 0:
      globalVariables["scroll"] += self.jumperX - self.scrollThreshold
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