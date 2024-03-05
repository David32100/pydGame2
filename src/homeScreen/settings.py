import pygame

from globalVariables import globalVariables
from drawingFunctions import shutdownGame, writeText

boxColor = (127, 0, 0, 255)

def drawSettingsBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) + 230, (globalVariables["screenHeight"] / 2) - 230, 100, 40))
  
def drawSettingsText(writeText):
  writeText("freesansbold.ttf", 30, "Settings", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 280, (globalVariables["screenHeight"] / 2) - 210))

def settings():
  changingSettings = True
  checkMouse = False
  currentTab = "general"
  scroll = 0
  maxScroll = 500

  while changingSettings:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        globalVariables["veiwingHomeScreen"] = False
        changingSettings = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_UP] and scroll < maxScroll:
      scroll += 1
    elif pressedKeys[pygame.K_DOWN] and scroll > 0:
      scroll -= 1

    globalVariables["screen"].fill((0, 255, 255))

    if currentTab == "general":
      pygame.draw.line(globalVariables["screen"], (0, 0, 0), (globalVariables["screenWidth"] / 2, 0), (globalVariables["screenWidth"] / 2, globalVariables["screenHeight"]))
      pygame.draw.rect(globalVariables["screen"], (0, 0, 0), (100, 110 + scroll, 100, 50))
    elif currentTab == "player":
      pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 100, 110 + scroll, 100, 50))
    elif currentTab == "account":
      pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 200, 110 + scroll, 100, 50))
    elif currentTab == "controls":
      pygame.draw.rect(globalVariables["screen"], (0, 0, 0), ((globalVariables["screenWidth"] / 2) - 300, 110 + scroll, 100, 50))

    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (0, 0, globalVariables["screenWidth"], 100))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (0, 400, globalVariables["screenWidth"], globalVariables["screenHeight"] - 400))
    pygame.draw.line(globalVariables["screen"], (0, 0, 0), (10, 100), (globalVariables["screenWidth"] - 10, 100), 2)
    pygame.draw.line(globalVariables["screen"], (0, 0, 0), (10, 400), (globalVariables["screenWidth"] - 10, 400), 2)
    pygame.draw.rect(globalVariables["screen"], (255, 0, 0), ((globalVariables["screenWidth"] / 4) - 137.5, 25, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 255, 0), ((globalVariables["screenWidth"] * (1 / 2)) - 137.5, 25, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 0, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 137.5, 25, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (127, 0, 0), (globalVariables["screenWidth"] - 137.5, 25, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 127, 0), (globalVariables["screenWidth"] * (3 / 5), 425, 100, 50))
    pygame.draw.rect(globalVariables["screen"], (0, 0, 127), (globalVariables["screenWidth"] / 4, 425, 100, 50))

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (255, 0, 0, 255):
        currentTab = "general"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 255, 0, 255):
        currentTab = "player"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 0, 255, 255):
        currentTab = "account"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (127, 0, 0, 255):
        currentTab = "controls"
      elif globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 127, 0, 255):
        changingSettings = False

      checkMouse = False

    writeText("freesansbold.ttf", 30, "General", (0, 0, 0), ((globalVariables["screenWidth"] / 4) - 87.5, 50))
    writeText("freesansbold.ttf", 30, "Player", (0, 0, 0), ((globalVariables["screenWidth"] * (1 / 2)) - 87.5, 50))
    writeText("freesansbold.ttf", 30, "Account", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 87.5, 50))
    writeText("freesansbold.ttf", 30, "Controls", (0, 0, 0), (globalVariables["screenWidth"] - 87.5, 50))
    writeText("freesansbold.ttf", 30, "Back", (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 5)) + 50, 450))
    writeText("freesansbold.ttf", 30, "Save", (0, 0, 0), ((globalVariables["screenWidth"] / 4) + 50, 450))
    
    pygame.display.flip()

settingsEvent = (boxColor, settings)