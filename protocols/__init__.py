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
        self.ACKED = []
        for i in range(256): # set 0 <-> 255 to false
            self.ACKED.append(False)
        self.resetFlag = False
        self.current = 0    # current frame sending
        self.send = 0
        self.cuts = 0
        self.stopAll = False
        # define two_threads to run simultaneusly

        haltEvent = threading.Event()

        #_thread 1

        def send_packet(self, pack, timeout):
            print("#############START", threading.currentThread().getName())
            num = pack.SequenceNumber
            while not self.ACKED[num] and not (num == 255 and self.resetFlag) and not self.stopAll:
                print("Attempting to send a packet\n", pack)
                self.sock.sendto(pack.dump(), (self.UDP_IP, self.UDP_PORT_1))
                time.sleep(timeout)
            print("#############STOP", threading.currentThread().getName())

        # listener thread, adds ACKs to the self.ACKED
        # sets the resetFlag to true when reset needed
        def listen(self):
            while True:
                bAPair = self.sock2.recvfrom(self.bufferSize) # recieve from client
                binFlag = bytearray(bAPair[0][:3])  # binary flags sent in packet
                ackn = binFlag[1]
                a = binFlag[2]

                # determine if ACK, RST, SYN, or FIN (or any combination of them)
                if a >= packet.ACK:
                    # ack received
                    a -= packet.ACK
                if a >= packet.RST:
                    # reset received
                    a -= packet.RST
                    self.resetFlag = True
                    self.lastACK = -1
                if a >= packet.SYN:
                    # sync received
                    a -= packet.SYN
                if a >= packet.FIN:
                    # finalize received
                    a -= packet.FIN
                    print("Recieved finalization fix later")

                # if this is one of the next ACKs
                if ackn > self.lastACK:
                    # set this packet and all previous packets to true
                    print("===ACK", ackn)
                    for i in range(ackn, -1, -1):
                        self.ACKED[i] = True
                    self.lastACK = ackn

        # run the listener
        t1 = threading.Thread(target=listen, args=(self,))
        t1.start()
        # run the sender
        i = 0
        while i < len(windows):
            j = 0
            threads = []
            while j < 256:
                # start threads
                print(windows[i + j].SequenceNumber, i, j, i + j)
                temp = threading.Thread(name=str(j), target=send_packet, args=(self, windows[i + j], 0.1))
                temp.start()
                threads.append(temp)
                # ensure only maxFrames threads are running at once
                while len(threads) >= maxFrames:
                    print("Threads at max length")
                    threads = [t for t in threads if t.is_alive()]
                    time.sleep(0.1)

                # ensure that, if we are on the 255th window, that we wait until it completes.
                while len(threads) >= 1 and j == 255:
                    for t in threads:
                        if t.getName() == str(j) and not t.is_alive():
                            print("STOP ALL")
                            self.stopAll = True
                            time.sleep(2)
                            self.stopAll = False
                            for k in range(255):
                                self.ACKED[k] = False
                            threads = [t for t in threads if t.is_alive()]
                            break
                    time.sleep(0.1)
                j += 1

            i += 256

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

            tp2 = packet.ACK

            rstflag = False

            if tp - packet.ACK >= 0:
                # ack
                tp -= packet.ACK
                # nothing pmuch

            if tp - packet.RST >= 0:
                # reset
                tp -= packet.RST
                tp2 += packet.RST
                # reset acker
                lastRec = 0
                rstflag = True

            if tp - packet.SYN >= 0:
                # sync
                tp -= packet.SYN

            if binFlag[0] == lastRec + 1 or rstflag:
                # otherwise if the ack is the next-in-line, ack this packet
                lastRec = binFlag[0]
                data += bAPair[0][3:] # data from client
                if tp - packet.FIN >= 0:
                    # finalize
                    tp -= packet.FIN
                    breakflag = True # if finalize, stop

            elif binFlag[0] > lastRec + 1 or binFlag[0] < lastRec + 1:
                binFlag[0] = lastRec
                # if SYN number is too high or too low (ie: packet lost or delayed)
                # ack the last properly recieved packet

            # send ACK
            a = packet(0, binFlag[0], tp2, "ack")
            self.sock.sendto(a.dump(), (raddr, self.UDP_PORT_1))
            if rstFlag:
                lastRec = 0
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

            if j == 255:
                tp += packet.RST

            packets.append(packet(j, 0, tp, arg))
            j = j + 1
        return packets

    # returns: an ACK packet with ack number j
    @staticmethod
    def ACK(j):
        return packet(0, j, packet.ACK, "")
