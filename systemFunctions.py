import sys
import pygame

from globalVariables import globalVariables, updateGameProgress
from levels import levels
from communications import shutdownGameClient, sendAMessage

def writeText(font: str, size: int, text: str, color: tuple,  textPosition: tuple, background: tuple = None):
  font = pygame.font.SysFont(font, size)
  text = font.render(text, True, color, background)

  textRect = text.get_rect()
  textRect.center = textPosition

  globalVariables["screen"].blit(text, textRect)

  return text, textRect

# All noto fonts: 'notosans', 'notosanslaoui', 'notosansarmenian', 'notosansosmanya', 'notosansadlam', 'notosansrejang', 'notosansphoenician', 'notosanstagbanwa', 'notoserif', 'notosansinscriptionalparthian', 'notosanscjksc', 'notoemoji', 'notosansgujaratiui', 'notosanslimbu', 'notoserifkannada',  'notoseriftelugu', 'notosansphagspa', 'notosanskhmer', 'notosansgujarati', 'notosanslao', 'notosansnko', 'notosansdevanagari',  'notosansmonocjkhk', 'notosansmonocjkkr', 'notosansmonocjkjp', 'notosansgurmukhi', 'notosanslycian', 'notosansmonocjktc', 'notosansmonocjksc', 'notosansogham', 'notosanstamil', 'notosansoriyaui', 'notosanssundanese', 'notosanskannadaui', 'notosanstibetan', 'notosansethiopic',  'notosansthaana', 'notosanscjktc', 'notosansthai', 'notosanscjkjp', 'notosanscjkhk', 'notosanscjkkr', 'notoserifarmenian', 'notoserifmyanmar', 'notosansegyptianhieroglyphs', 'notoserifkhmer', 'notoserifbengali', 'notosansbamum', 'notosansolchiki', 'notosanskhmerui', 'notosanssyriacestrangela', 'notosansgothic', 'notosansbatak', 'notosanscherokee', 'notosansmath', 'notonaskharabicui', 'notosansmyanmarui', 'notosansbuhid', 'notosansbengaliui', 'notosansimperialaramaic', 'notosansdeseret', 'notosansoriya', 'notosanskayahli', 'notoserifmalayalam', 'notonaskharabic', 'notosansarabicui', 'notosanstaiviet', 'notosanstaile', 'notoserifcjkjp', 'notosansgurmukhiui', 'notosansmono', 'notosanscarian', 'notoseriflao', 'notosanstifinagh', 'notosansglagolitic', 'notoserifgeorgian', 'notoserifthai', 'notosanskannada', 'notosanshanunoo', 'notosansdevanagariui', 'notosansmyanmar', 'notosanssinhalaui', 'notosanskharoshthi', 'notosanscham', 'notosansteluguui', 'notosansrunic', 'notosanslepcha', 'notosansbuginese', 'notosansnewtailue', 'notoserifhebrew', 'notosanssinhala', 'notosanslydian', 'notosanskaithi', 'notosanscanadianaboriginal', 'notoserifethiopic', 'notosanstelugu', 'notonastaliqurdu', 'notosansavestan', 'notosansbengali', 'notosanscypriot', 'notosansyi', 'notosanslisu', 'notosanstamilui', 'notosanstagalog', 'notosansinscriptionalpahlavi', 'notosanssaurashtra', 'notosansoldsoutharabian', 'notosanslinearb', 'notosanssamaritan', 'notoserifdevanagari', 'notosanssyriaceastern', 'notosansmeeteimayek', 'notoserifsinhala', 'notosansmalayalamui', 'notoserifcjkkr',  'notosansanatolianhieroglyphs', 'notosansmandaic', 'notosansosage', 'notosanscoptic', 'notosansbalinese',  'notosanssymbols', 'notoserifcjktc', 'notocoloremoji', 'notoserifcjksc', 'notosansolditalic', 'notosansthaiui', 'notosansarabic', 'notosansgeorgian', 'notosansmalayalam', 'notosanssymbols2', 'notoserifgujarati', 'notosansmongolian', 'notosanshebrew', 'notosansoldpersian', 'notosansvai', 'notosanssylotinagri', 'notosansjavanese', 'notosanschakma', 'notosansugaritic', 'notoseriftamil', 'notosanssyriacwestern', 'notosanstaitham', 'notosansbrahmi', 'notosansoldturkic', 'notosanscuneiform', 'notosansshavian'
# All non-noto fonts: 'lohitodia', 'dejavusansmono', 'dejavuserif', 'tinos', 'arimo', 'googlesans', 'dejavusans', 'caladea', 'wingdings2', 'roboto', 'wingdings3', 'arialnarrow', 'webdings', 'jomolhari', 'nanumgothic', 'georgia', 'carlito', 'cousine', 'verdana', 'tahoma', 'bizudpgothic', 'comicsansms', 'garamond', 'wingdings', 'lohitpunjabi', 'arialblack', 'bizudpmincho', 'ipaexmincho'

