from smartcard.util import *
from string import  *
from scipy.cluster.setup import DEFINE_MACROS

statusWordFileName = '../APDUresponses.csv'

def getStatusWordType(sw1,sw2):
    if (len(sw2)==2):
        if (sw2[0] in hexdigits):
             if  (sw2[1] in hexdigits):
                 return 0       #standard status word with two hex codes
             else:
                 return 1       #status word with last nibble of sw2 contains information
        else:
            return 2            #status word with last nibble of sw2 contains information
    else:
        if (len(sw2)==1):
            if (sw2[0] in hexdigits):
                return 0
    print "Error: ", sw1, sw2
    return -1


class ResponseAPDUStatus:
    def __init__(self):
        self.wordDict0={}    #contains basic status word with sw1, sw2 hex value
        self.wordDict1={}   #contains special status word with sw1 hex value and sw2 special meaning
        self.wordDict2={}   #contains special status word with sw1 hex value and sw2 special meaning
        statusWordFileName = '../APDUresponses.csv'
        self.importAPDUStatusses(statusWordFileName)
    
    def importAPDUStatusses(self, fname):
        hexdigits = '0123456789ABCDEF'
        with open(fname,"r") as f:
            content = f.readlines()
        for x in content:
            (cat,sub,flag,desc) = rsplit(x,";")[:4]
            type = getStatusWordType(cat, sub)
            if type==0:
                self.wordDict0[(atoi(cat,16),atoi(sub,16))]=[flag,desc]
            else:
                if type==1:
                    self.wordDict1[(atoi(cat,16),atoi(sub[0],16))]=[sub[1],flag,desc]
                else:
                    self.wordDict2[(atoi(cat,16))]=[sub,flag,desc]
        f.close()
    
    def getStatusWordCount(self):
        return len(self.wordDict0)
                
    def getCategory(self,sw):
        #sw1,sw1 should be integers [0:255]
        return self.wordDict[(sw)]
    
    def getStatusWordInfo(self,swType,sw1,sw2):
        if swType==0:
            return self.wordDict0[(atoi(sw1,16),atoi(sw2,16))]
        else:
            return ''
        
    def getStatusWordInfo(self,sw):
        #sw = list (swType, sw1, sw2)
        if sw[0]==0:
            return self.wordDict0[(atoi(sw[1],16),atoi(sw[2],16))]
        else:
            if sw[0]==1:
                return self.wordDict1[(atoi(sw[1],16),atoi(sw[2][0],16))]
            else:
                if sw[0]==2:
                    return self.wordDict2[(atoi(sw[1],16))]
            return ''
        
    def printStatusWordInfo(self,sw):
        #sw = list (swType, sw1, sw2)
        if sw[0]==0:
            info=self.wordDict0[(atoi(sw[1],16),atoi(sw[2],16))]
            sws = hex(atoi(sw[1],16)), hex(atoi(sw[2],16))
            param = ''
            level = info[0]
            descr = info[1]
        else:
            if sw[0]==1:
                info=self.wordDict1[(atoi(sw[1],16),atoi(sw[2][0],16))]
                sws = hex(atoi(sw[1],16)), hex(atoi(sw[2][0],16))
                param = info[0]
                level = info[1]
                descr = info[2] 
            else:
                if sw[0]==2:
                    info= self.wordDict2[(atoi(sw[1],16))]
                    sws = hex(atoi(sw[1],16))
                    param = info[0]
                    level = info[1]
                    descr = info[2] 
        print"Status words: ", sws
        print "Parameter: ", param
        print "Level: ",level
        print "Description: ",descr
        return ''
        
class ResponseAPDU:
    def __init__(self,sw1,sw2,data):
        # sw1, sw2 are stored as integers and provided as hex bytes.
        self.sw1=sw1
        self.sw2=sw2
        self.statusWordType = getStatusWordType(self.sw1,self.sw2)
        self.data=data
    
    def getStatusWords(self):
        return self.statusWordType,self.sw1,self.sw2
    
    def hexPrint(self):
        return hex(atoi(self.sw1,16)),hex(atoi(self.sw2,16))
    
print "\nTesting ResponseAPDUStatus class"    
words = ResponseAPDUStatus()
print "Dictionary of type 0:", words.wordDict0
print "Dictionary of type 1:", words.wordDict1
print "Dictionary of type 2:", words.wordDict2

print "\nTesting ResponseAPDUS class swType = 0"   
resp = ResponseAPDU('63','C1','')
print resp.getStatusWords()
print words.getStatusWordInfo(resp.getStatusWords())
words.printStatusWordInfo(resp.getStatusWords())

print "\nTesting ResponseAPDUS class swType = 1"   
resp = ResponseAPDU('63','CX','')
print resp.getStatusWords()
print words.getStatusWordInfo(resp.getStatusWords())
words.printStatusWordInfo(resp.getStatusWords())

print "\nTesting ResponseAPDUS class swType = 2"   
resp = ResponseAPDU('63','XX','')
print resp.getStatusWords()
print words.getStatusWordInfo(resp.getStatusWords())
words.printStatusWordInfo(resp.getStatusWords())
