from account.login import login
from account.signUp import signUp
from globalVariables import globalVariables
from client.communications import sendAMessage

def loginToAccount():
  while globalVariables["loggingIn"]:
    login()

    if globalVariables["loggingIn"]:
      signUp()
    
    if not globalVariables["loggingIn"]:
      sendAMessage({"action":"joinServer"})