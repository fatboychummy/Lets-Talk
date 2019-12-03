import socket,sys
import protocols
import threading

class Proxy:
    """ Used to proxy single udp connection"""
    BUFFER_SIZE = 1024

    def __init__(self, listening_addr, forward_addr):
        print ("Server started on", listening_addr)
        self.bind = listening_addr
        self.target = forward_addr

        def proxy_server(self):
            # listen for incoming connections:
            try:
                target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("cannot open socket")

            try:
                target.connect(self.target)
            except OSError as err:
                print("cannot connect to: {}".format(err.strerror))
                sys.exit(1)

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("cannot bind socket to port")
            try:
                s.bind(self.bind)

            except:
                print ("couldn't bind port" )
                raise SystemExit

            while 1:
                dgram = s.recv(self.BUFFER_SIZE)
                if not dgram:
                    break
                length = len(dgram)
                sent = target.send(dgram)
                if length != sent:
                    print ("cannot send data")
            s.close()
