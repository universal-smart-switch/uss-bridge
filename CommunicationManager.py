import BluetoothManager
import threading
import codecs
import DefinedInformation
from MessageManager import BCMessage
from MessageManager import BCCommand

receivingMode = False

def SendMessage(deviceAddr,message,isAddressBluetoothAddress):
    #BluetoothManager.sendMessageTo(deviceBMA,message)
    print ('unimplemented')

def thread_bufferValidator():
    while(receivingMode):
        possibleMarkBytes = [BluetoothManager.buffer[1], BluetoothManager.buffer[0]]
        possibleMark = codecs.decode(possibleMarkBytes, 'UTF-8')

        if (possibleMark == DefinedInformation.DefinedInformation.BSMark):

            while(len(BluetoothManager.buffer) < (DefinedInformation.DefinedInformation.BSBytesHeader)):
                # wait till length is received
                print('unimplemented')
                 
            lengthBytes = [BluetoothManager.buffer[4],BluetoothManager.buffere[3],BluetoothManager.buffer[2]]
            length =  int.from_bytes(lengthBytes, "big")

            while (len(BluetoothManager.buffer) < (DefinedInformation.DefinedInformation.BSBytesHeader + length) ):
                # wait till message is complete
                print('unimplemented')
            
            receivedMessage = BCMessage()
            receivedMessage.CreateFromRaw()
