import pygame

from globalVariables import globalVariables

groundColor = (125, 125, 0, 255)
goalColor = (0, 255, 0, 255)
enemyColor = (255, 0, 255)

class Ground():
  def draw(self, groundRect: tuple):
    pygame.draw.rect(globalVariables["screen"], groundColor, groundRect)

class EndGoal():
  def draw(self, positionAndSize: tuple):
    goalposition = (positionAndSize[0], positionAndSize[1])
    goalRadius = positionAndSize[2]

    pygame.draw.circle(globalVariables["screen"], goalColor, goalposition, goalRadius)

class Enemy():
  def draw(self, enemyRect: tuple):
    pygame.draw.rect(globalVariables["screen"], enemyColor, enemyRect)