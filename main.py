import NetworkManager
import time
import SettingsManager as SM
import ModeExecutor
import BluetoothManager

if __name__ == '__main__':
    SM.LoadSettings()
    ModeExecutor.Start()
    NetworkManager.Start()
    
    BluetoothManager.Start()
