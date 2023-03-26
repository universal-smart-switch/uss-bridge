import NetworkManager
import time
import SettingsManager as SM
import ModeExecutor
#import BluetoothManager


SM.LoadSettings()
#BluetoothManager.startUp()         # vllcht zuerst threads dann async wichtig vllcht idk
ModeExecutor.Start()
NetworkManager.Start()
    
  
