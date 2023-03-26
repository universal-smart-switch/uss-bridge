import os
import sys
import struct
import bluetooth._bluetooth as bluez

def find_Smartswitch_devices():
    devices = []
    for i in range(255):
        address = "00:00:00:00:00:" + "{:02x}".format(i)
        try:
            result = bluez.hci_inquiry(address, duration=8, limit=1)
        except:
            print("Inquiry Error")
            continue
        if len(result) == 0:
            continue
        for (address, name) in result:
            if "Smartswitch-" in name:
                devices.append((address, name))
    return devices

def read_device_UUID(address, uuid):
    try:
        sock = bluez.hci_open_dev(bluez.hci_get_route(address))
    except:
        print("Error accessing device")
        return None

    service_matches = bluez.find_service(address, uuid=uuid)
    if len(service_matches) == 0:
        print("Couldn't find the service")
        return None

    first_match = service_matches[0]
    attrs = bluez.find_attributes(first_match["handle"], uuid=uuid)
    if len(attrs) == 0:
        print("Couldn't find the UUID")
        return None

    value = attrs[0]["value"]
    return struct.unpack("<h", value)[0]

def set_device_UUID(address, uuid, value):

    try:
        sock = bluez.hci_open_dev(bluez.hci_get_route(address))
    except:
        print("Error accessing device")
        return False

    service_matches = bluez.find_service(address, uuid=uuid)
    if len(service_matches) == 0:
        print("Couldn't find the service")
        return False

    first_match = service_matches[0]
    attrs = bluez.find_attributes(first_match["handle"], uuid=uuid)
    if len(attrs) == 0:
        print("Couldn't find the UUID")
        return False

    bluez.write_attribute(attrs[0]["handle"], struct.pack("<h", value))
    return True

find_Smartswitch_devices()