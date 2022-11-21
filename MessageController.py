from MessageManager import BCMessage
from MessageManager import BCCommand
from ModeManager import Mode
from ModeManager import Characterisic
from ModeManager import ModeManager
import DefinedInformation as DI
import NetworkManager as NM
import datetime
from Switch import Switch
from Switch import SwitchList
from GlobalStates import GlobalStates
import datetime
import SettingsManager

# create message out of received bytes
def ValidateMessage(possMes):
    msg = BCMessage()
    msg.CreateFromRaw(possMes)
    #md = Mode()   
    #md.FromXML(msg.dataString)
    ReceiveController(msg)

# what to do with message?
def ReceiveController(message):
    if (message.command == BCCommand.BCCINVALID):
        print('unimplemented')

    elif (message.command == BCCommand.BCCECHOREQ):
        echoResponse = BCMessage()  # create response message
        curDT = datetime.datetime.now()

        # get unix timestamp and format in .NET style
        unixStamp = DI.DateTimeToUnix(datetime.datetime.now())
        unxStampStr = str(unixStamp)
        unxStampStr = unxStampStr.replace(".0","")

        # send responsd
        echoResponse.CreateFromScratch(BCCommand.BCCECHOREP,unxStampStr,0)
        NM.RequestToSend(echoResponse)

    elif (message.command == BCCommand.BCCECHOREP):
        print('unimplemented')

    elif (message.command == BCCommand.BCCGETSWITCHES):
        getSwRep = BCMessage()
        getSwRep.CreateFromScratch(BCCommand.BCCGETSWITCHESREP,GlobalStates.switchList.ToXML(),0)
        NM.RequestToSend(getSwRep)

    elif (message.command == BCCommand.BCCGETSWITCHESREP):
        test = message.dataString
        GlobalStates.writeLock = True
        GlobalStates.switchList.FromXML(message.dataString)
        SettingsManager.SaveSettings()
        GlobalStates.writeLock = False

    elif (message.command == BCCommand.BCCGETMODES):
        modeStr = GlobalStates.modeMan.ToXML()
        getModesRep = BCMessage()
        getModesRep.CreateFromScratch(BCCommand.BCCGETMODESREP,modeStr,0)
        NM.RequestToSend(getModesRep)

    elif (message.command == BCCommand.BCCGETMODESREP):
        modeStr = message.dataString
        GlobalStates.writeLock = True
        GlobalStates.modeMan.FromXML(modeStr)
        GlobalStates.writeLock = False

    elif (message.command == BCCommand.BCCGETSYSINFO):
        print('unimplemented')