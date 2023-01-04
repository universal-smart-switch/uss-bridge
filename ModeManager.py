from enum import Enum
import DefinedInformation
import xml.etree.ElementTree as ET
from xml.dom import minidom
import DefinedInformation as DI
import time
from datetime import datetime

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

    def GetDateTimeVal(self):
        return DI.UnixToDateTime(self.value)

    def SetDateTimeVal(self,dt):
        self.value = DI.DateTimeToUnix(dt)

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

    def ReviewExecuteMet(self,temp):

        tempExMet = False
        singleExMet = False        

        for x in self.characteristicsToMet:
            
            

            # check type
            if (    (x.CharacteristicType == CharacteristicType.TEMPERATURE)    and temp == x.value):
                if (x.invert == True): x.met = False
                else: x.met = True
            
            if (    (x.CharacteristicType == CharacteristicType.DATE)):
                dt = x.GetDateTimeVal()
                # check if datetime is same
                if (datetime.hour == dt.hour and datetime.minute == x.minute):
                    if (x.invert == True): x.met = False
                    else: x.met = True

            if ( not x.met):
                tempExMet = False
            else:
                if self.onSingle == True:
                    singleExMet = True
                    tempExMet = True
                else:
                    tempExMet == True

        if (singleExMet == True or tempExMet == True):
            self.executeMet = True
            return True
        else:
            self.executeMet = False
            return False
            

        
                


        

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

    #def __init__(self):
        #defMode = Mode()
        #chr1 = Characterisic(CharacteristicType.BLANK,0,False)
        #defMode.characteristicsToMet.append(chr1)
        #defMode.name = "Default"

        #if ( not (len(self.modeList) > 0)):
            #self.modeList.append(defMode)   # add default mode -> does nothing


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

    def FromXML(self,xmlString):
        rawXML = ET.fromstring(xmlString)

        if(rawXML.tag == 'modeList'):
            
            self.modeList.clear()
            default = Mode()
            #default.characteristicsToMet.append(Characterisic(CharacteristicType.BLANK,0,0))
            #self.modeList.append(default)

            for child in rawXML:

                recMode = Mode()
                recMode.characteristicsToMet.clear()
                recMode.name = child.get('name')
                recMode.invert = format(child.get('invert'))
                recMode.executeMet = format(child.get('executeMet'))
                recMode.onSingle = format(child.get('onSingle'))


                for subchild in child:
                    characType = CharacteristicType(int(subchild.get('type')))
                    characVal = subchild.get('value')
                    characMet = subchild.get('met')
                    characInv = subchild.get('invert')
                    characToAdd = Characterisic(characType,characVal,characInv)
                    characToAdd.met = characMet
                    recMode.characteristicsToMet.append(characToAdd)
                
                self.modeList.append(recMode)
    

    

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

