# Level loader: Put level and levelLayout in a list, in that order, each key in levelLayout must have one character in front of it, then click load level
# Print level: Click print level, level will be in level.JSON, NOTE: Level must be changed before it's put into game
import pygame
import sys
import json

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
changingWidth = False
levelWidth = str(level[1])
changingX = False
spawnX = str(level[3])
changingY = False
spawnY = str(level[4])

def changeText(event:pygame.event.Event, text:str, onlyNumbers:bool = False, maxCharacters:int = -1) -> str:
  if event.key == pygame.K_BACKSPACE:
    if len(text) > 0:
      text = text.removesuffix(text[-1])
  elif event.key == pygame.K_SPACE:
    if (maxCharacters == -1 or len(text) < maxCharacters) and not onlyNumbers:
      text += " "
  elif len(pygame.key.name(event.key)) < 2:
    if maxCharacters == -1 or len(text) < maxCharacters:
      if not onlyNumbers:
        text += event.unicode
      elif event.unicode.isdigit():
        text += event.unicode

  return text

def scrollScreen(scroll:int) -> int:
  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_RIGHT]:
    if scroll > -level[1]:
      scroll -= 10
  
  if pressedKeys[pygame.K_LEFT]:
    if scroll < 0:
      scroll += 10

  if scroll < -level[1]:
    scroll = -level[1]
  elif scroll > 0:
    scroll = 0

  return scroll

def drawGrid(scroll:int):
  for line in range(20, level[1] + 700, 20):
    pygame.draw.line(screen, (0, 0, 0), (line + scroll, 0), (line + scroll, 499))

  for line in range(20, 500, 20):
    pygame.draw.line(screen, (0, 0, 0), (0, line), (700, line))

def drawObjects(scroll:int):
  for object in list(levelLayout.keys()):
    object.draw(levelLayout[object], scroll)

  if lastPoint != []:
    if currentObstacle == "Ground":
      drawAlphaRect((125, 125, 0, 127), [lastPoint[1][0] + scroll, lastPoint[1][1], mouseX - scroll - lastPoint[1][0], mouseY - lastPoint[1][1]])
    elif currentObstacle == "EndGoal":
      if abs(mouseX - scroll - lastPoint[1][0]) > abs(mouseY - lastPoint[1][1]):
        drawAlphaCircle((0, 255, 0, 127), [lastPoint[1][0] + scroll, lastPoint[1][1]], mouseX - scroll - lastPoint[1][0])
      else:
        drawAlphaCircle((0, 255, 0, 127), [lastPoint[1][0] + scroll, lastPoint[1][1]], mouseY - lastPoint[1][1])
    elif currentObstacle == "Enemy":
      drawAlphaRect((255, 0, 255, 127), [lastPoint[1][0] + scroll, lastPoint[1][1], mouseX - scroll - lastPoint[1][0], mouseY - lastPoint[1][1]])
    elif currentObstacle == "Text":
      textSize = pygame.font.Font("freesansbold.ttf", 30).size(text)
      textWidth = int(textSize[0] / 1.45)

      writeText("freesansbold.ttf", 30, text, (0, 0, 0), (lastPoint[1][0] + scroll, lastPoint[1][1]))
      pygame.draw.rect(screen, (0, 0, 0), (lastPoint[1][0] - (textWidth / 2) - 3 + scroll, lastPoint[1][1] - (textSize[1] / 2) - 3, textWidth + 6, textSize[1] + 6), 3)

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

  # Draw things on top of selector
  pygame.draw.rect(screen, (255, 255, 255), (365, 500, 335, 100))
  pygame.draw.rect(screen, (255, 0, 0), (560, 525, 50, 50))
  pygame.draw.rect(screen, (0, 0, 255), (510, 525, 20, 60))
  pygame.draw.line(screen, (0, 0, 0), (510, 545), (529, 545), 2)
  pygame.draw.line(screen, (0, 0, 0), (510, 565), (529, 565), 2)
  pygame.draw.line(screen, (0, 0, 0), (365, 500), (365, 600), 3)
  pygame.draw.line(screen, (0, 0, 0), (550, 510), (550, 590))
  pygame.draw.circle(screen, (127, 127, 127), (660, 550), 25)
  writeText("freesansbold.ttf", 20, "Max jump height:", (0, 0, 0), (430, 515))
  writeText("freesansbold.ttf", 20, "6-9 boxes", (0, 0, 0), (430, 530))
  writeText("freesansbold.ttf", 20, "Scroll:", (0, 0, 0), (430, 555))
  writeText("freesansbold.ttf", 20, str(-scroll), (0, 0, 0), (430, 570))
  writeText("freesansbold.ttf", 25, "Player", (0, 0, 0), (520, 515))

  # Outline delete button if selected
  if currentObstacle == "Delete":
    pygame.draw.rect(screen, (0, 0, 0), (557, 522, 56, 56), 3)

