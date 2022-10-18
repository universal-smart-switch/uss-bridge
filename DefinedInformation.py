class DefinedInformation:
    BCMark = "$C"
    BSMark = "$S"

    
    BSBytesMark = 2
    BSBytesLength = 3
    BSBytesCheckSum = 1
    BSBytesHeader = BSBytesMark + BSBytesLength

    BCCInvalid = 1
    BCCGetSwitches = 2
    BCCGetModeSwitches = 3
    BCCGetStateSwitch = 4
    BCCSendSwitches = 5
    BCCSendModeSwitches = 6
    BCCSendStateSwitch = 7
    BCCEchoRequest = 8
    BCCSetModeSwitch = 9

    BluetoothBridgePin = "welcome"
    BluetoothAuthentificate = True
    BluetoothBridgeAdress = "test"

    BridgeCOMBaud = 9600
