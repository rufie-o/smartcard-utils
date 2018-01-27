import smartcard
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
    session = smartcard.Session(readers[1])
except smartcard.Exceptions.NoCardException:
    print('Unable to connect to card or no card in reader')
    exit("Exit on error")
    
print "\n### START GET VENDOR ID"

VENDOR = [0xFF, 0x9A, 0x1, 0x7,0xFF]

try:
    apduCommand = VENDOR
    data, sw1, sw2 = session.sendCommandAPDU(apduCommand)
    print "DATA READ: %s " % (data)
    print "SW1 SW2: %02X %02X" % (sw1, sw2)
except:
    print("Error executing APDU", apduCommand)
    
print "\n###Get the ATR response"
atr = session.getATR()
print(atr)
print printAsHex(atr)