def drawSideBarRects():
  pygame.draw.rect(screen, (255, 255, 255), (600, 200, 100, 300))
  pygame.draw.line(screen, (0, 0, 0), (600, 499), (700, 499))
  pygame.draw.rect(screen, (0, 0, 2), (610, 210, 80, 40))
  pygame.draw.rect(screen, (0, 0, 3), (610, 285, 80, 40))
  pygame.draw.rect(screen, (0, 2, 0), (640, 360, 50, 25))
  pygame.draw.rect(screen, (0, 3, 0), (640, 395, 50, 25))
  pygame.draw.rect(screen, (0, 4, 0), (610, 435, 80, 40))

def drawSideBarText():
  writeText("freesansbold.ttf", 20, "Print level", (255, 255, 255), (650, 230))
  writeText("freesansbold.ttf", 20, "Level width", (0, 0, 0), (650, 270))
  writeText("freesansbold.ttf", 25, str(levelWidth), (255, 255, 255), (650, 305))
  writeText("freesansbold.ttf", 20, "Player spawn", (0, 0, 0), (650, 345))
  writeText("freesansbold.ttf", 20, "X:", (0, 0, 0), (620, 372))
  writeText("freesansbold.ttf", 20, "Y:", (0, 0, 0), (620, 407))
  writeText("freesansbold.ttf", 20, str(level[3]), (255, 255, 255), (665, 372))
  writeText("freesansbold.ttf", 20, str(level[4]), (255, 255, 255), (665, 407))
  writeText("freesansbold.ttf", 20, "Load level", (255, 255, 255), (650, 455))

