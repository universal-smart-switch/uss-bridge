from enum import Enum
import DefinedInformation
import xml.etree.ElementTree as ET
from xml.dom import minidom

# possible types of characteristics
class CharacteristicType(Enum):
    BLANK = 0
    TEMPERATURE = 1
    DATE = 2


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
    name = ''
    
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

    def FromXML(self,rawXMLString):
        rawXML = ET.fromstring(rawXMLString)

        if(rawXML.tag == 'mode'):
            self.name = rawXML.get('name')
            for child in rawXML:
                characType = CharacteristicType(int(child.get('type')))
                characVal = child.get('value')
                characMet = child.get('met')
                characInv = child.get('invert')

                characToAdd = Characterisic(characType,characVal,characInv)
                self.characteristicsToMet.clear
                self.characteristicsToMet.append(characToAdd)

    def ToXML(self):
       root = ET.Element("mode",name=self.name,invert=format(self.invert),executemet=format(self.executeMet),onSingle=format(self.onSingle))
       for item in self.characteristicsToMet:
        ET.SubElement(root, "characteristic",type=format(item.CharacteristicType.value) ,value=item.value,invert=format(self.invert),met=format(self.executeMet))
       
       tree = ET.ElementTree(root)
       return ET.tostring(root, encoding='utf8', method='xml')


class ModeManager:
    modeList = [] # list of possible modes to select
    activated = False

    def __init__(self):
        defMode = Mode()
        chr1 = Characterisic(CharacteristicType.BLANK,0,False)
        defMode.characteristicsToMet.append(chr1)
        defMode.name = "Default"
        self.modeList.append(defMode)   # add default mode -> does nothing


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

    def ToXML(self):
       root = ET.Element("modeList")
       
       for mode in self.modeList:
            md = ET.SubElement(root,"mode",name=format(mode.name),invert=format(mode.invert),executeMet=format(mode.executeMet),onSingle=format(mode.onSingle))
            for item in mode.characteristicsToMet:
                ET.SubElement(md, "characteristic",type=format(item.CharacteristicType.value) ,value=format(item.value),invert=format(item.invert),met=format(item.met))
       
       tree = ET.ElementTree(root)
       return ET.tostring(root, encoding='utf8', method='xml')

    def FromXML(self):

    

# testing purpose
#tmpChrc = Characterisic(CharacteristicType.TEMPERATURE,22,False)
#tmpMd = Mode()


#newTemp = 24
#tmpMd.CheckSpecific(CharacteristicType.TEMPERATURE,newTemp)
#print(tmpMd.CheckExecuteMet())

#newTemp = 22
#tmpMd.CheckSpecific(CharacteristicType.TEMPERATURE,newTemp)
#print(tmpMd.CheckExecuteMet())

#jsonstr1 = json.dumps(tmpMd.__dict__)
#print(jsonstr1)

#testuuus = '<?xml version=\"1.0\" encoding=\"utf-16\"?>\r\n<mode name=\"hiii\" invert=\"False\" executemet=\"False\" onSingle=\"False\">\r\n  <characteristic type=\"1\" value=\"22\" invert=\"False\" met=\"False\" />\r\n</mode>'

#secondMode = Mode()
#secondMode.FromXML(testuuus)

#test = secondMode.ToXML()


#thirdMode = Mode()
#thirdMode.FromXML(secondMode.ToXML())

#print(thirdMode.name)
#print(secondMode.name)

#print(thirdMode.invert)
#print(secondMode.invert)

