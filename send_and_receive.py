import socket

def send(UDP_IP, UDP_PORT, MESSAGE):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Cannot open socket")
        sys.exit(1) 
    try:
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    except:
        print("cannot send")
        sys.exit(1)

def receive(UDP_IP, UDP_PORT, MESSAGE):
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
    try:
        data, addr = sock.recvfrom(1024) # buffer size can change
    except:
        print("cannot receive")
        sys.exit(1)
