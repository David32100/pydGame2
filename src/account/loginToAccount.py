from account.login import login
from account.signUp import signUp
from globalVariables import globalVariables

def loginToAccount():
  global error

  while globalVariables["loggingIn"]:
    login()

    if globalVariables["loggingIn"]:
      signUp()