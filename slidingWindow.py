import sys
import socket
import time
import pickle

class Window:
    def __init__(self, id, content):
        self.id = id
        self.content = content
    def __str__(self):
        return "ID=" + str(self.id) + "\ncontent=" + content

def slidingWindow(send, windowSize, maxFrames):
    windows = window(send, windowSize)
    lastACK = -1
    current = 0
    # set a = start time
    # define two threads
    # V thread 1
    while current < len(windows) and current != lastACK:
        startTime = time.time()
        cAck = lastACK
        while current < lastACK + maxFrames:
            currentWindow = windows[current]
            w = Window(current, currentWindow)
            w = pickle.dumps(w)
            print(w)
            mySocket.send(w)
            current = current + 1
        while time.time() < startTime + x and cAck == lastACK:
            time.sleep(0.001)

    # listen for acks
        # set lastACK to the ack recieved
        # if the ack recieved is greater than 1 above the lastACK
            # set current back to lastACK



def window(send, k):
    n = len(send) # get size of object to be sent
    arr = []
    for i in range(0, n - k + 1, k):
        w = "" # initialize window
        for j in range(k):
            w = w + send[i + j]
            # add to the window
        arr.append(w)
    return arr

mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

send = "hi yes i want to be sent"

slidingWindow(send, 4, 4)
