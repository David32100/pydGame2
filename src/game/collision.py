from globalVariables import globalVariables

def collisionCheck(spriteX: float, spriteY: float, spriteWidth: int, spriteHeight: int, colorOfObject: tuple):
  collisionDetected = {
      "Top": False,
      "Bottom": False,
      "Left": False,
      "Right": False
    }

  if spriteX > 0 and (spriteX + spriteWidth) < globalVariables["screenWidth"] and spriteY > 0 and (spriteY + spriteHeight) < globalVariables["screenHeight"]:
    for xPos in range(int(spriteX), int(spriteX + spriteWidth)):
      if globalVariables["screen"].get_at((xPos, int(spriteY + spriteHeight))) == colorOfObject:
        collisionDetected["Bottom"] = True
          
      if globalVariables["screen"].get_at((xPos, int(spriteY))) == colorOfObject:
        collisionDetected["Top"] = True
    
    for yPos in range(int(spriteY), int(spriteY + spriteHeight)):
      if globalVariables["screen"].get_at((int(spriteX), yPos)) == colorOfObject:
        collisionDetected["Left"] = True
        
      if globalVariables["screen"].get_at((int(spriteX + spriteWidth), yPos)) == colorOfObject:
        collisionDetected["Right"] = True
        
    return collisionDetected
  
  else:
    return {"Top": True, "Bottom": True, "Left": True, "Right": True}