import sys
import pygame

from globalVariables import globalVariables
from client.communications import shutdownGameClient, sendAMessage
from savingFunctions import updateGameProgress

# All noto fonts: 'notosans', 'notosanslaoui', 'notosansarmenian', 'notosansosmanya', 'notosansadlam', 'notosansrejang', 'notosansphoenician', 'notosanstagbanwa', 'notoserif', 'notosansinscriptionalparthian', 'notosanscjksc', 'notoemoji', 'notosansgujaratiui', 'notosanslimbu', 'notoserifkannada',  'notoseriftelugu', 'notosansphagspa', 'notosanskhmer', 'notosansgujarati', 'notosanslao', 'notosansnko', 'notosansdevanagari',  'notosansmonocjkhk', 'notosansmonocjkkr', 'notosansmonocjkjp', 'notosansgurmukhi', 'notosanslycian', 'notosansmonocjktc', 'notosansmonocjksc', 'notosansogham', 'notosanstamil', 'notosansoriyaui', 'notosanssundanese', 'notosanskannadaui', 'notosanstibetan', 'notosansethiopic',  'notosansthaana', 'notosanscjktc', 'notosansthai', 'notosanscjkjp', 'notosanscjkhk', 'notosanscjkkr', 'notoserifarmenian', 'notoserifmyanmar', 'notosansegyptianhieroglyphs', 'notoserifkhmer', 'notoserifbengali', 'notosansbamum', 'notosansolchiki', 'notosanskhmerui', 'notosanssyriacestrangela', 'notosansgothic', 'notosansbatak', 'notosanscherokee', 'notosansmath', 'notonaskharabicui', 'notosansmyanmarui', 'notosansbuhid', 'notosansbengaliui', 'notosansimperialaramaic', 'notosansdeseret', 'notosansoriya', 'notosanskayahli', 'notoserifmalayalam', 'notonaskharabic', 'notosansarabicui', 'notosanstaiviet', 'notosanstaile', 'notoserifcjkjp', 'notosansgurmukhiui', 'notosansmono', 'notosanscarian', 'notoseriflao', 'notosanstifinagh', 'notosansglagolitic', 'notoserifgeorgian', 'notoserifthai', 'notosanskannada', 'notosanshanunoo', 'notosansdevanagariui', 'notosansmyanmar', 'notosanssinhalaui', 'notosanskharoshthi', 'notosanscham', 'notosansteluguui', 'notosansrunic', 'notosanslepcha', 'notosansbuginese', 'notosansnewtailue', 'notoserifhebrew', 'notosanssinhala', 'notosanslydian', 'notosanskaithi', 'notosanscanadianaboriginal', 'notoserifethiopic', 'notosanstelugu', 'notonastaliqurdu', 'notosansavestan', 'notosansbengali', 'notosanscypriot', 'notosansyi', 'notosanslisu', 'notosanstamilui', 'notosanstagalog', 'notosansinscriptionalpahlavi', 'notosanssaurashtra', 'notosansoldsoutharabian', 'notosanslinearb', 'notosanssamaritan', 'notoserifdevanagari', 'notosanssyriaceastern', 'notosansmeeteimayek', 'notoserifsinhala', 'notosansmalayalamui', 'notoserifcjkkr',  'notosansanatolianhieroglyphs', 'notosansmandaic', 'notosansosage', 'notosanscoptic', 'notosansbalinese',  'notosanssymbols', 'notoserifcjktc', 'notocoloremoji', 'notoserifcjksc', 'notosansolditalic', 'notosansthaiui', 'notosansarabic', 'notosansgeorgian', 'notosansmalayalam', 'notosanssymbols2', 'notoserifgujarati', 'notosansmongolian', 'notosanshebrew', 'notosansoldpersian', 'notosansvai', 'notosanssylotinagri', 'notosansjavanese', 'notosanschakma', 'notosansugaritic', 'notoseriftamil', 'notosanssyriacwestern', 'notosanstaitham', 'notosansbrahmi', 'notosansoldturkic', 'notosanscuneiform', 'notosansshavian'
# All non-noto fonts: 'lohitodia', 'dejavusansmono', 'dejavuserif', 'tinos', 'arimo', 'googlesans', 'dejavusans', 'caladea', 'wingdings2', 'roboto', 'wingdings3', 'arialnarrow', 'webdings', 'jomolhari', 'nanumgothic', 'georgia', 'carlito', 'cousine', 'verdana', 'tahoma', 'bizudpgothic', 'comicsansms', 'garamond', 'wingdings', 'lohitpunjabi', 'arialblack', 'bizudpmincho', 'ipaexmincho'
def writeText(font: str, size: int, text: str, color: tuple,  textPosition: tuple, background: tuple = None):
  font = pygame.font.SysFont(font, size)
  text = font.render(text, True, color, background)

  textRect = text.get_rect()
  textRect.center = textPosition

  globalVariables["screen"].blit(text, textRect)

  return text, textRect

def shutdownGame():
  if globalVariables["party"] != None:
    sendAMessage({"action":"leaveParty", "contents":{"username":globalVariables["username"], "party":globalVariables["party"]}})

  globalVariables["status"] = "Offline"
  sendAMessage({"action": "leaveServer"})
  shutdownGameClient()
  pygame.quit()
  updateGameProgress()
  sys.exit()

def leaveLobby(jumper):
  globalVariables["veiwingHomeScreen"] = True
  globalVariables["playingGame"] = False
  jumper.resetJumper()
  sendAMessage({"action":"leaveGame", "contents":{"username":globalVariables["username"], "lobby":globalVariables["lobby"]}})
  globalVariables["lobby"] = None
  globalVariables["status"] = "Not in game"