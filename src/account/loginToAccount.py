from account.login import login
from account.signUp import signUp
from globalVariables import globalVariables
from client.communications import sendAMessage, condition

def loginToAccount():
  global error

  while globalVariables["loggingIn"]:
    login()

    if globalVariables["loggingIn"]:
      signUp()
    
    if not globalVariables["loggingIn"]:
      sendAMessage({"action":"joinServer", "contents":{"username":globalVariables["username"]}})
      condition.acquire()
      
      l = 0

      while l < 4:
        if not condition.wait(1):
          sendAMessage({"action":"joinServer", "contents":{"username":globalVariables["username"]}})
          l += 1
        else:
          break
      
      if l == 4:
        globalVariables["loggingIn"] = True
        globalVariables["connectedToServer"] = False
      
      condition.release()
