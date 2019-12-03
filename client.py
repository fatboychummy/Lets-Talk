import socket,sys

from protocols import protocols
from packet import packet

#placeholder  from https://pythontic.com/modules/socket/udp-client-server-example

localPort = 55000
destIP = "142.66.140.186"

if len(sys.argv) != 2:
    print("Usage: PIPE_COMMAND | {} destination_IP_addr".format(sys.argv[0]))
    sys.exit(1)

send = ""
for line in sys.stdin:
    send += line

a = protocols(sys.argv[1], localPort, localPort + 1, 1024)
#a.connect()

a.slidingWindow(send, 64, 4)

print("Successfully sent data.")
sys.exit(1)
