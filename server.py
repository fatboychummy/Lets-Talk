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
print("UDP server up and listening")
# Listen for incoming datagrams
while(True):
    try:
        bytesAddressPair = a.slidingListen()
    except OSError as err:
        print("Cannot receive from socket: {}".format(err.strerror))
        sys.exit(1)

    message = bytesAddressPair
    clientMsg = "Message from Client:{}".format(message.decode("utf-8"))
    print(clientMsg)



thread1:
    while true: # recieving from computer 1 (which sends to port 2)
        data = recieve(port2)
        sendto(computer2, data))

thread2:
    while true: # recieving from computer 2 (which sends to port 1)
        data = recieve(port1)
        sendto(computer1, data))
