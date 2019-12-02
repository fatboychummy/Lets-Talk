import sys
import socket
import time
import struct
import _thread
from threading import Event


from packet import packet

class protocols:
    # set udp_ip to an empty string if reciever
    def __init__(self, UDP_IP, UDP_PORT_1, UDP_PORT_2, BUFFER_SIZE):
        self.UDP_IP = UDP_IP
        self.UDP_PORT_1 = UDP_PORT_1
        self.UDP_PORT_2 = UDP_PORT_2
        self.bufferSize = BUFFER_SIZE
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print("Cannot open sockets.")
            sys.exit(1)

        try:
            self.sock.bind(('', UDP_PORT_1))
        except:
            print("Cannot bind socket 1")
        try:
            self.sock2.bind(('', UDP_PORT_2))
        except:
            print("Cannot bind socket 2.")
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
            fails = 0
            while self.current < len(windows) or self.current != self.lastACK:
                if fails >= 9:
                    print("Failed to send (No update after 10 tries)")
                    break
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
                    self.sock.sendto(currentWindow.dump(), (self.UDP_IP, self.UDP_PORT_1))
                    self.current = self.current + 1
                while time.time() < startTime + 0.5 and cAck == self.lastACK:
                    # wait x seconds (timeout) or wait until lastACK is updated
                    time.sleep(0.001)
                # if timeout
                if time.time() > startTime + 0.5:
                    self.current = self.lastACK + 1
                # if lastACK updated
                if cAck != self.lastACK:
                    fails = 0
                else:
                    fails += 1

            haltEvent.set()

        def thread_2(self, halt):
            while not halt.is_set():
                print("In thread 2 loop")
                try:
                    print("a-----------------------")
                    bAPair = self.sock2.recvfrom(self.bufferSize) # recieve from client
                    print("b-----------------------")
                    binFlag = bytearray(bAPair[0][:3])  # binary flags sent in packet
                    ackn = binFlag[1]
                    self.current = ackn
                except:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    sys.exit(1)
                print("recv " + bAPair)
            print("THREAD 2 DONE")

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
            bAPair = self.sock2.recvfrom(self.bufferSize) # recieve from client
            print("Recieved")
            print(bAPair)
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
            a = packet(0, binFlag[0], packet.ACK, "ack")
            print("REPLY: ")
            print("TO: " + str(raddr) + " " + str(rport))
            print(a)
            self.sock.sendto(a.dump(), (raddr, self.UDP_PORT_1))
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
