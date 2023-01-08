import datetime
import time

delimiter = "/"

# Bridge <-> Client
BCMark = "$C"
BCMarkEnd = "$CE"
BSMark = "$S"
BSMarkEnd = "$E"
BSBytesMark = 2
BSBytesLength = 3
BSBytesCheckSum = 1
BSBytesHeader = BSBytesMark + BSBytesLength

BCCInvalid = 1
BCCEchoReq = 2
BCCEchorRep = 3
BCCGetSwitches = 4
BCCGetSwitchesRep = 5
BCCGetModes = 6
BCCGetModesRep = 7
BCCGetSysInfo = 8
BCCGetSysInfoRep = 9
BCCSetSwitchState = 10

BSInvalid = 1
BSGetState = 2
BSGetStateRep = 3
BSGetTemp = 4
BSGetTempRep = 5
BSEchoRequest = 6
BSEchoReply = 7

# Bridge <-> Switch
BluetoothBridgePin = "welcome"
BluetoothAuthentificate = True
BluetoothBridgeAdress = "test"
BTSwitchMark = "AB"


BridgeCOMBaud = 9600
TCPPort = 5000

def DateTimeToUnix(dateTime):
    return time.mktime(dateTime.timetuple())

def UnixToDateTime(unix):
    return datetime.datetime.fromtimestamp(unix)

def GetFixedBool(posBo):

    if (type(posBo) == bool):
        return posBo

    if (posBo == "True" or posBo == 'True' or posBo == "true" or posBo == 'true'):
        return True
    else: 
        return False