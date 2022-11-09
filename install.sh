#!/bin/bash

installBluetoothApt=`sudo apt-get install bluetooth bluez libbluetooth-dev`
installBluetoothPIP=`sudo python3 -m pip install pybluez`

echo $installBluetoothApt
echo $installBluetoothPIP