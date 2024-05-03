import pygame

from globalVariables import globalVariables
from game.collision import collisionCheck
from game.levels import levels
from game.obstacles import groundColor, goalColor, enemyColor

def checkIfTouchingColor(spriteX, spriteY, spriteWidth, spriteHeight, colorToCheckFor):
  for xPos in range(int(spriteX), int(spriteX + spriteWidth)):
    for yPos in range(int(spriteY), int(spriteY + spriteHeight)):
      if globalVariables["screen"].get_at((xPos, yPos)) == colorToCheckFor:
        return True
      
  return False

class Jumper():
  def __init__(self):
    globalVariables["scroll"] = 0
    self.jumperColor = globalVariables["userSettings"]["playerColor"]
    self.jumperX, self.jumperY = 0, 0
    self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]
    self.jumperWidth, self.jumperHeight = 20, 40
    self.jumperHeadRadius = 10
    self.alive = True
    self.levelWon = False
    self.scrollThreshold = globalVariables["screenWidth"] / 2
    self.xVelocity, self.yVelocity = 0, 0
    self.canJump = False
    self.jumpTimer = 0
    self.canMove = True
    self.talking = False
    self.veiwingPauseScreen = False
    
  def drawJumper(self):
    jumperBody = (self.jumperX, self.jumperY, self.jumperWidth, self.jumperHeight)
    jumperHead = (self.jumperX + (self.jumperWidth / 2), self.jumperY - self.jumperHeadRadius)

    if not self.alive:
      self.jumperColor = (255, 0, 0)

    defaultFont = pygame.font.SysFont("freesansbold.ttf", 20)
    name = defaultFont.render(globalVariables["shownUsername"], True, (0, 0, 0))
    nameRect = name.get_rect()
    nameRect.center = (self.jumperX + (self.jumperWidth / 2), self.jumperY - (self.jumperHeadRadius * 2) - 10)
    globalVariables["screen"].blit(name, nameRect)
    pygame.draw.rect(globalVariables["screen"], self.jumperColor, jumperBody)
    pygame.draw.circle(globalVariables["screen"], self.jumperColor, jumperHead, self.jumperHeadRadius)

  def moveLeft(self, speed:float):
    if self.canMove:
      if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Left"] and (self.jumperX + self.xVelocity) > 0:
        if self.xVelocity > 0:
          if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Right"] and (self.jumperX + self.jumperWidth + self.xVelocity) < globalVariables["screenWidth"]:
            self.jumperX += self.xVelocity
          else:
            self.xVelocity = 0
        else:
          self.jumperX += self.xVelocity

        self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]

        if self.xVelocity > -4 * speed:
          self.xVelocity -= speed
        else:
          self.xVelocity = -4 * speed
      else:
        self.xVelocity = 0

  def moveRight(self, speed:float):
    if self.canMove:
      if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Right"] and (self.jumperX + self.jumperWidth + self.xVelocity) < globalVariables["screenWidth"]:
        if self.xVelocity < 0:
          if not self.checkJumperCollision(xDisplacement=self.xVelocity)["Left"] and (self.jumperX + self.xVelocity) > 0:
            self.jumperX += self.xVelocity
          else:
            self.xVelocity = 0
        else:
          self.jumperX += self.xVelocity

        self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]

        if self.xVelocity < 4 * speed:
          self.xVelocity += speed
        else:
          self.xVelocity = 4 * speed
      else:
        self.xVelocity = 0

  def experienceGravity(self):
    if self.alive:
      if not self.checkJumperCollision(yDisplacement=self.yVelocity)["Bottom"] and (self.jumperY + self.jumperHeight + self.yVelocity) < globalVariables["screenHeight"]:
        if self.yVelocity < 0:
          if not self.checkJumperCollision(yDisplacement=self.yVelocity)["Top"] and (self.jumperY + (self.jumperHeadRadius * 2) + self.yVelocity) > 0:
            self.jumperY += self.yVelocity
        else:
          self.jumperY += self.yVelocity

        self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]

        if self.yVelocity < 10:
          self.yVelocity += 0.5
      else:
        self.yVelocity = 0

  def jump(self, height:float, speed:float=1):
    if self.canMove:
      if not self.canJump:
        if self.checkJumperCollision(yDisplacement=1)["Bottom"]:
          self.canJump = True

      if self.checkJumperCollision(yDisplacement=self.yVelocity)["Top"] or self.jumperY + (self.jumperHeadRadius * 2) + self.yVelocity < 0:
        self.canJump = False
        self.yVelocity = 0

      if self.canJump:
        if self.jumpTimer < 20 * height:
          self.yVelocity -= speed
          self.jumpTimer += 1
        else:
          self.canJump = False
          self.jumpTimer = 0

  def stopJumping(self):
    self.canJump = False

  def slowDownIfNotMoving(self):
    if self.alive:
      if self.xVelocity > 0 and not self.checkJumperCollision(xDisplacement=self.xVelocity)["Right"] and (self.jumperX + self.jumperWidth + self.xVelocity) < globalVariables["screenWidth"]:
        self.jumperX += self.xVelocity
      elif self.xVelocity < 0 and not self.checkJumperCollision(xDisplacement=self.xVelocity)["Left"] and (self.jumperX + self.xVelocity) > 0:
        self.jumperX += self.xVelocity

      self.jumperXWithScroll = self.jumperX + globalVariables["scroll"]

      if self.xVelocity > 1 or self.xVelocity < -1:
        self.xVelocity += self.xVelocity / -10
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
    self.jumperColor = globalVariables["userSettings"]["playerColor"]
    self.jumperX, self.jumperY = levels[globalVariables["currentLevel"]][3], levels[globalVariables["currentLevel"]][4]
    globalVariables["scroll"] = 0
    self.alive = True
    self.levelWon = False
    self.xVelocity, self.yVelocity = 0, 0
    self.canJump = False
    self.jumpTimer = 0
    self.canMove = True
    self.talking = False
    self.veiwingPauseScreen = False

  def winLevelIfTouchingGoal(self):
    self.levelWon = checkIfTouchingColor(self.jumperX, self.jumperY - (self.jumperHeadRadius * 2), self.jumperWidth, self.jumperHeight + (self.jumperHeadRadius * 2), goalColor)

  def dieIfTouchingBottom(self):
    if self.jumperY + self.jumperHeight + self.yVelocity > globalVariables["screenHeight"]:
      self.alive = False
      self.canMove = False
      self.jumperColor = (255, 0, 0)

  def talk(self, text:str):
    defaultFont = pygame.font.SysFont("freesansbold.ttf", 30)
    text1 = defaultFont.render(text, True, (0, 0, 0), (255, 255, 255))
    text1Rect = text1.get_rect()
    text1Rect.center = (self.jumperX + (self.jumperWidth / 2), self.jumperY - (self.jumperHeadRadius * 2) - 28)
    globalVariables["screen"].blit(text1, text1Rect)

  def dieIfTouchingEnemy(self):
    if checkIfTouchingColor(self.jumperX, self.jumperY - (self.jumperHeadRadius * 2), self.jumperWidth, self.jumperHeight + (self.jumperHeadRadius * 2), enemyColor):
      self.alive = False
      self.canMove = False
      self.jumperColor = (255, 0, 0)
    
jumper = Jumper()