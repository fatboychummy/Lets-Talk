import socket,sys

#placeholder  from https://pythontic.com/modules/socket/udp-client-server-example

localPort = 55000
destIP = "142.66.140.186"

if len(sys.argv) != 2:
    print("Usage: {} destination_IP_addr".format(sys.argv[0]))
    sys.exit(1)

try:
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("Cannot open socket")
    sys.exit(1)

try:
    UDPClientSocket.bind(('', 55000))
    UDPClientSocket.sendto(b'Hello World', (sys.argv[1], localPort))
except OSError as err:
    print('Cannot send: {}'.format(err.strerror))
    sys.exit(1)
