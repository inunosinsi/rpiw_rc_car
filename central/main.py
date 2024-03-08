import bluetooth
import time
from ble_simple_central import BLESimpleCentral
from KitronikPicoMiniController import *

ble = bluetooth.BLE()
central = BLESimpleCentral(ble)

controller = MiniController()

not_found = False

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found peripheral:", addr_type, addr, name)
        central.connect()
    else:
        not_found = True
        print("No peripheral found.")

central.scan(callback=on_scan)

# 今回はon_rxは不要
#def on_rx(v):
    # do nothing
    
#central.on_notify(on_rx)

is_connect = True
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        is_connect = False
        break

if is_connect:
    print("Connected")
    
    with_response = False
    
    central.write("l\r\n", with_response)
    time.sleep(1)
    central.write("r\r\n", with_response)
    time.sleep(1)

    while central.is_connected():
        try:
            if controller.Left.pressed():
                central.write("l\r\n", with_response)
            if controller.Right.pressed():
                central.write("r\r\n", with_response)
            if controller.Up.pressed():
                central.write("f\r\n", with_response)
            if controller.Down.pressed():
                central.write("b\r\n", with_response)
            if controller.A.pressed():
                central.write("re\r\n", with_response)
            if controller.B.pressed():
                central.write("s\r\n", with_response)
        except:
            time.sleep_ms(10)
            #print("TX failed")
        

    print("Disconnected")
