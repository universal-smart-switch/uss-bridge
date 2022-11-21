import datetime
import time

BCMark = "$C"
BCMarkEnd = "$CE"
BSMark = "$S"



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

BluetoothBridgePin = "welcome"
BluetoothAuthentificate = True
BluetoothBridgeAdress = "test"

BridgeCOMBaud = 9600
TCPPort = 5000

def DateTimeToUnix(dateTime):
    return time.mktime(dateTime.timetuple())

def UnixToDateTime(unix):
    return datetime.datetime.fromtimestamp(unix)
