import DefinedInformation
from enum import Enum
import codecs
from array import array
# types of messages

class BCCommand(Enum):
    BCCINVALID = DefinedInformation.BCCInvalid
    BCCECHOREQ = DefinedInformation.BCCEchoReq
    BCCECHOREP = DefinedInformation.BCCEchorRep
    BCCGETSWITCHES = DefinedInformation.BCCGetSwitches
    BCCGETSWITCHESREP = DefinedInformation.BCCGetSwitchesRep
    BCCGETMODES = DefinedInformation.BCCGetModes
    BCCGETMODESREP = DefinedInformation.BCCGetModesRep
    BCCGETSYSINFO = DefinedInformation.BCCGetSysInfo
    BCCGETSYSINFOREP = DefinedInformation.BCCGetSysInfoRep
    BCCSETSWITCHSTATE = DefinedInformation.BCCSetSwitchState

class BCMessage:
    data = []
    fullMessage = []
    correct = False
    # command = BCCommand.INVALID

    def CreateFromScratch(self,command,data,switchId):

        test = type(data)

        self.command = command
        self.commandRaw = command.value
        self.dataString = data

        if(type(data) == str):
            self.data = bytes(data, encoding='utf-8')
        else:
            self.data = data

        # int to byte
        idList = switchId.to_bytes(1, 'big')
        self.id = idList[0]

        # add endmark byte  s
        for item in bytes(DefinedInformation.BCMarkEnd, 'utf-8'):
            self.fullMessage.append(item)

        # add all data bytes to message
        for item in self.data:
            self.fullMessage.append(item)
        
        # add raw command byte
        self.fullMessage.append(self.commandRaw)

        # add id bytes
        self.fullMessage.append(self.id)

        # calculate length
        lengthInt = len(data)
        #self.length = len(data)

        # calc checksum and add to message
        self.checkSum = self.CalcCheckSum(self.data)
        self.fullMessage.append(self.checkSum)
        self.correct = True

        # add length to message
        # self.fullMessage.append(self.length)
        for item in lengthInt.to_bytes(3, 'big'):
            self.fullMessage.append(item)

        # add mark bytes to message
        for item in bytes(DefinedInformation.BCMark, 'utf-8'):
            self.fullMessage.append(item)
    
    def CreateFromRaw(self, raw):

        self.fullMessage = []

        for item in raw:
            self.fullMessage.append(item)

        self.fullMessage.reverse()
        
        self.RemoveFirstItems(self.fullMessage,2)  #remove mark bytes

        # save length and remove
        lengthBytes = [self.fullMessage[2],self.fullMessage[1],self.fullMessage[0]]
        self.length =  int.from_bytes(lengthBytes, "big")
        self.RemoveFirstItems(self.fullMessage,3)

        # save and remove checksum from message
        self.checkSum = self.fullMessage[0]      
        self.RemoveFirstItems(self.fullMessage,1)  # remove checksum from message

        # save id and remove
        self.id = self.fullMessage[0]
        self.RemoveFirstItems(self.fullMessage,1)

        # save command and remove
        self.commandRaw = self.fullMessage[0]
        self.command = BCCommand(self.commandRaw)
        self.RemoveFirstItems(self.fullMessage,1)

        # remove endmak
        self.fullMessage.reverse()
        self.RemoveFirstItems(self.fullMessage,3)  #remove endmark bytes
        self.fullMessage.reverse()

    	# save string
        self.fullMessage.reverse()  # reverse in order to get string in right order
        res = array("b", self.fullMessage)
        self.dataString = codecs.decode(res, 'UTF-8')

        # save checksum
        self.realCheckSum =  self.CalcCheckSum(self.dataString)
        if( self.realCheckSum == self.checkSum):
            self.correct = True
        else:
            self.correct = False

        self.correct = True

        self.fullMessage = raw  # save full message again
    
    def GetByteFromBCCommand(command) :
        if (command == BCCommand.BCCGETSWITCHES):
            return DefinedInformation.BCCGetSwitches
        
    def CalcCheckSum(self, dataToCalc ):
        fullVal = 0
        dataBytes = []

        if(type(dataToCalc) == str):
            dataBytes = bytes(dataToCalc, encoding='utf-8')
        else:
            dataBytes = dataToCalc
            
        datLen = dataBytes.count
        for item in dataBytes:
            fullVal += item

        while(fullVal > 8):
            fullVal = fullVal / 8

        # to byte
        fullVal = int(fullVal)
        fullValList = fullVal.to_bytes(1, 'big')
        fullVal = fullValList[0]

        return fullVal

    def RemoveFirstItems(self,coll,amount):
        for x in range(amount):
            coll.remove(coll[0])

