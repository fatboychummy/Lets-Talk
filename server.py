import socket,sys,errno
from protocols import protocols
# example from https://pythontic.com/modules/socket/udp-client-server-example

localPort   = 55000
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
# Create a datagram socket
a = protocols("", localPort + 1, localPort, bufferSize)
b = a.waitForConnection()
# Listen for incoming datagrams

try:
    bytesAddressPair = a.slidingListen()
except OSError as err:
    print("Cannot receive from socket: {}".format(err.strerror))
    sys.exit(1)

message = bytesAddressPair
clientMsg = message.decode("utf-8")
print(clientMsg)
