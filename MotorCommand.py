# -*- coding: utf-8 -*-

import struct

class MotorCommand(object):

    _struct = struct.Struct('<Bh')

    def __init__(self):
        self.id = 0 #unsigned char
        self.cmd = 0 #unsigned char

    def serialize(self, buff):
        #try
        buff.write(MotorCommand._struct.pack(self.id, self.cmd))
        #except struct.error as se:
        #    raise SerializationError('Error in serialization %s' % (self.__str__))

    def fromTuple(self, data):
        self.id = data.id
        self.cmd = data.cmd

def to_hex(data):
    return ":".join("{:02x}".format(c) for c in data)