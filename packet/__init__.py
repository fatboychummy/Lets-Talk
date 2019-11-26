import struct

# convert a list of numbers into bytes
def combinate(*argv):
    a = ''
    for arg in argv:
        a = a + struct.pack("B", arg)
    return a

def kBit(n, k):
    if n & (1 << (k - 1)):
        return True
    return False

class packet:
    ACK = 8
    RST = 4
    SYN = 2
    FIN = 1

    # self: dont worry about it its just us
    # sn: sequence number
    # an: acknowledgement number
    # arsf: packet.ACK, packet.RST, packet.SYN, or packet.FIN
    # data: the data
    def __init__(self, sn, an, arsf, data):
        self.SequenceNumber = sn
        self.AcknowledgeNumber = an
        self.Type = arsf
        self.Data = data

    # convert to string
    def __str__(self):
        b = "Sequence Number: " + str(self.SequenceNumber) + "\nACK Number: " + str(self.AcknowledgeNumber) + "\nFlag:"
        if kBit(self.Type, 3):
            b = b + " RST"
        if kBit(self.Type, 2):
            b = b + " SYN"
        if kBit(self.Type, 4): # syn before ACK
            b = b + " ACK"
        if kBit(self.Type, 1):
            b = b + " FIN"

        b = b + "\nData: " + str(self.Data)
        return b

    # convert to whatever the fuck this converts to
    def __repr__(self):
        return repr(self.dump())

    def __getitem__(self, i):
        return self.dump()[i]

    def __len__(self):
        return len(self.dump())

    # dump to bits
    def dump(self):
        # convert to binary format
        dat = []
        for char in self.Data:
            dat.append(ord(char))
        w = combinate(self.SequenceNumber, self.AcknowledgeNumber, self.Type, *dat)
        return w
