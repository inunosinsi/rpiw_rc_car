import bluetooth
import machine 
import PicoMotorDriver
import utime
from ble_simple_peripheral import BLESimplePeripheral


# duty_rate: percent->u16
def convert(duty_rate):
    return int(65535*duty_rate/100)

speed = 80

board = PicoMotorDriver.KitronikPicoMotor()
#board.motorOff(1)

pwm = machine.PWM(machine.Pin(0))
pwm.freq(50)
pwm.duty_u16(convert(7.5))
# 動作確認用のコード　必要であればコメントアウトを外す
#board.motorOn(1, "f", speed)
#time.sleep(2)
#board.motorOn(1, "r", speed)
#time.sleep(2)
#board.motorOff(1)

ble = bluetooth.BLE()
p = BLESimplePeripheral(ble)

duty_rate = 7.5

def on_rx(v):
    global duty_rate
    print("received:", v)
    
    if v == b'r\r\n':
        duty_rate += 0.1
        if duty_rate > 9.0:
            duty_rate = 9.0
    elif v == b'l\r\n':
        duty_rate -= 0.1
        if duty_rate < 5.5:
            duty_rate = 5.5
    elif v == b're\r\n':
        duty_rate = 7.5
    elif v == b'f\r\n':
        board.motorOn(1, "f", speed)
    elif v == b'b\r\n':
        board.motorOn(1, "r", speed)
    elif v == b's\r\n':
        board.motorOff(1)
        
    
    pwm.duty_u16(convert(duty_rate))
       
while True:
    if p.is_connected():
        p.on_write(on_rx)

