import sys
import socket
import time
import pickle

sys.exit(100000000000)

class protocols:
    def connect(transmit, IP, PORT):
        # three-way handshake
        print("no")

    # --------------------------------------------------------------------------

    def slidingWindow(transmit, send, windowSize, maxFrames):
        windows = toWindows(send, windowSize)   # cut the data into frames
        lastACK = -1    # last acked frame, set to -1 since frame 0 is not acked
        current = 0     # current frame sending
        # define two threads to run simultaneusly

        # Thread 1
        while current < len(windows) and current != lastACK:
            # while we still have frames to send
            # and until the final ack is recieved
            startTime = time.time() # get the time at which we started sending
            cAck = lastACK          # set a temporary ack check var

            while current < lastACK + maxFrames:
                # send the next maxFrames frames
                currentWindow = windows[current]
                transmit.send(currentWindow)
                current = current + 1

            while time.time() < startTime + x and cAck == lastACK:
                # wait x seconds (timeout) or wait until lastACK is updated
                time.sleep(0.001)

        # Thread 2
        # listen for acks
            # if the ack recieved is greater than 1 above the lastACK
                # set current back to lastACK
            # else set lastACK to the ack recieved

    # --------------------------------------------------------------------------

    def toWindows(send, k):
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

slidingWindow(mySocket, send, 4, 4)