def checkIfTouchingColor(spriteX, spriteY, spriteWidth, spriteHeight, colorToCheckFor):
  for xPos in range(int(spriteX), int(spriteX + spriteWidth)):
    for yPos in range(int(spriteY), int(spriteY + spriteHeight)):
      if globalVariables["screen"].get_at((xPos, yPos)) == colorToCheckFor:
        return True
      
  return False

def shutdownGame():
  sendAMessage({"action":"updateStatus","contents":{"Username": globalVariables["username"], "Status":"Offline"}})
  shutdownGameClient()
  pygame.quit()
  updateGameProgress()
  sys.exit()

def drawGameAndUpdateJumperPosition(jumper):
  globalVariables["screen"].fill((0, 128, 128))
  
  for object in levels[globalVariables["currentLevel"]][2]:
    objectRect = levels[globalVariables["currentLevel"]][2][object]
    object.draw((objectRect[0] - globalVariables["scroll"], objectRect[1], objectRect[2], objectRect[3]))

  pressedKeys = pygame.key.get_pressed()

  for key in list(jumper.keyBinds.keys()):
    if pressedKeys[key]:
      jumper.keyBinds[key](jumper.speed)

  jumper.scrollScreen(jumper.speed)
  jumper.experienceGravity()
  jumper.winLevelIfTouchingGoal()
  sendAMessage({"action":"updatePlayer", "contents":{"Username":globalVariables["username"], "Lobby":globalVariables["lobby"], "postion":(jumper.jumperXWithScroll, jumper.jumperY)}})
  jumper.drawJumper()

def drawDeathScreen(jumper):
  globalVariables["screen"].fill((255, 0, 0))
  writeText("arialblack", 50, "Game Over", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 50))
  writeText("roboto", 25, "Click Space to restart and b + y + e to go to home screen", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 50))

  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_SPACE]:
    jumper.resetJumper()
    sendAMessage({"action":"updatePlayer", "contents":{"Username": globalVariables["username"], "Lobby": globalVariables["lobby"], "postion":(jumper.jumperXWithScroll, jumper.jumperY)}})
  if pressedKeys[pygame.K_b] and pressedKeys[pygame.K_y] and pressedKeys[pygame.K_e]:
    globalVariables["veiwingHomeScreen"] = True
    globalVariables["playingGame"] = False
    jumper.resetJumper()
    sendAMessage({"action":"leaveGame", "contents":{"Username":globalVariables["username"], "Lobby":globalVariables["lobby"]}})
    sendAMessage({"action":"updateStatus", "contents":{"Username":globalVariables["username"], "status":"Not in game"}})

def drawWinScreen(jumper):
  globalVariables["screen"].fill((127, 127, 0))
  writeText("arialblack", 50, "Level Complete", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 50))
  writeText("roboto", 30, "Click r to restart and b + y + e to go to home screen", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 50))

  if globalVariables["currentLevel"] == globalVariables["discoveredLevels"]:
    globalVariables["discoveredLevels"] += 1

  pressedKeys = pygame.key.get_pressed()

  if pressedKeys[pygame.K_r]:
    jumper.resetJumper()
    sendAMessage({"action":"updatePlayer", "contents":{"Username":globalVariables["username"], "Lobby":globalVariables["lobby"], "postion":(jumper.jumperXWithScroll, jumper.jumperY)}})
  if pressedKeys[pygame.K_b] and pressedKeys[pygame.K_y] and pressedKeys[pygame.K_e]:
    globalVariables["veiwingHomeScreen"] = True
    globalVariables["playingGame"] = False
    jumper.resetJumper()
    sendAMessage({"action":"leaveGame", "contents":{"Username":globalVariables["username"], "Lobby":globalVariables["lobby"]}})
    sendAMessage({"action":"updateStatus", "contents":{"Username":globalVariables["username"], "status":"Not in game"}})

