# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Connect to an "eval()" service over BLE UART.
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_connection = None

def connectionSCD30(uart_connection):
    while not uart_connection:
        print("Trying to connect...")
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            if UARTService in adv.services:
                uart_connection = ble.connect(adv)
                print("Connected")
                break
        ble.stop_scan()
        

    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        return uart_service, uart_connection
    
while True:
    uart_serviceSCD30, uart_connectionSCD30 = connectionSCD30(uart_connection)
    while uart_connectionSCD30.connected:
    
        s = uart_serviceSCD30.readline().decode("utf-8")
        if s:
            print(list(map(float, s.split(','))))
            
            