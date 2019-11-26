import sys
import socket
import time
import struct

from packet import packet

class protocols:
    def __init__(self, transmitSource):
        self.transmit = transmitSource

    def connect(self, IP, PORT):
        # three-way handshake
        print("Not Implemented")

    def waitForConnection(self):
        print("Not Implemented")

    # --------------------------------------------------------------------------

    def slidingWindow(send, windowSize, maxFrames):
        temp = cutData(send, windowSize)   # cut the data
        windows = toFrames(packet.SYN, *temp) # convert into frames
        lastACK = -1   # last acked frame, set to -1 since frame 0 is not acked
        current = 0    # current frame sending
        # define two threads to run simultaneusly

        # Thread 1
        def thread_1():
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

    # ----
    # data: data to be cut into smaller size and inserted into a list
    # size: the size between each cut
    # ----
    @staticmethod
    def cutData(data, size):
        n = len(data)
        lst = []
        for i in range(0, n - 1, size):
            w = ""
            for j in range(size):
                if i + j < len(data):
                    w = w + data[i + j]
                else:
                    w = w + '\0'
            lst.append(w)
        return lst

    # ----
    # arsf: packet.ACK, packet.RST, packet.SYN, or packet.FIN
    # argv: unpacked list of data frames (strings or something) to be converted
    # into binary frames
    #
    # returns: a list of packets that can be sent via socket.sendTo(pack)
    # ----
    @staticmethod
    def toFrames(arsf, *argv):
        packets = []
        j = 0
        for arg in argv:
            packets.append(packet(j, 0, arsf, arg))
            j = j + 1
        return packets

    # returns: an ACK packet with ack number j
    @staticmethod
    def ACK(j):
        return packet(0, j, packet.ACK, "")
