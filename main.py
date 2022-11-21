import NetworkManager
import time
import SettingsManager as SM
#import BluetoothManager

if __name__ == '__main__':
    SM.LoadSettings()
    NetworkManager.Start()
    #BluetoothManager.Start()
