import struct
import sys

from protocols import protocols
from packet import packet

fname = sys.argv[0]
if len(sys.argv) != 2:
    print("Usage: " + fname + " <ip address>")
    sys.exit(1)
ip = sys.argv[1]

prot = protocols(ip, 6969)

prot.slidingWindow("We need more memes, memes are life, send help in the form of memes please.", 8, 4)

while 1:
    pass
