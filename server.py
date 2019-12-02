import socket,sys,errno
from protocols import protocols
# example from https://pythontic.com/modules/socket/udp-client-server-example

localPort   = 55000
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
# Create a datagram socket
a = protocols("", localPort + 1, localPort, bufferSize)
#a.waitForConnection()
print("UDP server up and listening")
# Listen for incoming datagrams
while(True):
    try:
        bytesAddressPair = a.slidingListen()
    except OSError as err:
        print("Cannot receive from socket: {}".format(err.strerror))
        sys.exit(1)

    message = bytesAddressPair
    clientMsg = "Message from Client:{}".format(message)
    print(clientMsg)
