import socket,sys

from protocols import protocols
from packet import packet

#placeholder  from https://pythontic.com/modules/socket/udp-client-server-example

localPort = 55000
destIP = "142.66.140.186"

if len(sys.argv) != 2:
    print("Usage: {} destination_IP_addr".format(sys.argv[0]))
    sys.exit(1)

a = protocols(sys.argv[1], localPort, localPort + 1, 1024)
a.connect()

a.slidingWindow("This is a string of stuff that needs to be sent", 4, 4)
print("Successfully sent data.")
sys.exit(1)
