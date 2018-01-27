#! /usr/bin/env python

import smartcard
from smartcard.System import readers
from smartcard.reader.ReaderGroups import readergroups
from _ctypes import sizeof

def printAsHex(data):
    l=len(data)
    hexList=[]
    n=0
    while n<len(data):
       hexList.append(hex(data[n]))
       n+=1
    return(hexList)

# define the APDUs used in this script
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0xA0, 0x00, 0x00, 0x00, 0x62,
    0x03, 0x01, 0x0C, 0x06, 0x01]
READBINARY = [0x00, 0x0B, 0x00, 0x00]
COMMAND = [0x00, 0x00, 0x00, 0x00,0xA0]

# get all the available readers
r = readers()
print "Available readers:", r

if len(r) < 1:
        raise Exception('No smart card reader found')
reader = r[0]
print "Using:", reader

connection = reader.createConnection()
connection.connect()

data, sw1, sw2 = connection.transmit(SELECT)
print data
print "Select Applet statuswords: %02X %02X" % (sw1, sw2)

data, sw1, sw2 = connection.transmit(READBINARY)
print data
print "READ: %02X %02X" % (sw1, sw2)
