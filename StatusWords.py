import smartcard
from compiler.pycodegen import EXCEPT
from smartcard.CardType import ATRCardType

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
    
print "\n###Get the ATR response"
atr = session.getATR()
print(atr)
print printAsHex(atr)
print smartcard.util.toHexString(atr)

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
print smartcard.util.toHexString(data)  