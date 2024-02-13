import pygame

from globalVariables import globalVariables

def collisionCheck(spriteX, spriteY, spriteWidth, spriteHeight, spriteDownwardMovemomentSpeed):
  collisionDetected = {
      "Top": False,
      "Bottom": False,
      "Left": False,
      "Right": False
    }

  if not 0 >= spriteX >= globalVariables["screenWidth"] or not 0 >= spriteY >= globalVariables["screenHeight"]:
    for xPos in range(int(spriteX), int(spriteX + spriteWidth)):
      if globalVariables["screen"].get_at((xPos, int(spriteY + spriteHeight + spriteDownwardMovemomentSpeed))) == globalVariables["groundColor"]:
        collisionDetected["Bottom"] = True
          
      if globalVariables["screen"].get_at((xPos, int(spriteY))) == globalVariables["groundColor"]:
        collisionDetected["Top"] = True
    
    for yPos in range(int(spriteY), int(spriteY + spriteHeight)):
      if globalVariables["screen"].get_at((int(spriteX), yPos)) == globalVariables["groundColor"]:
        collisionDetected["Left"] = True
        
      if globalVariables["screen"].get_at((int(spriteX + spriteWidth + 1.6), yPos)) == globalVariables["groundColor"]:
        collisionDetected["Right"] = True
        
    return collisionDetected
  
  else:
    raise IndexError()