class BSCommand(Enum):
    BSINVALID = DefinedInformation.BSInvalid
    BSGETSTATE = DefinedInformation.BSGetState
    BSGETSTATEREP = DefinedInformation.BSGetStateRep
    BSGETTEMP = DefinedInformation.BSGetTemp
    BSGETTEMPREP = DefinedInformation.BSGetTempRep
    BSECHOREQUEST = DefinedInformation.BSEchoRequest
    BSECHOREPLY = DefinedInformation.BSEchoReply

class BSMessage:
    data = []
    fullMessage = []
    correct = False

    def CalcCheckSum(self, dataToCalc ):
        fullVal = 0
        dataBytes = []

        if(type(dataToCalc) == str):
            dataBytes = bytes(dataToCalc, encoding='utf-8')
        else:
            dataBytes = dataToCalc
            
        datLen = dataBytes.count
        for item in dataBytes:
            fullVal += item

        while(fullVal > 8):
            fullVal = fullVal / 8

        # to byte
        fullVal = int(fullVal)
        fullValList = fullVal.to_bytes(1, 'big')
        fullVal = fullValList[0]

        return fullVal

    def RemoveFirstItems(self,coll,amount):
        for x in range(amount):
            coll.remove(coll[0])

    def CreateFromScratch(self,command,data,switchId):
        self.command = command
        self.commandRaw = command.value
        self.dataString = data

        if(type(data) == str):
            self.data = bytes(data, encoding='utf-8')
        else:
            self.data = data

        # int to byte
        idList = switchId.to_bytes(1, 'big')
        self.id = idList[0]

        # add endmark byte  s
        for item in bytes(DefinedInformation.BSMarkEnd, 'utf-8'):
            self.fullMessage.append(item)

        # add all data bytes to message
        for item in self.data:
            self.fullMessage.append(item)
        
        # add raw command byte
        self.fullMessage.append(self.commandRaw)

        # add id bytes
        self.fullMessage.append(self.id)

        # calc checksum and add to message
        self.checkSum = self.CalcCheckSum(self.data)
        self.fullMessage.append(self.checkSum)
        self.correct = True

        # add mark bytes to message
        for item in bytes(DefinedInformation.BSMark, 'utf-8'):
            self.fullMessage.append(item)
    
    def CreateFromRaw(self, raw):

        self.fullMessage = []

        for item in raw:
            self.fullMessage.append(item)

        self.fullMessage.reverse()
        
        self.RemoveFirstItems(self.fullMessage,2)  #remove mark bytes

        # save and remove checksum from message
        self.checkSum = self.fullMessage[0]      
        self.RemoveFirstItems(self.fullMessage,1)  # remove checksum from message

        # save id and remove
        self.id = self.fullMessage[0]
        self.RemoveFirstItems(self.fullMessage,1)

        # save command and remove
        self.commandRaw = self.fullMessage[0]
        self.command = BSCommand(self.commandRaw)
        self.RemoveFirstItems(self.fullMessage,1)

        # remove endmak
        self.fullMessage.reverse()
        self.RemoveFirstItems(self.fullMessage,2)  #remove endmark bytes
        self.fullMessage.reverse()

    	# save string
        self.fullMessage.reverse()  # reverse in order to get string in right order
        self.data = self.fullMessage
        res = array("b", self.fullMessage)
        self.dataString = codecs.decode(res, 'UTF-8')

        # save checksum
        self.realCheckSum =  self.CalcCheckSum(self.dataString)
        if( self.realCheckSum == self.checkSum):
            self.correct = True
        else:
            self.correct = False

        self.correct = True

        self.fullMessage = raw  # save full message again
    




#testing

#tmpMsg = BSMessage()
#tmpMsg.CreateFromScratch(BSCommand.BSECHOREPLY,"hiWelt",34)

#testMsg = BSMessage()
#testMsg.CreateFromRaw(tmpMsg.fullMessage.copy())

#print("Checksum correct : + {}".format(testMsg.checkSum))
#print("Values [S|R] : " + tmpMsg.dataString + "|" + testMsg.dataString)
#print("CommandRaw [S|R] : " + tmpMsg.commandRaw + "|" + testMsg.commandRaw)
#print("Command [S|R] : " + tmpMsg.command + "|" + testMsg.command)