while True:
  clock.tick(60)
  checkMouse = False
  mouseX, mouseY = pygame.mouse.get_pos()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      checkMouse = True
    elif event.type == pygame.KEYDOWN:
      if typing:
        text = changeText(event, text)
      elif changingWidth:
        levelWidth = changeText(event, levelWidth, True, 6)

        if len(levelWidth) > 1 and levelWidth[0] == "0":
          levelWidth = levelWidth[1:]
        if levelWidth == "":
          levelWidth = "0"

        level[1] = int(levelWidth)
      elif changingX:
        spawnX = changeText(event, spawnX, True)

        if len(spawnX) > 0:
          if spawnX[0] == "0":
            spawnX = spawnX[1:]
          if int(spawnX) < 0:
            spawnX = "0"
          if int(spawnX) > 350:
            spawnX = "350"
        else:
          spawnX = "0"

        level[3] = int(spawnX)
      elif changingY:
        spawnY = changeText(event, spawnY, True)

        if len(spawnY) > 1:
          if spawnY[0] == "0":
            spawnY = spawnY[1:]
          if int(spawnY) < 0:
            spawnY = "0"
          if int(spawnY) > 460:
            spawnY = "460"
        else:
          spawnY = "0"

        level[4] = int(spawnY)

  screen.fill((0, 255, 255))
  scroll = scrollScreen(scroll)
  drawObjects(scroll)
  drawItemSelecter()
  drawGrid(scroll)
    
  if showSideBar:
    drawSideBarRects()

  if checkMouse:
    if typing:
      if text != "":
        levelLayout[lastPoint[0]] = ["freesansbold.ttf", 30, str(text), (0, 0, 0), [lastPoint[1][0], lastPoint[1][1]], 1, None]
        text = ""

      typing = False
    
    changingWidth = False
    changingX = False
    changingY = False
    screenColor = screen.get_at((mouseX, mouseY))

    if screenColor == (0, 0, 2, 255):
      levelLayoutToPrint = {}
      i = 0

      for key in list(levelLayout.keys()):
        levelLayoutToPrint[str(key).split(".")[1].split(" ")[0] + "()" + str(i)] = levelLayout[key]
        i += 1

      with open("levelMaker/level.JSON", "w") as writeFile:
        writeFile.truncate(0)
        writeFile.write(json.dumps([level, levelLayoutToPrint]))

    elif screenColor == (0, 0, 3, 255):
      changingWidth = True
    elif screenColor == (0, 2, 0, 255):
      changingX = True
    elif screenColor == (0, 3, 0, 255):
      changingY = True
    elif screenColor == (0, 4, 0, 255):
      savedLevel = level
      savedLevelLayout = levelLayout
      try:
        with open("levelMaker/levelLoader.JSON", "r") as readFile:
          levelInfo = json.loads(readFile.read())
          level = levelInfo[0]
          levelLayout = {}
          
          for object in list(levelInfo[1].keys()):
            levelLayout[eval(object[:-1])] = levelInfo[1][object]

        lastPoint = []
        currentObstacle = None
        scroll = 0
        typing = False
        text = ""
        changingWidth = False
        levelWidth = str(level[1])
        changingX = False
        spawnX = str(level[3])
        changingY = False
        spawnY = str(level[4])
      except:
        level = savedLevel
        levelLayout = savedLevelLayout

        with open("levelMaker/levelLoader.JSON", "a") as writeFile:
          writeFile.write('\n"Failed to load level!"')
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
          lastPoint = [eval(currentObstacle)(), [mouseX - scroll, mouseY], scroll]
        else:
          if currentObstacle != "EndGoal":
            if mouseX - scroll - lastPoint[1][0] < 0:
              width = lastPoint[1][0] - mouseX - scroll
              lastPoint[1][0] = mouseX - scroll
            else:
              width = mouseX - scroll - lastPoint[1][0]

            if mouseY - lastPoint[1][1] < 0:
              height = lastPoint[1][1] - mouseY
              lastPoint[1][1] = mouseY
            else:
              height = mouseY - lastPoint[1][1]

            levelLayout[lastPoint[0]] = [lastPoint[1][0], lastPoint[1][1], width, height]
          else:
            width = abs(mouseX - scroll - lastPoint[1][0])

            if abs(mouseY - lastPoint[1][1] > width):
              width = abs(mouseY - lastPoint[1][1])

            levelLayout[lastPoint[0]] = [lastPoint[1][0], lastPoint[1][1], width]

          lastPoint = []  
      elif currentObstacle == "Delete":
        for obstacle in list(levelLayout.keys()):
          if str(obstacle).split(".")[1].split(" ")[0] == "EndGoal":
            if mouseX - scroll > levelLayout[obstacle][0] - levelLayout[obstacle][2] and mouseX - scroll < levelLayout[obstacle][0] + levelLayout[obstacle][2] and mouseY > levelLayout[obstacle][1] - levelLayout[obstacle][2] and mouseY < levelLayout[obstacle][1] + levelLayout[obstacle][2]:
              levelLayout.pop(obstacle)
          elif str(obstacle).split(".")[1].split(" ")[0] == "Text":
            textSize = pygame.font.Font(levelLayout[obstacle][0], levelLayout[obstacle][1]).size(levelLayout[obstacle][2])
            
            if mouseX - scroll > levelLayout[obstacle][4][0] - textSize[0] / 2 and mouseX - scroll < levelLayout[obstacle][4][0] + textSize[0] / 2 and mouseY > levelLayout[obstacle][4][1] - textSize[1] / 2 and mouseY < levelLayout[obstacle][4][1] + textSize[1] / 2:
              levelLayout.pop(obstacle)
          else:
            if mouseX - scroll > levelLayout[obstacle][0] and mouseX - scroll < levelLayout[obstacle][0] + levelLayout[obstacle][2] and mouseY > levelLayout[obstacle][1] and mouseY < levelLayout[obstacle][1] + levelLayout[obstacle][3]:
              levelLayout.pop(obstacle)
      elif currentObstacle == "Text":
        typing = True
        lastPoint = [eval(currentObstacle)(), [mouseX - scroll, mouseY], scroll]

    else:
      lastPoint = []
      currentObstacle = None
  
  if showSideBar:
    drawSideBarText()

  pygame.display.flip()