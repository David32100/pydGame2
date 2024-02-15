from globalVariables import globalVariables

boxColor = (127, 0, 0, 255)

def drawSettingsBox(pygameDraw):
  pygameDraw(globalVariables["screen"], boxColor, ((globalVariables["screenWidth"] / 2) + 230, (globalVariables["screenHeight"] / 2) - 230, 100, 40))
  
def drawSettingsText(writeText):
  writeText("freesansbold.ttf", 30, "Settings", (0, 0, 0), ((globalVariables["screenWidth"] / 2) + 280, (globalVariables["screenHeight"] / 2) - 210))

def settings():
  print("Settings: WIP")

settingsEvent = (boxColor, settings)