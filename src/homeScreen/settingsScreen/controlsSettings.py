import pygame

from globalVariables import globalVariables
from drawingFunctions import writeText

def drawJumpingScreen(checkMouse, newUserSettings, addingButton, buttonPressed):
  if not addingButton:
    writeText("freesansbold.ttf", 35, "Jumping", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
    writeText("freesansbold.ttf", 30, "The keys that make the player", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
    writeText("freesansbold.ttf", 30, "jump.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))

    for keyIndex in range(len(newUserSettings["controls"]["jump"])):
      pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["jump"]) + 1))) - 175, 200, 50, 50))
      writeText("freesansbold.ttf", 25, str(pygame.key.name(newUserSettings["controls"]["jump"][keyIndex])), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["jump"]) + 1))) - 150, 225))

    if len(newUserSettings["controls"]["jump"]) == 0:
      writeText("freesansbold.ttf", 30, "No keys are set to jumping.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))

    pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 12, 275, 50, 50))
    pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 62, 275, 50, 50))

    if checkMouse:
      screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())

      if screenColor == (2, 0, 0, 255) and len(newUserSettings["controls"]["jump"]) < 3:
        return True
      elif screenColor == (1, 0, 0, 255) and len(newUserSettings["controls"]["jump"]) > 0:
        newUserSettings["controls"]["jump"].pop(-1)

    writeText("freesansbold.ttf", 30, "+", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 37, 300))
    writeText("freesansbold.ttf", 30, "-", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 37, 300))
    return False
  else:
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (globalVariables["screenWidth"] / 2, 0, globalVariables["screenWidth"] / 2, globalVariables["screenHeight"]))
    writeText("freesansbold.ttf", 30, "Click any button or click", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) - 12))
    writeText("freesansbold.ttf", 30, "the screen to cancel.", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) + 12))
    
    if checkMouse:
      return False
      
    if buttonPressed != None and not " " in pygame.key.name(buttonPressed) and buttonPressed != pygame.K_ESCAPE:
      newUserSettings["controls"]["jump"].append(buttonPressed)
      return False

    return True

def drawMovingLeftScreen(checkMouse, newUserSettings, addingButton, buttonPressed):
  if not addingButton:
    writeText("freesansbold.ttf", 35, "Moving left", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
    writeText("freesansbold.ttf", 30, "The keys that make the player", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
    writeText("freesansbold.ttf", 30, "move left.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))

    for keyIndex in range(len(newUserSettings["controls"]["left"])):
      pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["left"]) + 1))) - 175, 200, 50, 50))
      writeText("freesansbold.ttf", 25, str(pygame.key.name(newUserSettings["controls"]["left"][keyIndex])), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["left"]) + 1))) - 150, 225))

    if len(newUserSettings["controls"]["left"]) == 0:
      writeText("freesansbold.ttf", 30, "No keys are set to moving left.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))

    pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 12, 275, 50, 50))
    pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 62, 275, 50, 50))

    if checkMouse:
      screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())

      if screenColor == (2, 0, 0, 255) and len(newUserSettings["controls"]["left"]) < 3:
        return True
      elif screenColor == (1, 0, 0, 255) and len(newUserSettings["controls"]["left"]) > 0:
        newUserSettings["controls"]["left"].pop(-1)

    writeText("freesansbold.ttf", 30, "+", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 37, 300))
    writeText("freesansbold.ttf", 30, "-", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 37, 300))
    return False
  else:
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (globalVariables["screenWidth"] / 2, 0, globalVariables["screenWidth"] / 2, globalVariables["screenHeight"]))
    writeText("freesansbold.ttf", 30, "Click any button or click", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) - 12))
    writeText("freesansbold.ttf", 30, "the screen to cancel.", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) + 12))
    
    if checkMouse:
      return False
      
    if buttonPressed != None and not " " in pygame.key.name(buttonPressed) and buttonPressed != pygame.K_ESCAPE:
      newUserSettings["controls"]["left"].append(buttonPressed)
      return False
  
    return True

