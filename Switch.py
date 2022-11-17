import datetime
import time
import NameGenerator
import os
import xml.etree.ElementTree as ET

class Switch:
    name = ""
    address = ""
    mode = ""
    stateOn = False

    def __init__(self,address):
        self.lastContacted = datetime.datetime.now()
        self.address = address
        self.name = NameGenerator.get_random_name()


class SwitchList:
    raw = []

    def Save(self):
        directory_path = os.path.join(os.getcwd(), "settings")  # get current settings directory 

        if ( not (os.path.exists(directory_path))): # check if file exists
            os.mkdir(directory_path)
        
        full_path = directory_path + '\\SwitchList.xml'

        root = ET.Element("switchList")
        for item in self.raw:
            ET.SubElement(root,"switch",name=item.name,address=item.address,stateOn=format(item.stateOn),lastContacted=format(datetime.datetime.timestamp(item.lastContacted)),mode=item.mode)
        
        tree = ET.ElementTree(root)
        tree.write(full_path)

    def Load(self):
        directory_path = os.path.join(os.getcwd(), "settings")
        file = open(directory_path + '\\SwitchList.xml', 'r')
        xml = ET.parse(file)
        self.FromXML(0,xml)


    def ToXML(self):
        root = ET.Element("switchList")
        for item in self.raw:
            ET.SubElement(root,"switch",name=item.name,address=item.address,stateOn=format(item.stateOn),lastContacted=format(datetime.datetime.timestamp(item.lastContacted)),mode=item.mode)
        return ET.tostring(root, encoding='utf8', method='xml')

    

    def FromXML(self,xmldata,rawXML):

        if not rawXML:
            rawXML = ET.fromstring(xmldata) # get xml from string
        if(rawXML.tag == 'switchList'):
            self.characteristicsToMet.clear # clear current list

            for child in rawXML:    # for each switch
                # get data from xaml
                recSw = Switch()
                recSw.name = child.get('name')
                recSw.address = child.get('address')
                recSw.stateOn = bool(child.get('stateOn'))
                recSw.lastContacted = datetime.datetime.fromtimestamp(child.get('lastContacted'))
                recSw.mode = child.get('mode')

                self.raw.append(recSw)  # add switch







    