from datetime import datetime
import datetime
import ModeManager
import HardwareInteractions
import MessageManager
from Switch import SwitchList

class GlobalStates:
    timeChanged = False
    writeLock = False
    sendMessage = False
    netManRunning = True
    savedSwitches = []
    switchList = SwitchList()
    modeMan = ModeManager.ModeManager()



    def __init__(self):
        self.currentTime = datetime.datetime.now()
        
        self.messageToSend = MessageManager.BCMessage()
        self.messageToSend.CreateFromScratch(MessageManager.BCCommand.BCCINVALID,"helloWorld",69)   # blank default message
        self.modeMan = ModeManager()

    def UpdateSwitchState(self,newState):
        self.switchState = newState

    def UpdateTime(self,newTime,modeManager):
        self.currentTime = datetime.datetime.now()
        self.timeChanged = True
        modeManager.UpdateCharacteristic(ModeManager.Kind.DATE,self.currentTime)

    # def UpdateTemperature(self,newTemp,modeManager):
        # self.currentTemperature  
