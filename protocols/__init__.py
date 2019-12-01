import sys
import socket
import time
import struct
import _thread
from threading import Event


from packet import packet

class protocols:
    # set udp_ip to an empty string if reciever
    def __init__(self, UDP_IP, UDP_PORT, BUFFER_SIZE):
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT
        self.bufferSize = BUFFER_SIZE
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print("Cannot open socket.")
            sys.exit(1)

        try:
            self.sock.bind(('', UDP_PORT))
        except:
            print("Cannot bind socket.")
            sys.exit(1)

    def connect(self, IP, PORT):
        # three-way handshake
        print("Not Implemented")
        # send SYN
        # recieve SYN ACK
        # send ACK

    def waitForConnection(self):
        print("Not Implemented")
        # recieve SYN
        # send SYN ACK
        # recieve ACK

    # --------------------------------------------------------------------------

    def slidingWindow(self, send, windowSize, maxFrames):
        temp = protocols.cutData(send, windowSize)   # cut the data
        windows = protocols.toWindowFrames(packet.SYN, *temp) # convert into frames
        self.lastACK = -1   # last acked frame, set to -1 since frame 0 is not acked
        self.current = 0    # current frame sending
        # define two_threads to run simultaneusly

        haltEvent = Event()

        #_thread 1
        def thread_1(self, windows):
            while self.current < len(windows) or self.current != self.lastACK:
                # while we still have frames to send
                # and until the final ack is recieved
                startTime = time.time() # get the time at which we started sending
                cAck = self.lastACK          # set a temporary ack check var
                while self.current < self.lastACK + maxFrames:
                    print("C" + str(self.current))
                    print("L" + str(self.lastACK))
                    print("M" + str(maxFrames))
                    # send the next maxFrames frames
                    currentWindow = windows[self.current]
                    print("Send " + repr(currentWindow))
                    self.sock.sendto(currentWindow.dump(), (self.UDP_IP, self.UDP_PORT))
                    self.current = self.current + 1
                while time.time() < startTime + 0.5 and cAck == self.lastACK:
                    # wait x seconds (timeout) or wait until lastACK is updated
                    time.sleep(0.001)
                if time.time() > startTime + 0.5:
                    self.current = self.lastACK + 1

            print("Done at")
            print(self.current)
            print(self.lastACK)
            print(maxFrames)
            haltEvent.set()
            print("THREAD 1 DONE")

        def thread_2(self, halt):
            while not halt.is_set():
                try:
                    bAPair = self.sock.recvfrom(self.bufferSize) # recieve from client
                    binFlag = bytearray(bAPair[0][:3])  # binary flags sent in packet
                    ackn = binFlag[1]
                    self.current = ackn
                except:
                    print("cannot receive")
                    sys.exit(1)
                print("recv " + data)
            print("THREAD 2 DONE")
            #_thread 2
            # listen for acks
            # if the ack recieved is greater than 1 above the lastACK
            # set current back to lastACK
            # else set lastACK to the ack recieved

        _thread.start_new_thread(thread_1, (self, windows))
        _thread.start_new_thread(thread_2, (self, haltEvent))
        while not haltEvent.is_set():
            print("CHECKY " + str(self.current))
            time.sleep(0.1)


    def slidingListen(self):
        # run until FIN flag recieved
        # if recieved > 1 above lastRec then ack lastRec
        lastRec = 0
        data = bytearray()
        while 1:
            bAPair = self.sock.recvfrom(self.bufferSize) # recieve from client
            binFlag = bytearray(bAPair[0][:3])  # binary flags sent in packet
            raddr = bAPair[1][0]                # address to respond to
            rport = bAPair[1][1]                # port to respond to
            breakflag = False
            if binFlag[2] == packet.FIN:
                breakflag = True   # if FINALIZE, stop

            if binFlag[0] > lastRec + 1:
                binFlag[0] = lastRec
                # if SYN number is too high (ie: packet lost)
                # ack the last recieved packet
            else:
                # otherwise ack this packet
                lastRec = binFlag[0]
                data += bAPair[0][3:]               # data from client

            # send ACK
            self.sock.sendto(str(packet(0, binFlag[0], packet.ACK, "ack")).encode(), (raddr, rport))
            if breakflag:
                break
        return protocols.scrub(data)
    # --------------------------------------------------------------------------


    # ----
    # scrubs empty characters from a bytearray
    # dat: the data to be scrubbed
    # ----
    @staticmethod
    def scrub(dat):
        dat2 = dat.split(b'\x00')
        return dat2[0]

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
