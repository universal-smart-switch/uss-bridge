import os
import GlobalStates
import codecs
from array import array
from sys import platform

def LoadSettings():
    dirPath = os.path.join(os.getcwd(), "settings")  # get current settings directory
    if ( not (os.path.exists(dirPath))): # check if file exists
        os.mkdir(dirPath) 
    else:
        LoadSwitchSettings(dirPath)
        #LoadModeSettings(dirPath)

def LoadSwitchSettings(directoryPath):
    fullPath = directoryPath + '\\SwitchList.xml'
    if(os.path.exists(fullPath)):
        file = open(fullPath,"r")
        switchString =  file.read()
        if (( not len(switchString) == 0)):    # if string has required length
            GlobalStates.GlobalStates.switchList.FromXML(switchString)

def LoadModeSettings(directoryPath):
    fullPath = directoryPath + '\\ModeList.xml'
    if(os.path.exists(fullPath)):
        file = open(fullPath,"r")
        
def SaveSettings():
    dirPath = os.path.join(os.getcwd(), "settings")  # get current settings directory
    if ( not (os.path.exists(dirPath))): # check if file exists
        os.mkdir(dirPath) 

    SaveSwitchSettings(dirPath)
    
def SaveSwitchSettings(directoryPath):
    fullPath = directoryPath + '\\SwitchList.xml'
    if( not (os.path.exists(fullPath))):
        file = open(fullPath,"x")
    else:
        file = open(fullPath,"w")


    res = array("b", GlobalStates.GlobalStates.switchList.ToXML())
    dataString = codecs.decode(res, 'UTF-8')

    file.write(dataString)

    