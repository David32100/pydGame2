import pygame
import sys

from levelMakerObstacles import Ground, EndGoal, Enemy, Text
from levelMakerGlobalVariables import clock, level, levelLayout, screen
from levelMakerDrawingFunctions import drawAlphaCircle, drawAlphaRect, writeText

pygame.init()
lastPoint = []
currentObstacle = None
scroll = 0
showSideBar = False
typing = False
text = ""

def scrollScreen(scroll:int) -> int:
  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_LEFT]:
    if scroll > 0:
      scroll -= 1
  
  if pressedKeys[pygame.K_RIGHT]:
    if scroll < level[1]:
      scroll += 1

  return scroll

def drawObjects(scroll:int):
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
    elif currentObstacle == "Text":
      textSize = pygame.font.Font("freesansbold.ttf", 30).size(text)
      textWidth = int(textSize[0] / 1.45)

      writeText("freesansbold.ttf", 30, text, (0, 0, 0), lastPoint[1])
      pygame.draw.rect(screen, (0, 0, 0), (lastPoint[1][0] - (textWidth / 2) - 3, lastPoint[1][1] - (textSize[1] / 2) - 3, textWidth + 6, textSize[1] + 6), 3)

def drawItemSelecter():
  # Draw background
  pygame.draw.rect(screen, (255, 255, 255), (0, 500, 700, 100))
  # Draw items to select
  pygame.draw.rect(screen, (125, 125, 0), (25, 525, 50, 50))
  pygame.draw.circle(screen, (0, 255, 0), (125, 550), 25)
  pygame.draw.rect(screen, (255, 0, 255), (175, 525, 50, 50))
  pygame.draw.rect(screen, (0, 0, 4), (250, 525, 50, 50))
  writeText("freesansbold.ttf", 25, "Text", (255, 255, 254), (275, 550))

  # Outline items if selected
  if currentObstacle == "Ground":
    pygame.draw.rect(screen, (0, 0, 0), (22, 522, 56, 56), 3)
  elif currentObstacle == "EndGoal":
    pygame.draw.circle(screen, (0, 0, 0), (125, 550), 28, 3)
  elif currentObstacle == "Enemy":
    pygame.draw.rect(screen, (0, 0, 0), (172, 522, 56, 56), 3)
  elif currentObstacle == "Text":
    pygame.draw.rect(screen, (0, 0, 0), (246, 521, 58, 58), 3)

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
  writeText("freesansbold.ttf", 20, "Level width", (0, 0, 0), (650, 270))
  writeText("freesansbold.ttf", 25, str(level[1]), (255, 255, 255), (650, 305))

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
    if event.type == pygame.KEYDOWN and typing:
      if event.key == pygame.K_BACKSPACE:
        if len(text) > 0:
          text = text.removesuffix(text[-1])
      elif event.key == pygame.K_SPACE:
        text += " "
      elif len(pygame.key.name(event.key)) < 2:
        text += event.unicode

  screen.fill((0, 255, 255))
  scroll = scrollScreen(scroll)
  drawObjects(scroll)
  drawItemSelecter()
    
  if showSideBar:
    drawSideBarRects()

  if checkMouse:
    if typing:
      if text != "":
        levelLayout[lastPoint[0]] = ("freesansbold.ttf", 30, str(text), (0, 0, 0), lastPoint[1], 1, None)
        
      text = ""
      typing = False

    screenColor = screen.get_at((mouseX, mouseY))

    if screenColor == (0, 0, 2, 255):
      levelLayoutToPrint = {}
      i = 0

      for key in list(levelLayout.keys()):
        levelLayoutToPrint[str(key).split(".")[1].split(" ")[0] + "()" + str(i)] = levelLayout[key]
        i += 1

      print("\nLevel: level =", level, "\nLevel Layout: levelLayout =", levelLayoutToPrint)
    elif screenColor == (0, 0, 3, 255):
      pass
    elif screenColor == (0, 0, 4, 255) or screenColor == (255, 255, 254, 255):
      currentObstacle = "Text"
      lastPoint = []
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
      if currentObstacle != None and currentObstacle != "Delete" and currentObstacle != "Text":
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
          elif str(obstacle).split(".")[1].split(" ")[0] == "Text":
            textSize = pygame.font.Font(levelLayout[obstacle][0], levelLayout[obstacle][1]).size(levelLayout[obstacle][2])
            
            if mouseX > levelLayout[obstacle][4][0] - textSize[0] / 2 and mouseX < levelLayout[obstacle][4][0] + textSize[0] / 2 and mouseY > levelLayout[obstacle][4][1] - textSize[1] / 2 and mouseY < levelLayout[obstacle][4][1] + textSize[1] / 2:
              levelLayout.pop(obstacle)
          else:
            if mouseX > levelLayout[obstacle][0] and mouseX < levelLayout[obstacle][0] + levelLayout[obstacle][2] and mouseY > levelLayout[obstacle][1] and mouseY < levelLayout[obstacle][1] + levelLayout[obstacle][3]:
              levelLayout.pop(obstacle)
      elif currentObstacle == "Text":
        typing = True
        lastPoint = [eval(currentObstacle)(), [mouseX + scroll, mouseY]]

    else:
      lastPoint = []
      currentObstacle = None
  
  if showSideBar:
    drawSideBarText()

  pygame.display.flip()