import pygame

from levelMakerGlobalVariables import screen

def drawAlphaRect(color:tuple, rect:list) -> pygame.Surface:
  if rect[2] < 0:
    rect[0] = rect[0] + rect[2]
    rect[2] = -rect[2]

  if rect[3] < 0:
    rect[1] = rect[1] + rect[3]
    rect[3] = -rect[3]

  alphaRect = pygame.Surface((rect[2], rect[3]))
  alphaRect.set_alpha(color[3])
  alphaRect.fill(color[:3])
  screen.blit(alphaRect, rect[:2])
  return alphaRect

def drawAlphaCircle(color:tuple, center:list, radius:float) -> pygame.Surface:
  radius = abs(radius)
  alphaCircle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
  alphaCircle.fill((0, 0, 0, 0))
  pygame.draw.circle(alphaCircle, color, (radius, radius), radius)
  screen.blit(alphaCircle, (center[0] - radius, center[1] - radius))
  return alphaCircle

def writeText(font: str, size: int, text: str, color: tuple,  textPosition: tuple, positionedByPoint: int = 1, background: tuple = None) -> tuple:
  """
    positionedByPoint: How to position text, 1 - center, 2-9  - top left corner clockwise to middle left side
  """

  font = pygame.font.SysFont(font, size)
  text = font.render(text, True, color, background)

  textRect = text.get_rect()
  
  if positionedByPoint == 1:
    textRect.center = textPosition
  elif positionedByPoint == 2:
    textRect.topleft = textPosition
  elif positionedByPoint == 3:
    textRect.top = textPosition
  elif positionedByPoint == 4:
    textRect.topright = textPosition
  elif positionedByPoint == 5:
    textRect.midright = textPosition
  elif positionedByPoint == 6:
    textRect.bottomright = textPosition
  elif positionedByPoint == 7:
    textRect.bottom = textPosition
  elif positionedByPoint == 8:
    textRect.bottomleft = textPosition
  else:
    textRect.midleft = textPosition

  screen.blit(text, textRect)

  return text, textRect