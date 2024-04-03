import pygame
import sys

from levelMakerObstacles import Ground, EndGoal, Enemy
from levelMakerGlobalVariables import clock, level, levelLayout, screen
from levelMakerDrawingFunctions import drawAlphaCircle, drawAlphaRect, writeText

pygame.init()
lastPoint = []
currentObstacle = None
scroll = 0
showSideBar = False

def scrollScreen(scroll:int) -> int:
  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_LEFT]:
    if scroll > 0:
      scroll -= 1
  
  if pressedKeys[pygame.K_RIGHT]:
    if scroll < level[1]:
      scroll += 1
      print(scroll)

  return scroll

def drawObjects():
  for object in list(levelLayout.keys()):
    object.draw(levelLayout[object])

  if lastPoint != []:
    if currentObstacle == "Ground":
      drawAlphaRect((125, 125, 0, 127), [lastPoint[1][0], lastPoint[1][1], mouseX + scroll - lastPoint[1][0], mouseY - lastPoint[1][1]])
    elif currentObstacle == "EndGoal":
      if abs(mouseX + scroll - lastPoint[1][0]) > abs(mouseY - lastPoint[1][1]):
        drawAlphaCircle((0, 255, 0, 127), [lastPoint[1][0], lastPoint[1][1]], mouseX + scroll - lastPoint[1][0])
      else:
        drawAlphaCircle((0, 255, 0, 127), [lastPoint[1][0], lastPoint[1][1]], mouseY - lastPoint[1][1])
    elif currentObstacle == "Enemy":
      drawAlphaRect((255, 0, 255, 127), [lastPoint[1][0], lastPoint[1][1], mouseX + scroll - lastPoint[1][0], mouseY - lastPoint[1][1]])

def drawItemSelecter():
  # Draw background
  pygame.draw.rect(screen, (255, 255, 255), (0, 500, 700, 100))
  # Draw items to select
  pygame.draw.rect(screen, (125, 125, 0), (25, 525, 50, 50))
  pygame.draw.circle(screen, (0, 255, 0), (125, 550), 25)
  pygame.draw.rect(screen, (255, 0, 255), (175, 525, 50, 50))

  # Outline items if selected
  if currentObstacle == "Ground":
    pygame.draw.rect(screen, (0, 0, 0), (22, 522, 56, 56), 3)
  elif currentObstacle == "EndGoal":
    pygame.draw.circle(screen, (0, 0, 0), (125, 550), 28, 3)
  elif currentObstacle == "Enemy":
    pygame.draw.rect(screen, (0, 0, 0), (172, 522, 56, 56), 3)

  # Draw delete and settings buttons on top of selector
  pygame.draw.rect(screen, (255, 255, 255), (500, 500, 200, 100))
  pygame.draw.rect(screen, (255, 0, 0), (560, 525, 50, 50))
  pygame.draw.circle(screen, (127, 127, 127), (660, 550), 25)

  # Outline delete button if selected
  if currentObstacle == "Delete":
    pygame.draw.rect(screen, (0, 0, 0), (557, 522, 56, 56), 3)

def drawSideBarRects():
  pygame.draw.rect(screen, (255, 255, 255), (600, 200, 100, 300))

  pygame.draw.rect(screen, (0, 0, 2), (610, 210, 80, 40))
  pygame.draw.rect(screen, (0, 0, 3), (610, 285, 80, 40))

def drawSideBarText():
  writeText("freesansbold.ttf", 20, "Print level", (255, 255, 255), (650, 230))
  writeText("freesansbold.ttf", 20, "Start position", (0, 0, 0), (650, 270))
  writeText("freesansbold.ttf", 20, "(" + str(level[3]) + ", " + str(level[4]) + ")", (255, 255, 255), (650, 305))

while True:
  clock.tick(60)
  checkMouse = False
  mouseX, mouseY = pygame.mouse.get_pos()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      checkMouse = True

  screen.fill((0, 255, 255))
  scroll = scrollScreen(scroll)
  drawObjects()
  drawItemSelecter()
    
  if showSideBar:
    drawSideBarRects()

  if checkMouse:
    screenColor = screen.get_at((mouseX, mouseY))

    if screenColor == (0, 0, 2, 255):
      levelLayoutToPrint = {}

      for key in list(levelLayout.keys()):
        levelLayoutToPrint[str(key).split(".")[1].split(" ")[0] + "()"] = levelLayout[key]

      print("\nLevel: level =", level, "\nLevel Layout: levelLayout =", levelLayoutToPrint)
    elif screenColor == (125, 125, 0, 255):
      currentObstacle = "Ground"
      lastPoint = []
    elif screenColor == (0, 255, 0, 255):
      currentObstacle = "EndGoal"
      lastPoint = []
    elif screenColor == (255, 0, 255, 255):
      currentObstacle = "Enemy"
      lastPoint = []
    elif screenColor == (255, 0, 0, 255):
      currentObstacle = "Delete"
      lastPoint = []
    elif screenColor == (127, 127, 127, 255):
      showSideBar = not showSideBar
      lastPoint = []
    elif screenColor != (255, 255, 255, 255):
      if currentObstacle != None and currentObstacle != "Delete":
        if lastPoint == []:
          lastPoint = [eval(currentObstacle)(), [mouseX + scroll, mouseY]]
        else:
          if currentObstacle != "EndGoal":
            if mouseX + scroll - lastPoint[1][0] < 0:
              width = lastPoint[1][0] - mouseX + scroll
              lastPoint[1][0] = mouseX + scroll
            else:
              width = mouseX + scroll - lastPoint[1][0]

            if mouseY - lastPoint[1][1] < 0:
              height = lastPoint[1][1] - mouseY
              lastPoint[1][1] = mouseY
            else:
              height = mouseY - lastPoint[1][1]

            levelLayout[lastPoint[0]] = (lastPoint[1][0], lastPoint[1][1], width, height)
          else:
            width = abs(mouseX + scroll - lastPoint[1][0])

            if abs(mouseY - lastPoint[1][1] > width):
              width = abs(mouseY - lastPoint[1][1])

            levelLayout[lastPoint[0]] = (lastPoint[1][0], lastPoint[1][1], width)

          lastPoint = []
      elif currentObstacle == "Delete":
        for obstacle in list(levelLayout.keys()):
          if str(obstacle).split(".")[1].split(" ")[0] == "EndGoal":
            if mouseX > levelLayout[obstacle][0] - levelLayout[obstacle][2] and mouseX < levelLayout[obstacle][0] + levelLayout[obstacle][2] and mouseY > levelLayout[obstacle][1] - levelLayout[obstacle][2] and mouseY < levelLayout[obstacle][1] + levelLayout[obstacle][2]:
              levelLayout.pop(obstacle)
          else:
            if mouseX > levelLayout[obstacle][0] and mouseX < levelLayout[obstacle][0] + levelLayout[obstacle][2] and mouseY > levelLayout[obstacle][1] and mouseY < levelLayout[obstacle][1] + levelLayout[obstacle][3]:
              levelLayout.pop(obstacle)
    else:
      lastPoint = []
      currentObstacle = None
  
  if showSideBar:
    drawSideBarText()

  pygame.display.flip()