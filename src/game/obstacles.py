import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText

groundColor = (125, 125, 0, 255)
goalColor = (0, 255, 0, 255)
enemyColor = (255, 0, 255)

class Ground():
  def draw(self, groundRect: list):
    groundRectCopy = groundRect.copy()
    groundRectCopy[0] = groundRectCopy[0] - globalVariables["scroll"]
    pygame.draw.rect(globalVariables["screen"], groundColor, groundRectCopy)

class EndGoal():
  def draw(self, positionAndSize: tuple):
    goalposition = (positionAndSize[0] - globalVariables["scroll"], positionAndSize[1])
    goalRadius = positionAndSize[2]

    pygame.draw.circle(globalVariables["screen"], goalColor, goalposition, goalRadius)

class Enemy():
  def draw(self, enemyRect: list):
    enemyRectCopy = enemyRect.copy()
    enemyRectCopy[0] = enemyRectCopy[0] - globalVariables["scroll"]
    pygame.draw.rect(globalVariables["screen"], enemyColor, enemyRectCopy)

class Text():
  def draw(self, args: list):
    args4Copy = args[4].copy()
    args4Copy[0] = args4Copy[0] - globalVariables["scroll"]
    writeText(args[0], args[1], args[2], args[3], args4Copy, args[5], args[6])