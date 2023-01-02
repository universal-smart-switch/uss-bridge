from GlobalStates import GlobalStates as GS
import logging
import threading
import time

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

        for switch in GS.switchList.raw:
            for mode in GS.modeMan.modeList:
                if mode.name == switch.mode:

                    doEx = mode.ReviewExecuteMet(switch.temp)
                    if (doEx):
                        print('change switch state from ' + switch.name + ' to ' + str(not switch.stateOn) + "[not implemented]")

                #if ((mode.name == switch.mode)  and mode.executeMet):
                    #print('change switch state from ' + switch.name + ' to ' + str(not switch.stateOn) + "[not implemented]")
                    #switch.stateOn = not switch.stateOn
