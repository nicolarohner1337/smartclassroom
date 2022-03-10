# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_hcsr04
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# nRF5840 D5, Grove D2
sonar = adafruit_hcsr04.GroveUltrasonicRanger(board.SCL)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
initDistance = None

uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
num = "0"
sensor_id = "1"

while not initDistance:
    try:
        initDistance = sonar.get_distance()
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

            if sonar.get_distance() > initDistance + 5:
                if num == "0":
                    led[0]=(0,0,255)
                    time.sleep(0.5)
                    num = "1"

                led[0]=(0,255,0)
            else:
                if num == "1":
                    led[0]= (255,255,0)
                    time.sleep(0.5)
                    num = "0"
                led[0]= (0,255,0)
            uart.write(sensor_id + "," + num + "\n")
            print(sensor_id, num, sonar.get_distance())
        except RuntimeError:
            uart.write(sensor_id + ","+ num + "\n")
            print(sensor_id, num)
            pass
        time.sleep(0.5)


