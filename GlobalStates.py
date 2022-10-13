from datetime import datetime
import datetime
import ModeManager
import HardwareInteractions

class GlobalStates:
    timeChanged = False
    switchState = False

    def __init__(self):
        self.currentTime = datetime.datetime.now()

    def UpdateSwitchState(self,newState):
        self.switchState = newState

    def UpdateTime(self,newTime,modeManager):
        self.currentTime = datetime.datetime.now()
        self.timeChanged = True
        modeManager.UpdateCharacteristic(ModeManager.Kind.DATE,self.currentTime)

    # def UpdateTemperature(self,newTemp,modeManager):
        # self.currentTemperature  
