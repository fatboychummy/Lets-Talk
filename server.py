import socket,sys,errno
import protocols
# example from https://pythontic.com/modules/socket/udp-client-server-example

localPort   = 55000
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
# Create a datagram socket
try:
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("Cannot open socket")
    sys.exit(1)
# Bind to address and ip
try:
    UDPServerSocket.bind(('', localPort))
except:
    print("Cannot bind socket to port")
    sys.exit(1)

print("UDP server up and listening")
# Listen for incoming datagrams
while(True):
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except OSError as err:
        print("Cannot receive from socket: {}".format(err.strerror))
        sys.exit(1)

    message = bytesAddressPair
    clientMsg = "Message from Client:{}".format(message)
    print(clientMsg)
