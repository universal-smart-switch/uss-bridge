import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import DefinedInformation as DI
from GlobalStates import GlobalStates as GS
from Switch import Switch
import SettingsManager as SM

foundSwitchesAddresses = []
foundSwitchesAddressesBluetooth = []

foundSwitches = {}

async def searchAndAdd():
    devices = await BleakScanner.discover()
    for d in devices:
        #print(d)
        name = d.name
        if (name.__contains__("Smartswitch-")):
            nmSpl = d.name.split('-')
            swID = nmSpl[1]
            print(d.name + ":" + d.address)

            foundSwitches[swID] = d.address
            

    for id in foundSwitchesAddressesBluetooth:
        async with BleakClient(foundSwitches[id]) as client:

            switch = Switch()
            

            # if switch is new -> add to list
            for savedSwitch in GS.switchList.raw:
                if savedSwitch.address == id:   # if not new
                    switch = savedSwitch    # set 
                    break
                else:
                    switch.address = id # save id
                    switch.btaddress = foundSwitches[id]    # save address
                    switch.mode = GS.modeMan.modeList[0].name   # set default mode
                    GS.switchList.raw.append(switch)



            svcs = await client.get_services()  # get all services

            # read values
            temperatureBytes = await client.read_gatt_char(DI.BSuuid_chr_temp)
            stateBytes = await client.read_gatt_char(DI.BSuuid_chr_state)

            # hast to be decoded first!!!11
            temp = int.from_bytes(temperatureBytes,byteorder='big')
            state = int.from_bytes(stateBytes,byteorder='big')       

            # save states
            switch.stateOn = state
            switch.temp = temp
            

    SM.SaveSwitchSettings   # save switch settings to file

async def getValueFromSwitch(address,valueType):
    async with BleakClient(address) as client:
            value = ''

            # read values
            # hast to be decoded first!!!11
            if valueType == 'temp':
                tmp = await client.read_gatt_char(DI.BSuuid_chr_temp)
                value = int.from_bytes(tmp,byteorder='big')
            else:
                state = await client.read_gatt_char(DI.BSuuid_chr_state)
                value = int.from_bytes(state,byteorder='big') 
            
            return value



async def mainPhone():
    devices = await BleakScanner.discover()
    add = ""
    for d in devices:
        #print(d)
        name = d.name
        if (name.__contains__("Tim")):
            print(d.name + ":" + d.address)
            add = d.address
            break


    async with BleakClient(add) as client:
        svcs = await client.get_services()

        print("Services:")
        for service in svcs:
            print(service)

        temperature = await client.read_gatt_char(DI.BSuuid_chr_temp)
        state = await client.read_gatt_char(DI.BSuuid_chr_state)

        print(int.from_bytes(temperature,byteorder='big'))
        print(int.from_bytes(state,byteorder='big'))


asyncio.run(mainPhone())