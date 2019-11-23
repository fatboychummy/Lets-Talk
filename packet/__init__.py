import struct

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
        return "Sequence Number: " + str(self.SequenceNumber) + "\nACK Number: " + str(self.AcknowledgeNumber) + "\nFlag: " + str(self.Type) + "\nData: " + str(self.Data)

    # convert to whatever the fuck this converts to
    def __repr__(self):
        return self.dump()

    # dump to bits
    def dump(self):
        # convert to binary format
        print("Not implemented")
        return struct.pack("B", 5) + struct.pack("B", 5) + struct.pack("B", 5)

    # convert a list of numbers into bytes
    def combinate(*argv):
        a = ''
        for arg in argv:
            a = a + struct.pack("B", arg)
        return a
