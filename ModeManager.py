from enum import Enum
import GlobalStates

# possible types of characteristics
class CharacteristicType(Enum):
    TEMPERATURE = 1
    DATE = 2
    BLANK = 3

class Characterisic:
    met = False
    invert = False
    def __init__(self,CharacteristicType,value,invert):
        self.CharacteristicType = CharacteristicType
        self.value = value
        if (invert == True):
            self.invert = True
            met = True

# contains multiple characteristics which have to be met in order to execute switch
class Mode:
    characteristicsToMet = []    # tempval
    invert = False   
    executeMet = False  # execute condition met?
    onSingle = True # execute switch at first met characteristic

    def __init__(self,name,Characterisic):
        self.characteristicsToMet.append(Characterisic)
        self.name = name
    
    def CheckSpecific(self, CharacteristicType,value):    # update met-value of single characteristic type
        for x in self.characteristicsToMet:
            if (x.CharacteristicType == CharacteristicType) & (x.value == value):
                if (x.invert):
                    x.met = False
                else:
                    x.met = True
        
    def CheckExecuteMet(self):  # check if execute condition is met
        tempMet = False # temp variable -> if multiple threads are running
        for x in self.characteristicsToMet: # for each characteristic
            if (x.met == True): # check if met
                tempMet = True
                if (self.onSingle):
                    break
            else:
                tempMet = False
        self.executeMet = tempMet  # save new value

class ModeManager:
    modeList = [] # list of possible modes to select
    activated = False

    def __init__(self,globalstates):
        self.modeList.append(Mode("", Characterisic(CharacteristicType.BLANK,0,False)))   # add default mode -> does nothing
        self.globalStates = globalstates


    def CheckSelectedMode(self):
        self.modeList[0].CheckExecuteMet()
        if (self.selectedMode.executeMet):
            if(self.selectedMode.invert):
                self.globalStates.UpdateSwitchState(False)
            else:
                self.globalStates.UpdateSwitchState(True)

    def UpdateCharacteristic(self,CharacteristicType,value):
        self.selectedMode.CheckSpecific(CharacteristicType,value)
        self.CheckSelectedMode()



# testing purpose
tmpChrc = Characterisic(CharacteristicType.TEMPERATURE,22,False)
tmpMd = Mode("firstMode",tmpChrc)


newTemp = 24
tmpMd.CheckSpecific(CharacteristicType.TEMPERATURE,newTemp)
print(tmpMd.CheckExecuteMet())

newTemp = 22
tmpMd.CheckSpecific(CharacteristicType.TEMPERATURE,newTemp)
print(tmpMd.CheckExecuteMet())
