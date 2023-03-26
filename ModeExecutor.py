from GlobalStates import GlobalStates as GS
import logging
import asyncio
import threading
import time
import BluetoothManager as BT
from MessageManager import BSMessage
from MessageManager import BSCommand
import BluetoothManager as BM

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
                        asyncio.run(BM.setValueSwitch(switch.btaddress,switch.stateOn)) # set state

                #if ((mode.name == switch.mode)  and mode.executeMet):
                    #print('change switch state from ' + switch.name + ' to ' + str(not switch.stateOn) + "[not implemented]")
                    #switch.stateOn = not switch.stateOn
