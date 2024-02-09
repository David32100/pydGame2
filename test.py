# import threading
# import time
# import random
# import queue

# number = 5
# lock = threading.Lock()

# def function1():
#   print("Hi")
#   time.sleep(6)
#   print("Ok, bye")

# def function2():
#   time.sleep(3)
#   print("Bye")

# def function3():
#   print("F3 called")

#   with lock:
#     print("Starting")
#     global number
#     localNumber = number
#     time.sleep(3)
#     localNumber += 24
#     time.sleep(3)
#     number = localNumber
#     print(number)

# def function4():
#   print("F4 called")

#   with lock:
#     print("Starting")
#     global number
#     localNumber = number
#     time.sleep(2)
#     localNumber -= 5
#     localNumber /= 5
#     time.sleep(2)
#     number = localNumber
#     print(number)

# t1 = threading.Thread(target=function1)
# t2 = threading.Thread(target=function2)
# t3 = threading.Thread(target=function3)
# t4 = threading.Thread(target=function4)

# t1.start()
# t2.start()
# t3.start()
# t4.start()

# t4.join()

# def producer(queue, event):
#   while not event.is_set():
#     message = random.randint(1, 101)
#     print("Made message", queue.qsize())
#     queue.put(message)
#     print("Set message", queue.qsize())

# def consumer(queue, event):
#   while not event.is_set() or not queue.empty():
#     print("Getting message", queue.qsize())
#     message = queue.get()
#     print("Got message", queue.qsize())

# pipeline = queue.Queue(maxsize=5)
# event = threading.Event()

# threading.Thread(target=producer, args=(pipeline, event)).start()
# threading.Thread(target=consumer, args=(pipeline, event)).start()
# time.sleep(0.001)
# event.set()
# dataToSend = str([0, 300, 400]).encode("utf-8")

# dataRecieved = dataToSend.decode("utf-8")[1:-1].split(", ")
# dataPeices = []

# for i in range(len(dataRecieved)):
#   dataPeices.append(int(dataRecieved[i]))

# numricalDataRecieved = dataPeices

# print("numricalDataRecieved:", type(numricalDataRecieved), numricalDataRecieved)
list1 = ["1", "Hi"]

for part in list1:
  if part.isdigit():
    print("Yay", part)
  else:
    print("No", part)