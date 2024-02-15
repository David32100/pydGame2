import pygame
import random
from globalVariables import globalVariables

class OtherJumpers():
  def __init__(self, otherJumperX: float, otherJumperY: float):
    self.otherJumperColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    self.otherJumperX, self.otherJumperY = (otherJumperX - globalVariables["scroll"], otherJumperY)

  def drawJumper(self):
    otherJumperBody = (self.otherJumperX, self.otherJumperY, 20, 40)
    otherJumperHead = (self.otherJumperX + 10, self.otherJumperY - 10)

    pygame.draw.rect(globalVariables["screen"], self.otherJumperColor, otherJumperBody)
    pygame.draw.circle(globalVariables["screen"], self.otherJumperColor, otherJumperHead, 10)

  def updateJumper(self, otherJumperX: float, otherJumperY: float):
    self.otherJumperX = otherJumperX - globalVariables["scroll"]
    self.otherJumperY = otherJumperY