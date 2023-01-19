# -*- coding: utf-8 -*-

import struct

class MotorCommand(object):

    _struct = struct.Struct('<BH')

    def __init__(self):
        self.cmd = 0 #unsigned char - 1 byte
        self.data = 0 #unsigned short - 2 byte

    def serialize(self, buff):
        #try
        buff.write(MotorCommand._struct.pack(self.cmd, self.data))
        #except struct.error as se:
        #    raise SerializationError('Error in serialization %s' % (self.__str__))

    def fromTuple(self, data):
        self.cmd = data.cmd
        self.data = data.data

def to_hex(data):
    return ":".join("{:02x}".format(c) for c in data)