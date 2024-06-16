import socketio

def createClient() -> socketio.Client:
  return socketio.Client(reconnection_attempts=5, reconnection_delay=1)

def sendMessage(client: socketio.Client, message: str):
  client.send(message)

def shutDownClient(client: socketio.Client):
  print("Shutting down client...")
  client.disconnect()
  print("Client shut down.")