def drawHomeScreen(checkMouseEvent: bool) -> str:
  globalVariables["screen"].fill((0, 255, 255))
  pygame.draw.rect(globalVariables["screen"], (255, 0, 0, 255), ((globalVariables["screenWidth"] / 2) - 150, (globalVariables["screenHeight"] / 2) - 100, 300, 90))
  pygame.draw.rect(globalVariables["screen"], (0, 255, 0, 255), ((globalVariables["screenWidth"] / 2) - 150, (globalVariables["screenHeight"] / 2) + 10, 300, 90))
  pygame.draw.rect(globalVariables["screen"], (0, 0, 255, 255), ((globalVariables["screenWidth"] / 2) - 150, (globalVariables["screenHeight"] / 2) + 120, 300, 90))
  pygame.draw.rect(globalVariables["screen"], (127, 0, 0, 255), ((globalVariables["screenWidth"] / 2) + 230, (globalVariables["screenHeight"] / 2) - 230, 100, 40))

  if checkMouseEvent:
    mouseX, mouseY = pygame.mouse.get_pos()
    pixelColor = globalVariables["screen"].get_at((mouseX, mouseY))

    if pixelColor == (255, 0, 0, 255):
      return "Game"
    elif pixelColor == (0, 255, 0, 255):
      return "Level"
    elif pixelColor == (0, 0, 255, 255):
      return "Party"
    elif pixelColor == (127, 0, 0, 255):
      return "Settings"

    checkMouseEvent = False

  writeText("freesansbold.ttf", 75, "Game Title", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 175))
  writeText("freesansbold.ttf", 30, "By: David G", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 70, (globalVariables["screenHeight"] / 2) - 145))
  writeText("freesansbold.ttf", 50, "Join Game", (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) - 65))
  writeText("freesansbold.ttf", 30, "Level: " + str(globalVariables["currentLevel"]), (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) - 35))
  writeText("freesansbold.ttf", 50, "Level Select", (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) + 57))
  writeText("freesansbold.ttf", 50, "Join Party", (0, 0, 0), ((globalVariables["screenWidth"] / 2), (globalVariables["screenHeight"] / 2) + 167))
  writeText("freesansbold.ttf", 30, "Settings", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 280, (globalVariables["screenHeight"] / 2) - 210))

def drawLevels(levelScroll):
  for g in range(256):
    for r in range(256):
      if (g * 255) + r <= len(levels) - 1 and (g * 255) + r <= globalVariables["discoveredLevels"]:
        if ((g * 255) + r) % 2 == 0:
          pygame.draw.rect(globalVariables["screen"], (r, g, 0), ((((g * 255) + r) * 75) + 10 - levelScroll, (globalVariables["screenHeight"] / 2) - 100, 75, 75))
        else:
          pygame.draw.rect(globalVariables["screen"], (r, g, 0), (((((g * 255) + r) - 1) * 75) + 10 - levelScroll, (globalVariables["screenHeight"] / 2) + 50, 75, 75))      

def drawSelectLevel():
  selectingLevel = True
  levelScroll = 0
  checkMouse = False

  while selectingLevel:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        selectingLevel = False
        globalVariables["veiwingHomeScreen"] = False
        shutdownGame()
      if event.type == pygame.MOUSEBUTTONDOWN:
        checkMouse = True

    globalVariables["screen"].fill((0, 255, 255))
    drawLevels(levelScroll)
    pygame.draw.rect(globalVariables["screen"], (0, 0, 255, 255), ((globalVariables["screenWidth"] / 2) - 75, (globalVariables["screenHeight"] / 2) + 150, 150, 75))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and levelScroll < 177725:
      levelScroll += 5
    if keys[pygame.K_LEFT] and levelScroll > 0:
      levelScroll -= 5

    if checkMouse:
      mouseX, mouseY = pygame.mouse.get_pos()

      if globalVariables["screen"].get_at((mouseX, mouseY)) == (0, 0, 255, 255):
        selectingLevel = False

      for g in range(255):
        for r in range(255):
          if globalVariables["screen"].get_at((mouseX, mouseY)) == (r, g, 0, 255):
            globalVariables["currentLevel"] = (g * 255) + r
            selectingLevel = False

      checkMouse = False
        
    writeText("freesansbold.ttf", 35, "Back", (255, 255, 255, 255), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) + 187))
    writeText("freesansbold.ttf", 50, "Select a level", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 200))
    writeText("freesansbold.ttf", 30, "Use the arrow keys to move through the levels", (0, 0, 0), (globalVariables["screenWidth"] / 2, (globalVariables["screenHeight"] / 2) - 150))

    for levelIndex in range(0, len(levels)):
      if levelIndex <= globalVariables["discoveredLevels"]:
        if levelIndex % 2 == 0:
          writeText("freesansbold.ttf", 30, str(levelIndex), (255, 255, 255), (((levelIndex) * 75) + 48 - levelScroll, (globalVariables["screenHeight"] / 2) - 62))
        else:
          writeText("freesansbold.ttf", 30, str(levelIndex), (255, 255, 255), (((levelIndex - 1) * 75) + 48 - levelScroll, (globalVariables["screenHeight"] / 2) + 88))
      
    pygame.display.flip()