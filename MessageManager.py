import DefinedInformation
from enum import Enum
import codecs
from array import array
# types of messages

class BCCommand(Enum):
    BCCINVALID = DefinedInformation.BCCInvalid
    BCCGETSWITCHES = DefinedInformation.BCCGetSwitches
    BCCGETMODESWITCHES = DefinedInformation.BCCGetModeSwitches
    BCCGETSWITCHSTATE = DefinedInformation.BCCGetStateSwitch
    BCCSENDSWITCHES = DefinedInformation.BCCSendSwitches
    BCCSENDMODESWITCHES = DefinedInformation.BCCSendModeSwitches
    BCCECHOREQUEST = DefinedInformation.BCCEchoRequest
    BCCECHORESPONSE = DefinedInformation.BCCEchoResponse
    BCCSENDSTATESWITCH = DefinedInformation.BCCSendStateSwitch
    BCCSETMODESWITCH = DefinedInformation.BCCSetModeSwitch

class BCMessage:
    data = ""
    fullMessage = []
    correct = False
    # command = BCCommand.INVALID

    def CreateFromScratch(self,command,data,switchId):
        self.command = command
        self.commandRaw = command.value
        self.dataString = data
        self.data = bytes(data, 'utf-8')

        # int to byte
        idList = switchId.to_bytes(1, 'big')
        self.id = idList[0]

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
        self.checkSum = self.CalcCheckSum(data)
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

        self.fullMessage = raw  # save full message again
    
    def GetByteFromBCCommand(command) :
        if (command == BCCommand.BCCGETSWITCHES):
            return DefinedInformation.BCCGetSwitches
        
    def CalcCheckSum(self, dataToCalc ):
        fullVal = 0
        dataBytes = []
        dataBytes = bytes(dataToCalc, 'utf-8')
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
#testing

#tmpMsg = BCMessage()
#tmpMsg.CreateFromScratch(BCCommand.BCCGETMODESWITCHES,"hiWelt",34)

#testMsg = BCMessage()
#testMsg.CreateFromRaw(tmpMsg.fullMessage.copy())

#print("Checksum correct : + {}".format(testMsg.checkSum))
#print("Values [S|R] : " + tmpMsg.dataString + "|" + testMsg.dataString)
#print("CommandRaw [S|R] : " + tmpMsg.commandRaw + "|" + testMsg.commandRaw)
#print("Command [S|R] : " + tmpMsg.command + "|" + testMsg.command)
