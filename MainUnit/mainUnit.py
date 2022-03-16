#!/usr/bin/python3
from socket import timeout
import time
import requests
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


ble = BLERadio()
""" uart_connection1 = None
uart_connection2 = None
uart_connection3 = None """

uart_connections = {
    'CIRCUITPY323d': {'connection':None,'values':3},
    'CIRCUITPY825a': {'connection':None,'values':1},
    'CIRCUITPYbec9': {'connection':None,'values':1},
    #'CIRCUITPY7c40': {'connection':None}
}
urlApi = 'https://glusfqycvwrucp9-db202202211424.adb.eu-zurich-1.oraclecloudapps.com/ords/sensor_datalake1/sens/insert/'
headers = {"key":"Content-Type","value":"application/json","description":""}
lastApiCall = time.time()
class noConnection:
    connected = False
notTimeout = True
setTimeout = time.time()

def connection(uart_connection,complete_name):
    while not uart_connection:
        print("Trying to connect...{}".format(complete_name))
        for adv in ble.start_scan(ProvideServicesAdvertisement,timeout=10.0):
            #if longer than 10 seconds, stop trying
            
            if UARTService in adv.services:
                if complete_name == adv.complete_name:
                    uart_connection = ble.connect(adv, timeout=10.0)
                    print("Connected")
                    break   
        ble.stop_scan()
        break
        
    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        return uart_service, uart_connection
    else:
        uart_connections[complete_name]['inRange'] = False
        NoUart_connections = noConnection
        return None, NoUart_connections
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
            
    while any([uart_connections[k]['connection'].connected for k,v in uart_connections.items()]):
        #try read not readline
        if time.time() - lastApiCall > 20:
            for k,v in uart_connections.items():
                #if not all([uart_connections[k]['connection'].connected for k,v in uart_connections.items()]) and time.time() - startSending > 60:
                    #break
                try:
                    #only read if there is connection
                    #TODO read more sleep less, konstante daten, mehr kontrolle über die gelesenen daten
                    if uart_connections[k]['connection'].connected:
                        print(uart_connections[k]['service'].readline().decode("utf-8"))
                        tempList = uart_connections[k]['service'].readline().decode("utf-8").strip('\n').split(',')
                        print (tempList)
                        if uart_connections[k]['values'] == len(tempList[1:]) and k == tempList[0]:
                            print(tempList)
                            print("prepering to send")
                            # for list  with lenght > 2 call multiple post requests
                            
                            for i in range(1,len(tempList)):
                                json = {'sensor_id':tempList[0],'value1':tempList[i]}
                                print(json)
                                #send request
                                response = requests.post(urlApi,headers = headers,data=json)
                                #print response
                                print(response.status_code)
                                time.sleep(0.5)

                            lastApiCall = time.time()
                            #json['timestamp'] = time.time()
                            #send to server
                            
                    time.sleep(1)
                except KeyboardInterrupt:
                    print ('KeyboardInterrupt exception is caught')
                    #stop python script
                    exit()
        if time.time() - setTimeout > 20:
            notTimeout = True
        startReconnect = time.time()
        while notTimeout and not all([uart_connections[k]['connection'].connected for k,v in uart_connections.items()]):
            #timeout = False
            for k,v in uart_connections.items():
                if time.time() - startReconnect > 20:
                    notTimeout = False
                    setTimeout = time.time()
                    break
                elif not uart_connections[k]['connection'].connected:
                    print("We found a disconnected device{}".format(k))
                    uart_connections[k]['service'],uart_connections[k]['connection'] = connection(None,k)
                    print("Tried to Reconnected")
                    break
