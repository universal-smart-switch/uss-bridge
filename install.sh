#!/bin/bash

installBluetoothApt=`sudo apt-get install bluetooth bluez libbluetooth-dev`
installBluetoothPIP=`sudo python3 -m pip install pybluez`
installHaikunator=`pip install haikunator`

echo $installBluetoothApt
echo $installBluetoothPIP
echo $installHaikunator