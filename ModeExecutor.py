from GlobalStates import GlobalStates as GS
import logging
import threading
import time
import BluetoothManager as BT
from MessageManager import BSMessage
from MessageManager import BSCommand

def Start():
    print('unimplemented')
    thr = threading.Thread(target=CheckThread)
    thr.start()


def CheckThread():
    while(GS.modeExecutorRunning):
        while(GS.writeLock):
            print('wait for lock end')
        
        #for mode in GS.modeMan.modeList:
            #mode.CheckExecuteMet()

        for switch in GS.switchList.raw:    # for each switch
            for mode in GS.modeMan.modeList:    # for each mode
                if mode.name == switch.mode:    # get correct mode

                    doEx = mode.ReviewExecuteMet(switch.temp)
                    if (doEx):

                        if (mode.invert):
                            switch.stateOn = False
                        else:
                            switch.stateOn = True
                            
                        print('change switch state from ' + switch.name + ' to ' + str(switch.stateOn) + "[not implemented]")
                        nMes = BSMessage()
                        #nMes.CreateFromScratch(BSCommand.BSGETSTATEREP,0xFFFF,switch.address)
                        #BT.SendMessageTo(switch.btaddress,nMes.fullMessage)

                #if ((mode.name == switch.mode)  and mode.executeMet):
                    #print('change switch state from ' + switch.name + ' to ' + str(not switch.stateOn) + "[not implemented]")
                    #switch.stateOn = not switch.stateOn
