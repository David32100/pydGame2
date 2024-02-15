import json

from globalVariables import globalVariables, savedVariables

def readAndWriteFile(file: str, itemToWrite="", createFile=False):
  if createFile:
    with open(file, "w") as file:
      file.write(itemToWrite)

    return itemToWrite

  else:
    with open(file, "r+") as file:
      fileContents = file.read()
      
      if itemToWrite != "":
        file.seek(0)
        file.truncate(0)
        file.write(itemToWrite)

    return fileContents
  
def getSavedData(username:str):
  try:
    savedData = json.loads(readAndWriteFile("saveFiles/'" + username + "'GameProgress.JSON"))
  except FileNotFoundError:
    savedData = json.loads(readAndWriteFile("saveFiles/'" + username + "'GameProgress.JSON", itemToWrite=json.dumps(savedVariables), createFile=True))

  return savedData

def saveData(username: str):
  for key in list(savedVariables.keys()):
    savedVariables[key] = globalVariables[key]

  readAndWriteFile("saveFiles/'" + username + "'GameProgress.JSON", json.dumps(savedVariables))

def updateGlobalVariables():
  savedVariables = getSavedData(str(globalVariables["username"]))

  for key in savedVariables:
    globalVariables[key] = savedVariables[key]

def updateGameProgress():
  saveData(str(globalVariables["username"]))