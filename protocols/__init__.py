import sys
import socket
import time
import struct
import threading
import select


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

            # potentially remove
            #------------------------
            #self.sock.setblocking(0)
            #self.sock2.setblocking(0)
            #------------------------
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

    def connect(self):
        # three-way handshake
        #might need to use threads, will need to wait and have a time out
        #send SYN
        self.sock2.settimeout(2)
        fails = 0
        while True:
            self.sock.sendto(packet(0, 0, packet.SYN, "").dump(), (self.UDP_IP, self.UDP_PORT_1))
            # receive SYN ACK
            try:
                bAPair = self.sock2.recvfrom(self.bufferSize)
                binFlag = bytearray(bAPair[0][:3])
                tp = binFlag[2]
                if tp == packet.SYN + packet.ACK:
                    break
            except:
                fails = fails + 1
                if fails > 4:
                    raise Exception("Failed to send 5 times.")
                print("Failed to send, retrying in 1 second.")
                time.sleep(1)
        self.sock2.settimeout(None)

        #break this down somehow and check it

        # send ACK
        self.sock.sendto(packet(1, 5, packet.ACK, "").dump(), (self.UDP_IP, self.UDP_PORT_1))
        time.sleep(2) # allow time in case packet timed out

    def waitForConnection(self):
        # might need to use threads, will need to wait and have a time out
        # receive SYN
        syny = False
        self.sock2.settimeout(10)
        raddr = 1
        rport = 1
        while not syny:
            bAPair = 1
            try:
                bAPair = self.sock2.recvfrom(self.bufferSize)
                binFlag = bytearray(bAPair[0][:3])
                tp = binFlag[2]
                if tp == packet.SYN:
                    raddr = bAPair[1][0]
                    rport = bAPair[1][1]
                    pc = packet(1, 0, packet.SYN + packet.ACK, "")
                    self.sock.sendto(pc.dump(), (str(raddr), int(rport) + 1))
                    break
            except:
                raise Exception("No connection after 10 seconds. Stop.")
        self.sock2.settimeout(1.5)
        try:
            self.sock2.recvfrom(self.bufferSize)
        except:
            None
        self.sock2.settimeout(None)
        return (str(raddr), int(rport) + 1)

    # --------------------------------------------------------------------------

    def slidingWindow(self, send, windowSize, maxFrames):
        temp = protocols.cutData(send, windowSize)   # cut the data
        windows = protocols.toWindowFrames(*temp) # convert into frames
        self.lastACK = -1   # last acked frame, set to -1 since frame 0 is not acked
        self.current = 0    # current frame sending
        self.send = 0
        self.cuts = 0
        # define two_threads to run simultaneusly

        haltEvent = threading.Event()

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
                while self.send < self.lastACK + maxFrames:
                    if self.current > len(windows):
                        break
                    # send the next maxFrames frames

                    currentWindow = windows[self.current]
                    print(self.current, self.send, self.lastACK, currentWindow)

                    if self.send > 255:
                        self.send = 0
                        self.lastACK = -1
                        self.cuts += 1
                        currentWindow.Type += packet.RST

                    self.sock.sendto(currentWindow.dump(), (self.UDP_IP, self.UDP_PORT_1))
                    self.current += 1
                    self.send += 1
                while time.time() < startTime + 0.3 and cAck == self.lastACK and not self.current >= len(windows):
                    # wait x seconds (timeout) or wait until lastACK is updated
                    time.sleep(0.001)

                # if timeout
                if time.time() > startTime + 0.3:
                    print("##Timeout##")
                    print(self.current, self.send, self.lastACK)
                    self.current = self.lastACK + (255 * self.cuts) + 1
                    self.send = self.lastACK + 1
                    print(self.current, self.send, self.lastACK)
                    print("###########")

                # if lastACK updated
                if cAck != self.lastACK:
                    fails = 0
                else:
                    fails += 1

                # if we are done
                if self.current >= len(windows):
                    break
            haltEvent.set()

        def thread_2(self, halt):
            while not halt.is_set():
                try:
                    bAPair = self.sock2.recvfrom(self.bufferSize) # recieve from client
                    binFlag = bytearray(bAPair[0][:3])  # binary flags sent in packet
                    ackn = binFlag[1]
                    self.lastACK = ackn
                except:
                    print("Failed to recieve oh nooooo")
                    sys.exit(1)

        t1 = threading.Thread(name="Sender", target=thread_1, args=(self, windows))
        t2 = threading.Thread(name="Reciever", target=thread_2, args=(self, haltEvent))
        t2.start() # start the listener first in case
        # starting it takes longer than it does to send/recieve
        t1.start()
        haltEvent.wait() # wait until halt event recieved

    def slidingListen(self):
        # run until FIN flag recieved
        # if recieved > 1 above lastRec then ack lastRec
        lastRec = 0
        data = bytearray()
        while 1:
            bAPair = self.sock2.recvfrom(self.bufferSize) # recieve from client
            binFlag = bytearray(bAPair[0][:3])  # binary flags sent in packet
            tp = binFlag[2]

            raddr = bAPair[1][0]                # address to respond to
            rport = bAPair[1][1]                # port to respond to
            breakflag = False

            if tp - packet.ACK >= 0:
                # ack
                tp -= packet.ACK
                # nothing pmuch

            if tp - packet.RST >= 0:
                # reset
                tp -= packet.RST
                # reset acker
                lastRec = 0

            if tp - packet.SYN >= 0:
                # sync
                tp -= packet.SYN

            if tp - packet.FIN >= 0:
                # finalize
                tp -= packet.FIN
                breakflag = True # if finalize, stop

            if binFlag[0] > lastRec + 1:
                binFlag[0] = lastRec
                # if SYN number is too high (ie: packet lost)
                # ack the last recieved packet
            else:# binFlag[0] == lastRec + 1:
                # otherwise ack this packet
                lastRec = binFlag[0]
                data += bAPair[0][3:] # data from client

            # send ACK
            a = packet(0, binFlag[0], packet.ACK, "ack")
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
        lst = [data[i:i+size] for i in range(0, n, size)]
        #for i in range(0, n - 1, size):
        #    w = ""
        #    for j in range(size):
        #        if i + j < len(data):
        #            w = w + data[i + j]
        #        else:
        #            w = w + '\0'
        #    lst.append(w)
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
    def toWindowFrames(*argv):
        packets = []
        j = 0
        for i in range(len(argv)):
            arg = argv[i]

            tp = packet.SYN

            if i == len(argv) - 1:
                tp = packet.FIN

            if j > 255:
                j = 0
                tp += packet.RST

            packets.append(packet(j, 0, tp, arg))
            j = j + 1
        return packets

    # returns: an ACK packet with ack number j
    @staticmethod
    def ACK(j):
        return packet(0, j, packet.ACK, "")
