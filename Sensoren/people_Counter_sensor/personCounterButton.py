

import digitalio
import time
import board
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import tm1637

count_up = digitalio.DigitalInOut(board.D9)
count_down = digitalio.DigitalInOut(board.D5)
CLK = board.SCL
DIO = board.SDA
display = tm1637.TM1637(CLK, DIO)
#display.hex(0x1230)
time.sleep(5)

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
sensor_id = "CIRCUITPYbec9"
person = 0
lastPress = time.monotonic()
display.number(person)
senfFlag = True

waitAnimationList = ['-  ', ' - ', '  -',' - ']
animationIndex = 0
while True:
   
    led[0] = (255, 0, 0)
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    led[0] = (0, 255, 0)
    while ble.connected:
        #show animation
        if senfFlag:
            display.show(waitAnimationList[animationIndex])
            display.number(person)
            animationIndex = (animationIndex + 1) % len(waitAnimationList)
            time.sleep(1/20)
        if count_up.value:
            person += 1
            display.number(person)
            display.show("UP")
            time.sleep(0.2)
            display.number(person)
            lastPress = time.monotonic()
            senfFlag = True
        if count_down.value:
            #not less than 0
            if person > 0:
                person -= 1
                display.number(person)
                display.show("--")
                time.sleep(0.2)
                display.number(person)
                lastPress = time.monotonic()
                senfFlag = True
        
        if lastPress + 5 < time.monotonic() and senfFlag:
            display.show("SEND")
            time.sleep(1)
            uart.write("{}\n".format(person))
            time.sleep(1)
            display.number(person)
            senfFlag = False
        