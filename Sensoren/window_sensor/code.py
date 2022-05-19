# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# nRF5840 D5, Grove D2
infrared = digitalio.DigitalInOut(board.D9)
infrared.direction = digitalio.Direction.INPUT
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
initDistance = None

uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
sensor_id = "CIRCUITPY7c40"

last_state = 0 if infrared.value else 1

while True:
    led[0] = (255, 0, 0)
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    led[0] = (0, 255, 0)
    time.sleep(2)
    while ble.connected:
        measurement = {1: 0, 0: 0}
        print(measurement[1])
        start_check = time.monotonic()
        while (time.monotonic() - start_check) < 2:
            measurement[int(infrared.value)] += 1
            time.sleep(0.1)
        current_state = max(measurement, key=measurement.get)
        if current_state != last_state:
            uart.write(str(current_state)+ "\n")
            last_state = current_state
            led[0] = (0,0,255)
            time.sleep(1)
            led[0] = (0,255,0)

