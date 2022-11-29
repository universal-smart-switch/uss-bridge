from GlobalStates import GlobalStates as GS


def Start():
    print('unimplemented')


def CheckThread():
    while(GS.writeLock):
        print('wait for lock end')
    
    for mode in GS.modeMan.modeList:
        mode.CheckExecuteMet()

    for switch in GS.switchList:
        for mode in GS.modeMan.modeList:
            if ((mode.name == switch.mode)  and mode.executeMet):
                print('change switch state from ' + switch.name + ' to ')
