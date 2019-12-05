import socket,sys
from protocols import protocols
import threading

class Proxy:
    """ Used to proxy single udp connection"""
    localPoirt = 55002

    def __init__(self, UDP_IP1, UDP_IP2, UDP_PORT_1, UDP_PORT_2, BUFFER_SIZE):
        print ("Server started on", listening_addr)
        self.UDP_IP1 = UDP_IP1
        self.UDP_IP2 = UDP_IP2
        self.UDP_PORT_1 = UDP_PORT_1
        self.UDP_PORT_2 = UDP_PORT_2
        self.BUFFER_SIZE = BUFFER_SIZE

        def proxy_server(self):
            # listen for incoming connections on port 1:
            try:
                sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("cannot open socket")
                sys.exit(1)

            try:
                self.sock1.bind('', UDP_PORT_1)
            except:
                print ("couldn't bind socket 1 to port 1 recieve" )
                sys.exit(1)
            #thread_1 send to client
            while True:
                data = self.sock1.recvfrom(self.BUFFER_SIZE)
                self.sock1.sendto(data[0], (self.UDP_IP2, self.UDP_PORT_2))


        def proxy_client(self):
            #listen for incoming connectons on port 2
            try:
                sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("cannot open socket")
                sys.exit(1)

            try:
                self.sock2.bind('', UDP_PORT_2)
            except:
                print("couldn't bind socket 2 to port 2")
                sys.exit(1)

            #thread 2 send to server
            while True:
                data = self.sock2.recvfrom(self.BUFFER_SIZE)
                sef.sock2.sendto(data[0], (self.UDP_IP1, self.UDP_PORT_1))

        t1 = threading.Thread(name="Server", target=proxy_server, args=(self))
        t2 = threading.Thread(name="Client", target=proxy_client, args=(self))
        t1.start()
        t2.start()

        t1.join()
        t2.join()
