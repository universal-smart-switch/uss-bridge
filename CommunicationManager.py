import BluetoothManager
import threading
import codecs
import DefinedInformation
from MessageManager import BCMessage
from MessageManager import BCCommand

receivingMode = False

def SendMessage(deviceBMA,message):
    BluetoothManager.sendMessageTo(deviceBMA,message)

def thread_bufferValidator():
    while(receivingMode):
        possibleMarkBytes = [BluetoothManager.buffer[1], BluetoothManager.buffer[0]]
        possibleMark = codecs.decode(possibleMarkBytes, 'UTF-8')

        if (possibleMark == DefinedInformation.DefinedInformation.BSMark):

            while(len(BluetoothManager.buffer) < (DefinedInformation.DefinedInformation.BSBytesHeader)):
                # wait till length is received
                 
            lengthBytes = [BluetoothManager.buffer[4],BluetoothManager.buffere[3],BluetoothManager.buffer[2]]
            length =  int.from_bytes(lengthBytes, "big")

            while (len(BluetoothManager.buffer) < (DefinedInformation.DefinedInformation.BSBytesHeader + length) ):
                # wait till message is complete
            
            receivedMessage = BCMessage()
            receivedMessage.CreateFromRaw()
