# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Connect to an "eval()" service over BLE UART.
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_connection1 = None
uart_connection2 = None

def connection(uart_connection,complete_name):
    while not uart_connection:
        print("Trying to connect...{}".format(complete_name))
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            if UARTService in adv.services:
                if complete_name == adv.complete_name:
                    uart_connection = ble.connect(adv, timeout=10000)
                    print("Connected")
                    break
        ble.stop_scan()
        

    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        return uart_service, uart_connection
uart_serviceSCD30, uart_connectionSCD30 = connection(uart_connection1,'CIRCUITPY323d')
uart_servicewindow1, uart_connection_window1 = connection(uart_connection2,'CIRCUITPYaa83')    
while True:
    if not uart_connectionSCD30.connected:
        uart_serviceSCD30, uart_connectionSCD30 = connection(uart_connection1,'CIRCUITPY323d')
    
    if not uart_connection_window1.connected:
        uart_servicewindow1, uart_connection_window1 = connection(uart_connection2,'CIRCUITPYaa83')
  
    while uart_connectionSCD30.connected and uart_connection_window1.connected:
    
        s = uart_serviceSCD30.readline().decode("utf-8")
        t = uart_servicewindow1.readline().decode("utf-8")
        if s and t:
            print(s)
            print(t)
            
            