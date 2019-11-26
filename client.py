import socket

#placeholder  from https://pythontic.com/modules/socket/udp-client-server-example
def client (msgFromClient, serverAddressPort, bufferSize):
    #msgFromClient       = "Hello UDP Server"
    #serverAddressPort   = ("127.0.0.1", 20001)
    #bufferSize          = 1024

    bytesToSend         = str.encode(msgFromClient)
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while True:
        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        print(msg)


client("ACK", ('', 69420), 1024)
