import os
import GlobalStates
import codecs
from array import array
from sys import platform
import DefinedInformation as DI



def LoadSettings():

    if ( 'linux' not in platform ):
        DI.delimiter = "\\"

    dirPath = os.path.join(os.getcwd(), "settings")  # get current settings directory
    if ( not (os.path.exists(dirPath))): # check if file exists
        os.mkdir(dirPath) 
    else:
        LoadModeSettings(dirPath)
        LoadSwitchSettings(dirPath)

def LoadSwitchSettings(directoryPath):
    fullPath = directoryPath + DI.delimiter + 'SwitchList.xml'
    if(os.path.exists(fullPath)):
        file = open(fullPath,"r")
        switchString =  file.read()
        if (( not len(switchString) == 0)):    # if string has required length
            GlobalStates.GlobalStates.switchList.FromXML(switchString,False)

def LoadModeSettings(directoryPath):
    fullPath = directoryPath + DI.delimiter +'ModeList.xml'
    if(os.path.exists(fullPath)):
        file = open(fullPath,"r")
        switchString = file.read()
        if (( not len(switchString) == 0)):    # if string has required length
            GlobalStates.GlobalStates.modeMan.FromXML(switchString)
        
def SaveSettings():
    dirPath = os.path.join(os.getcwd(), "settings")  # get current settings directory
    if ( not (os.path.exists(dirPath))): # check if file exists
        os.mkdir(dirPath) 

    SaveSwitchSettings(dirPath)
    SaveModeSettings(dirPath)
    
def SaveSwitchSettings(directoryPath):
    fullPath = directoryPath + '\\SwitchList.xml'
    if( not (os.path.exists(fullPath))):
        file = open(fullPath,"x")
    else:
        file = open(fullPath,"w")


    res = array("b", GlobalStates.GlobalStates.switchList.ToXML())
    dataString = codecs.decode(res, 'UTF-8')

    file.write(dataString)

def SaveModeSettings(directoryPath):
    fullPath = directoryPath + '\\ModeList.xml'
    if( not (os.path.exists(fullPath))):
        file = open(fullPath,"x")
    else:
        file = open(fullPath,"w")


    res = array("b", GlobalStates.GlobalStates.modeMan.ToXML())
    dataString = codecs.decode(res, 'UTF-8')

    file.write(dataString)