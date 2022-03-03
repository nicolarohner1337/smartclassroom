# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_hcsr04
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.SDA, echo_pin=board.SCL)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
initDistance = None

uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
num = "0"

while not initDistance:
    try:
        initDistance = sonar.distance
    except:
        pass
print(initDistance)

while True:
    led[0] = (255, 0, 0)
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    led[0] = (0, 255, 0)
    while ble.connected:
        try:

            if sonar.distance > initDistance + 5:
                num = "1"

                # led[0]= (0,0,255)
            else:
                num = "0"

                # led[0]= (255,0,0)
            uart.write(num)
        except RuntimeError:
            uart.write(num)
            pass
        time.sleep(0.5)