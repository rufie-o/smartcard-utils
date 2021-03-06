import smartcard
from smartcard.util import *
from compiler.pycodegen import EXCEPT

def printAsHex(data):
    l=len(data)
    hexList=[]
    n=0
    while n<len(data):
       hexList.append(hex(data[n]))
       n+=1
    return(hexList)

readers=smartcard.listReaders()
if len(readers)>0:
    print "Available readers: ", readers
    print("using reader ",readers[0])

try:
    session = smartcard.Session(readers[0])
except smartcard.Exceptions.NoCardException:
    print('Unable to connect to card or no card in reader')
    exit("Exit on error")

    
print "\n### START SELECT EF.dir"

SELECT = [0x00, 0xA4, 0x02, 0x0C, 0x02]
EFDIR = [0x2F, 0x00]

try:
    apduCommand = SELECT+EFDIR
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
except:
    print("Error executing APDU", apduCommand)
    
print "\n### START READ BINARY EF.dir"

READ_BINARY = [0x00, 0xB0, 0x00, 0x00,0x00, 0xFF]

try:
    apduCommand = READ_BINARY
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
except:
    print("Error executing APDU", apduCommand)    

print printAsHex(data)
print "Bytes read: ", len(data)-2, hex(len(data)-2)  #last 2 bytes are discarded (SW1/SW2) 
print toHexString(data)       
      

print "\n### START SELECT EF.CardAccess"

SELECT = [0x00, 0xA4, 0x02, 0x0C, 0x02]
EFCardAccess = [0x01, 0x1C]

try:
    apduCommand = SELECT+EFCardAccess
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
except:
    print("Error executing APDU", apduCommand)  
    
print "\n### START READ BINARY EF.CardAccess"

READ_BINARY = [0x00, 0xB0, 0x00, 0x00, 0xFF]

try:
    apduCommand = READ_BINARY
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
    print printAsHex(data)
    print toHexString(data) 
    print len(data)-2, hex(len(data)-2)
except:
    print("Error executing APDU", apduCommand)    

print "\n### START READ BINARY EF.CardAccess sequence 2"

READ_BINARY = [0x00, 0xB0, 0x00, 0xFF, 0xFF]

try:
    apduCommand = READ_BINARY
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
    print printAsHex(data)
    print toHexString(data) 
    print "Bytes read: ", len(data)-2, hex(len(data)-2)  #last 2 bytes are discarded (SW1/SW2) 
except:
    print("Error executing APDU", apduCommand)    

print "\n### TODO READ BINARY should stop after read bytes < 0xFF"

print "\n### START SELECT MF"
       
SELECT = [0x00, 0xA4, 0x00, 0x00]
MDIR = [0x2F, 0x00]

try:
    apduCommand = SELECT+MDIR
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
except:
    print("Error executing APDU", apduCommand)  
    
    
print "\n### START SELECT PCA Applet"
       
SELECT = [0x00, 0xA4, 0x04, 0x0C, 0x08]
AID = [0x0A, 0x00, 0x00, 0x07, 0x73, 0x50, 0x43, 0x41]

try:
    apduCommand = SELECT+AID
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
except:
    print("Error executing APDU", apduCommand)  

session.close()
