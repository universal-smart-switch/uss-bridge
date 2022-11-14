from MessageManager import BCMessage
from MessageManager import BCCommand
from ModeManager import Mode
from ModeManager import Characterisic
import DefinedInformation as DI
import NetworkManager as NM

def ValidateMessage(possMes):
    msg = BCMessage()
    msg.CreateFromRaw(possMes)
    #md = Mode()   
    #md.FromXML(msg.dataString)
    MessageController(msg)

def MessageController(message):
    if (message.command == BCCommand.BCCINVALID):
        print('unimplemented')
    elif (message.command == BCCommand.BCCGETSWITCHES):
        print('unimplemented')
    elif (message.command == BCCommand.BCCGETMODESWITCHES):
        print('unimplemented')
    elif (message.command == BCCommand.BCCGETSWITCHSTATE):
        print('unimplemented')
    elif (message.command == BCCommand.BCCSETMODESWITCH):
        print('unimplemented')
    elif (message.command == BCCommand.BCCECHOREQUEST):
        echoResponse = BCMessage()
        echoResponse.CreateFromScratch(BCCommand.BCCECHORESPONSE,"0",0)
        NM.RequestToSend(echoResponse)

    elif (message.command == DI.BCCSetModeSwitch):
        print('unimplemented')