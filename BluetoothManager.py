# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth
from GlobalStates import GlobalStates as GS
from Switch import Switch
from Switch import SwitchList
import DefinedInformation as DI
currentClientBMA = 00

buffer = []

def ReceiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print("[BT] Accepted connection from " + str(address))
  
  data = client_sock.recv(1024)
  print("[BT] received [%s]" % data)
  
  client_sock.close()
  server_sock.close()
  
def SendMessageTo(targetBluetoothMacAddress,message):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send(message)
  sock.close()
  
def SearchSwitches():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:

    # check if device could be a switch
    if bluetooth.lookup_name(bdaddr).find(DI.BTSwitchMark) <= 0:
      break;
    

    print(str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    for switch in GS.switchList:

      # check if switch already known
      if switch.address == bdaddr:
        break

      # if switch new:
      anotherSwitch = Switch(bdaddr)
      GS.switchList.raw.append(anotherSwitch)


def Start():
  SearchSwitches()

    


