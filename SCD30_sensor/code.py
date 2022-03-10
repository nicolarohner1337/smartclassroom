# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_scd30

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import neopixel

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.1
id = "CIRCUITPY323d"
while True:
    led[0] = (255, 0, 0)

    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    led[0] = (0, 255, 0)
    while ble.connected:

        if scd.data_available:
            uart.write("{},{},{},{}\n".format(id, round(float(scd.CO2), 1), round(float(scd.temperature), 1),
                                              round(float(scd.relative_humidity), 1)))
            time.sleep(1)

while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        print("------")

        time.sleep(1)
