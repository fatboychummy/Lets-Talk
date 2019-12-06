import socket,sys
from protocols import protocols
import threading
import random
import time

errorChance = 5

class Proxy:
    """ Used to proxy single udp connection"""

    def __init__(self, UDP_IP1, UDP_IP2, UDP_PORT_1, UDP_PORT_2, BUFFER_SIZE):
        print ("Proxy starting")
        self.UDP_IP1 = UDP_IP1
        self.UDP_IP2 = UDP_IP2
        self.UDP_PORT_1 = UDP_PORT_1
        self.UDP_PORT_2 = UDP_PORT_2
        self.BUFFER_SIZE = BUFFER_SIZE
        self.dropCount = 0
        self.delayCount = 0

        def proxy_server(self):
            # listen for incoming connections on port 1:
            try:
                self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("cannot open socket")
                sys.exit(1)

            try:
                self.sock1.bind(('', UDP_PORT_1))
            except:
                print ("couldn't bind socket 1 to port 1" )
                sys.exit(1)
            #thread_1 send to client
            while True:
                data = self.sock1.recvfrom(self.BUFFER_SIZE)
                print("Recieved from server " + str(data))
                ran = random.randint(0, errorChance)
                if ran == 0:
                    # delay random time 0.2 -> 1.5 seconds
                    def func(self, rn, data):
                        time.sleep(rn)
                        self.sock1.sendto(data, (self.UDP_IP1, self.UDP_PORT_1))
                    tm = random.randint(0, 15)  /10
                    tt = threading.Thread(name="why", target=func, args=(self, tm, data[0]))
                    print("Delaying above packet by " + str(tm) + " seconds.")
                    tt.start()
                    delayCount += 1
                elif ran == 1:
                    # drop packet so do nothing
                    print("Dropping above packet.")
                    dropCount += 1
                else:
                    print("Doing normal stuff with above packet")
                    self.sock1.sendto(data[0], (self.UDP_IP1, self.UDP_PORT_1))


        def proxy_client(self):
            #listen for incoming connectons on port 2
            try:
                self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("cannot open socket")
                sys.exit(1)

            try:
                self.sock2.bind(('', UDP_PORT_2))
            except:
                print("couldn't bind socket 2 to port 2")
                sys.exit(1)

            #thread 2 send to server
            while True:
                data = self.sock2.recvfrom(self.BUFFER_SIZE)
                print("Recieved from client " + str(data))
                ran = random.randint(0, errorChance)
                if ran == 0:
                    # delay random time 0.2 -> 1.5 seconds
                    def func(self, rn, data):
                        time.sleep(rn)
                        self.sock2.sendto(data, (self.UDP_IP2, self.UDP_PORT_2))
                    tm = random.randint(0, 15)  /10
                    tt = threading.Thread(name="why", target=func, args=(self, tm, data[0]))
                    print("Delaying above packet by " + str(tm) + " seconds.")
                    tt.start()
                    delayCount += 1
                elif ran == 1:
                    # drop packet so do nothing
                    print("Dropping above packet.")
                    dropCount += 1
                else:
                    print("Doing normal stuff with above packet")
                    self.sock2.sendto(data[0], (self.UDP_IP2, self.UDP_PORT_2))

        t1 = threading.Thread(name="Server", target=proxy_server, args=(self,))
        t2 = threading.Thread(name="Client", target=proxy_client, args=(self,))
        t1.start()
        t2.start()

        print("Proxy started")

        t1.join()
        t2.join()
        print("Dropped", self.dropCount, "packets.")
        print("Delayed", self.delayCount, "packets.")

#def __init__(self, UDP_IP1, UDP_IP2, UDP_PORT_1, UDP_PORT_2, BUFFER_SIZE)
if len(sys.argv) < 3:
    print("Usage: <IP_CLIENT> <IP_SERVER>")
    sys.exit(1)

localPort = 55000

a = Proxy(sys.argv[1], sys.argv[2], localPort + 1, localPort, 1024)
