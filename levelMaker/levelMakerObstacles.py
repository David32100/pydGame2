import pygame

from levelMakerGlobalVariables import screen

class Ground:
  def draw(self, rect):
    pygame.draw.rect(screen, (125, 125, 1), rect)
class EndGoal:
  def draw(self, rect):
    pygame.draw.circle(screen, (0, 255, 1), (rect[0], rect[1]), rect[2])
class Enemy:
  def draw(self, rect):
    pygame.draw.rect(screen, (255, 0, 254), rect)