def drawMovingRightScreen(checkMouse, newUserSettings, addingButton, buttonPressed):
  if not addingButton:
    writeText("freesansbold.ttf", 35, "Moving right", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
    writeText("freesansbold.ttf", 30, "The keys that make the player", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
    writeText("freesansbold.ttf", 30, "move right.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))

    for keyIndex in range(len(newUserSettings["controls"]["right"])):
      pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["right"]) + 1))) - 175, 200, 50, 50))
      writeText("freesansbold.ttf", 25, str(pygame.key.name(newUserSettings["controls"]["right"][keyIndex])), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["right"]) + 1))) - 150, 225))

    if len(newUserSettings["controls"]["right"]) == 0:
      writeText("freesansbold.ttf", 30, "No keys are set to moving right.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))

    pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 12, 275, 50, 50))
    pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 62, 275, 50, 50))

    if checkMouse:
      screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())

      if screenColor == (2, 0, 0, 255) and len(newUserSettings["controls"]["right"]) < 3:
        return True
      elif screenColor == (1, 0, 0, 255) and len(newUserSettings["controls"]["right"]) > 0:
        newUserSettings["controls"]["right"].pop(-1)

    writeText("freesansbold.ttf", 30, "+", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 37, 300))
    writeText("freesansbold.ttf", 30, "-", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 37, 300))
    return False
  else:
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (globalVariables["screenWidth"] / 2, 0, globalVariables["screenWidth"] / 2, globalVariables["screenHeight"]))
    writeText("freesansbold.ttf", 30, "Click any button or click", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) - 12))
    writeText("freesansbold.ttf", 30, "the screen to cancel.", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) + 12))
    
    if checkMouse:
      return False
      
    if buttonPressed != None and not " " in pygame.key.name(buttonPressed) and buttonPressed != pygame.K_ESCAPE:
      newUserSettings["controls"]["right"].append(buttonPressed)
      return False

    return True

def drawTalkingScreen(checkMouse, newUserSettings, addingButton, buttonPressed):
  if not addingButton:
    writeText("freesansbold.ttf", 35, "Moving left", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 100))
    writeText("freesansbold.ttf", 30, "The keys that make the player", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 150))
    writeText("freesansbold.ttf", 30, "start and stop talking.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 175))

    for keyIndex in range(len(newUserSettings["controls"]["talk"])):
      pygame.draw.rect(globalVariables["screen"], (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["talk"]) + 1))) - 175, 200, 50, 50))
      writeText("freesansbold.ttf", 25, str(pygame.key.name(newUserSettings["controls"]["talk"][keyIndex])), (0, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + (300 * ((keyIndex + 1) / (len(newUserSettings["controls"]["talk"]) + 1))) - 150, 225))

    if len(newUserSettings["controls"]["talk"]) == 0:
      writeText("freesansbold.ttf", 30, "No keys are set to talking.", (0, 0, 0), (globalVariables["screenWidth"] * (3 / 4), 225))

    pygame.draw.rect(globalVariables["screen"], (1, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) + 12, 275, 50, 50))
    pygame.draw.rect(globalVariables["screen"], (2, 0, 0), ((globalVariables["screenWidth"] * (3 / 4)) - 62, 275, 50, 50))

    if checkMouse:
      screenColor = globalVariables["screen"].get_at(pygame.mouse.get_pos())

      if screenColor == (2, 0, 0, 255) and len(newUserSettings["controls"]["talk"]) < 3:
        return True
      elif screenColor == (1, 0, 0, 255) and len(newUserSettings["controls"]["talk"]) > 0:
        newUserSettings["controls"]["talk"].pop(-1)

    writeText("freesansbold.ttf", 30, "+", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) - 37, 300))
    writeText("freesansbold.ttf", 30, "-", (255, 255, 255), ((globalVariables["screenWidth"] * (3 / 4)) + 37, 300))
    return False
  else:
    pygame.draw.rect(globalVariables["screen"], (0, 255, 255), (globalVariables["screenWidth"] / 2, 0, globalVariables["screenWidth"] / 2, globalVariables["screenHeight"]))
    writeText("freesansbold.ttf", 30, "Click any button or click", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) - 12))
    writeText("freesansbold.ttf", 30, "the screen to cancel.", (255, 255, 255), (globalVariables["screenWidth"] * (3 / 4), (globalVariables["screenHeight"] / 2) + 12))
    
    if checkMouse:
      return False
      
    if buttonPressed != None and not " " in pygame.key.name(buttonPressed) and buttonPressed != pygame.K_ESCAPE:
      newUserSettings["controls"]["talk"].append(buttonPressed)
      return False
    
    return True