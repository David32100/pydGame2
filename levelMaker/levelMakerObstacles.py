import pygame

from levelMakerGlobalVariables import screen
from levelMakerDrawingFunctions import writeText

class Ground:
  def draw(self, rect:tuple):
    pygame.draw.rect(screen, (125, 125, 1), rect)
class EndGoal:
  def draw(self, rect:tuple):
    pygame.draw.circle(screen, (0, 255, 1), (rect[0], rect[1]), rect[2])
class Enemy:
  def draw(self, rect:tuple):
    pygame.draw.rect(screen, (255, 0, 254), rect)
class Text:
  def draw(self, args:tuple):
    writeText(args[0], args[1], args[2], args[3], args[4], args[5], args[6])