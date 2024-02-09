import pygame

from globalVariables import globalVariables

class Ground():
  def draw(self, positionAndSize: tuple):
    groundColor = globalVariables["groundColor"]
    groundRect = positionAndSize

    pygame.draw.rect(globalVariables["screen"], groundColor, groundRect)

class EndGoal():
  def draw(self, positionAndSize: tuple):
    goalColor = globalVariables["goalColor"]
    goalposition = (positionAndSize[0], positionAndSize[1])
    goalRadius = positionAndSize[2]

    pygame.draw.circle(globalVariables["screen"], goalColor, goalposition, goalRadius)