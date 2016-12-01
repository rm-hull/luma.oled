
class mode(object):
    command = 0x00
    data = 0x00


class recording(object):

    def __init__(self, addr, mode, data):
        self.addr = addr
        self.mode = mode
        self.data = data

    def __eq__(self, other):
        return self.addr == other.addr and \
            self.mode == other.mode and \
            self.data == other.data

    def __repr__(self):
        return "recording({0}, {1}, {2})".format(self.addr, self.mode, self.data)


class smbus(object):

    def __init__(self, port):
        self.port = port
        self.recordings = []

    def write_i2c_block_data(self, addr, mode, vals):
        self.recordings.append(recording(addr, mode, vals))

    def close(self):
        pass

    def reset(self):
        self.recordings = []
