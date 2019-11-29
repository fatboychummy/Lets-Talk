import socket
import protocols
# example from https://pythontic.com/modules/socket/udp-client-server-example
def server (localIP, localPort, bufferSize):
    localIP     = "127.0.0.1"
    localPort   = 20001
    bufferSize  = 1024
    msgFromServer       = "Hello UDP Client"
    bytesToSend         = str.encode(msgFromServer)
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    # Listen for incoming datagrams
    while(True):
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        except Exception as e:
            print("an exception has occured {}".format(e))

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)

server('127.0.0.1', 20001, 1024)
