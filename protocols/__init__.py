import sys
import socket
import time
import struct
import _thread
from threading import Event


from packet import packet

class protocols:
    def __init__(self, UDP_IP, UDP_PORT):
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT

    def connect(self, IP, PORT):
        # three-way handshake
        print("Not Implemented")

    def waitForConnection(self):
        print("Not Implemented")

    # --------------------------------------------------------------------------

    def slidingWindow(self, send, windowSize, maxFrames):
        temp = protocols.cutData(send, windowSize)   # cut the data
        windows = protocols.toWindowFrames(packet.SYN, *temp) # convert into frames
        lastACK = -1   # last acked frame, set to -1 since frame 0 is not acked
        current = 0    # current frame sending
        # define two threads to run simultaneusly

        haltEvent = Event()

        # Thread 1
        def thread_1(self, current, windows, lastACK):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while current < len(windows) and current != lastACK:
                # while we still have frames to send
                # and until the final ack is recieved
                startTime = time.time() # get the time at which we started sending
                cAck = lastACK          # set a temporary ack check var
                while current < lastACK + maxFrames:
                    # send the next maxFrames frames
                    currentWindow = windows[current]
                    sock.sendto(currentWindow.dump(), (self.UDP_IP, self.UDP_PORT))
                    current = current + 1
                while time.time() < startTime + 0.5 and cAck == lastACK:
                    # wait x seconds (timeout) or wait until lastACK is updated
                    time.sleep(0.001)
                if time.time() > startTime + 0.5:
                    current = lastACK + 1
            haltEvent.set()

        def thread_2(self, halt):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("Cannot open socket")
                sys.exit(1)

            try:
                sock.bind((UDP_IP, UDP_PORT))
            except:
                print("cannot bind")
                sys.exit(1)

            while not halt.is_set():
                try:
                    data, addr = sock.recvfrom(1024) # buffer size can change
                except:
                    print("cannot receive")
                    sys.exit(1)
                print(data)
            # Thread 2
            # listen for acks
            # if the ack recieved is greater than 1 above the lastACK
            # set current back to lastACK
            # else set lastACK to the ack recieved

        thread.start_new_thread(thread_1, (self, current, windows, lastACK))
        thread.start_new_thread(thread_2, (self, haltEvent))


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
    # NOTE: LAST FRAME WILL ALWAYS BE packet.FIN
    # arsf: packet.ACK, packet.RST, packet.SYN, or packet.FIN
    # argv: unpacked list of data frames (strings or something) to be converted
    # into binary frames
    #
    # returns: a list of packets that can be sent via socket.sendTo(pack)
    # ----
    @staticmethod
    def toWindowFrames(arsf, *argv):
        packets = []
        j = 0
        for i in range(len(argv)):
            arg = argv[i]
            if i != len(argv) - 1:
                packets.append(packet(j, 0, arsf, arg))
            else:
                packets.append(packet(j, 0, packet.FIN, arg))
            j = j + 1
        return packets

    # returns: an ACK packet with ack number j
    @staticmethod
    def ACK(j):
        return packet(0, j, packet.ACK, "")
