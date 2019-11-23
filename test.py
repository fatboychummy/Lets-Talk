import protocols
from packet import packet

prot = protocols.protocols("change this later")


pack = packet(1, 0, packet.ACK, "test")
print(pack)
print(repr(pack))
