from MessageManager import BCMessage
from MessageManager import BCCommand
from ModeManager import Mode
from ModeManager import Characterisic
import DefinedInformation as DI
import NetworkManager as NM
import datetime
from Switch import Switch
from Switch import SwitchList
from GlobalStates import GlobalStates
import datetime

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

    if (message.command == BCCommand.BCCECHOREP):
        print('unimplemented')

    if (message.command == BCCommand.BCCGETSWITCHES):
        getSwRep = BCMessage()
        getSwRep.CreateFromScratch(BCCommand.BCCGETSWITCHESREP,GlobalStates.switchList.ToXML(),0)
        NM.RequestToSend(getSwRep)

    if (message.command == BCCommand.BCCGETSWITCHESREP):
        test = message.dataString
        GlobalStates.switchList.FromXML(message.dataString)

    if (message.command == BCCommand.BCCGETMODES):
        print('unimplemented')


    if (message.command == BCCommand.BCCGETSYSINFO):
        print('unimplemented')