#!/usr/bin/python3
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


ble = BLERadio()
""" uart_connection1 = None
uart_connection2 = None
uart_connection3 = None """

uart_connections = {
    'CIRCUITPY323d': {'connection':None},
    'CIRCUITPY825a': {'connection':None},
    'CIRCUITPYbec9': {'connection':None},
    'CIRCUITPY7c40': {'connection':None}
}


def connection(uart_connection,complete_name):
    start = time.time()
    while not uart_connection:
        print("Trying to connect...{}".format(complete_name))
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            #if longer than 30 seconds, stop trying
            if time.time() - start > 10:
                break
            
            elif UARTService in adv.services:
                if complete_name == adv.complete_name:
                    uart_connection = ble.connect(adv, timeout=50)
                    print("Connected")
                    break   
        ble.stop_scan()
        break
        
    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        return uart_service, uart_connection.connected
    else:
        uart_connections[complete_name]['inRange'] = False
        return None, None
#check if connection is true
for k,v in uart_connections.items():
    uart_connections[k]['service'],uart_connections[k]['connection'] = connection(v['connection'],k)


while True:
    for k,v in uart_connections.items():
        try:
            if  not v['connection'] and uart_connections[k].get('inRange',True):
                uart_connections[k]['service'],uart_connections[k]['connection'] = connection(None,k)
        except:
            pass
    """ if not uart_connectionSCD30.connected:
        uart_serviceSCD30, uart_connectionSCD30 = connection(uart_connection1,'CIRCUITPY323d')
    
    if not uart_connection_window1.connected:
        uart_servicewindow1, uart_connection_window1 = connection(uart_connection2,'CIRCUITPY825a')
  
    if not uart_connection_window2.connected:
            uart_servicewindow2, uart_connection_window2 = connection(uart_connection3,'CIRCUITPYbec9') """
            
    while any([uart_connections[k]['connection'] for k,v in uart_connections.items()]):
        #try read not readline

        for k,v in uart_connections.items():
            try:
                print(uart_connections[k]['service'].readline().decode("utf-8"))
                time.sleep(1)
            except KeyboardInterrupt:
                print ('KeyboardInterrupt exception is caught')
                #stop python script
                exit()
