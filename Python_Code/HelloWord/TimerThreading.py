import time
from threading import Timer

count = 1

def printHello():
    global count
    print(time.time(),'show:',count)
    count += 1
    Timer(1, printHello).start()


printHello()
