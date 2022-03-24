# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_hcsr04
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising import Advertisement


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
sensor_id = "CIRCUITPY825a"
initDistance = []
while not initDistance:
    try:
        while len(initDistance) < 5:
            initDistance.append(sonar.get_distance())
            print(initDistance)
            time.sleep(0.1)
    except:
        pass

initDistance = sum(initDistance)/len(initDistance)

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
            temp = []
            while len(temp) < 3:
                temp.append(sonar.get_distance())
            temp = sum(temp)/len(temp)
            if temp > initDistance + 5:
                if num == "0":
                    led[0]=(0,0,255)
                    time.sleep(0.5)
                    num = "1"
                    uart.write(num + "\n")
                    print(num, temp)

                led[0]=(0,255,0)
            else:
                if num == "1":
                    led[0]= (255,255,0)
                    time.sleep(0.5)
                    num = "0"
                    uart.write(num + "\n")
                    print(num, temp)

                led[0]= (0,255,0)

            time.sleep(1.0)

        except:
            uart.write(num + "\n")
            time.sleep(1.0)
            print(sensor_id, num)
            pass
        time.sleep(4.0)


