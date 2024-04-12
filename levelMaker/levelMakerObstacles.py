import pygame

from levelMakerGlobalVariables import screen
from levelMakerDrawingFunctions import writeText

class Ground:
  def draw(self, rect:list, scroll:int):
    pygame.draw.rect(screen, (125, 125, 1), (rect[0] + scroll, rect[1], rect[2], rect[3]))
class EndGoal:
  def draw(self, rect:list, scroll:int):
    pygame.draw.circle(screen, (0, 255, 1), (rect[0] + scroll, rect[1]), rect[2])
class Enemy:
  def draw(self, rect:list, scroll:int):
    pygame.draw.rect(screen, (255, 0, 254), (rect[0] + scroll, rect[1], rect[2], rect[3]))
class Text:
  def draw(self, args:list, scroll:int):
    writeText(args[0], args[1], args[2], args[3], (args[4][0] + scroll, args[4][1]), args[5], args[6])