import pygame
import random
from globalVariables import globalVariables

class OtherJumpers():
  def __init__(self, otherJumperX: float, otherJumperY: float):
    self.otherJumperColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    self.otherJumperX, self.otherJumperY = (otherJumperX - globalVariables["scroll"], otherJumperY)
    self.otherJumperWidth, self.otherJumperHeight = 20, 40
    self.otherJumperHeadRadius = 10

  def drawJumper(self):
    otherJumperBody = (self.otherJumperX, self.otherJumperY, self.otherJumperWidth, self.otherJumperHeight)
    otherJumperHead = (self.otherJumperX + self.otherJumperHeadRadius, self.otherJumperY - self.otherJumperHeadRadius)

    pygame.draw.rect(globalVariables["screen"], self.otherJumperColor, otherJumperBody)
    pygame.draw.circle(globalVariables["screen"], self.otherJumperColor, otherJumperHead, self.otherJumperHeadRadius)

  def updateJumper(self, otherJumperX: float, otherJumperY: float):
    self.otherJumperX = otherJumperX - globalVariables["scroll"]
    self.otherJumperY = otherJumperY

  def talk(self, text:str):
    defaultFont = pygame.font.SysFont("freesansbold.ttf", 30)
    text1 = defaultFont.render(text, True, (0, 0, 0), (255, 255, 255))
    backgroundText = defaultFont.render(text, True, (0, 0, 0), (0, 0, 0))

    text1Rect = text1.get_rect()
    backgroundTextRect = backgroundText.get_rect()
    text1Rect.center = (self.otherJumperX + (self.otherJumperWidth / 2), self.otherJumperY - (self.otherJumperHeadRadius * 2) - 20)
    backgroundTextRect.center = (self.otherJumperX + (self.otherJumperWidth / 2), self.otherJumperY - (self.otherJumperHeadRadius * 2) - 20)


    globalVariables["screen"].blit(backgroundText, backgroundTextRect)
    globalVariables["screen"].blit(text1, text1Rect)