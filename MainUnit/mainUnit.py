#!/usr/bin/python3
from socket import timeout
import time
import requests
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


ble = BLERadio()



uart_connections = {
    'CIRCUITPY323d': {'connection':None,'values':3,'units':['PPM','C','%'],'timeoutDuration':0,'notTimeout':True,'timeoutStart':time.time(),'lastValues':[]},
    'CIRCUITPY825a': {'connection':None,'values':1, 'units':['Window'],'timeoutDuration':0,'notTimeout':True,'timeoutStart':time.time(),'lastValues':[]},
    'CIRCUITPYbec9': {'connection':None,'values':1, 'units':['Window'],'timeoutDuration':0,'notTimeout':True,'timeoutStart':time.time(),'lastValues':[]}
    #'CIRCUITPY7c40': {'connection':None}
}
urlApi = 'https://glusfqycvwrucp9-db202202211424.adb.eu-zurich-1.oraclecloudapps.com/ords/sensor_datalake1/sens/insert/'
headers = {"key":"Content-Type","value":"application/json","description":""}
lastApiCall = time.time()
class noConnection:
    connected = False
notTimeout = True
setTimeout = time.time()
#delete because move this to the connections dictionary
#timeoutDuration = 60
timeoutDurationSteps = [30,60,120,240,480,600,1200,1800]
def connection(uart_connection,complete_name):
    while not uart_connection:
        print("Trying to connect...{}".format(complete_name))
        for adv in ble.start_scan(ProvideServicesAdvertisement,timeout=10.0):
            #if longer than 10 seconds, stop trying
            if UARTService in adv.services:
                try:
                    #try to connect with specific device
                    if complete_name == adv.complete_name:
                        uart_connection = ble.connect(adv, timeout=10.0)
                        print("Connected")
                        break
                except:
                    print("Connection timed out")
                    break
        ble.stop_scan()
        break
        
    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        return uart_service, uart_connection
    else:
        #is this really needed?
        #uart_connections[complete_name]['inRange'] = False
        NoUart_connections = noConnection
        print("Failed to connect with {}".format(complete_name))
        return None, NoUart_connections
#check if connection is true
for k,v in uart_connections.items():
    uart_connections[k]['service'],uart_connections[k]['connection'] = connection(v['connection'],k)


while True:
    #initialize all connections
    for k,v in uart_connections.items():
        try:
            if  not v['connection'].connected:
                uart_connections[k]['service'],uart_connections[k]['connection'] = connection(None,k)
        except:
            pass
   
    while any([uart_connections[k]['connection'].connected for k,v in uart_connections.items()]):
        #TODO try read not readline
        if time.time() - lastApiCall > 20:
            for k,v in uart_connections.items():
                #if not all([uart_connections[k]['connection'].connected for k,v in uart_connections.items()]) and time.time() - startSending > 60:
                    #break
                try:
                    #only read if there is connection
                    #TODO read more sleep less, konstante daten, mehr kontrolle über die gelesenen daten
                    if uart_connections[k]['connection'].connected:
                        tempList = uart_connections[k]['service'].readline()
                        tempList = tempList.decode('utf-8').strip('\n').split(',')
                        if uart_connections[k]['values'] == len(tempList):
                            print(tempList)
                            print("prepering to send")
                            # for list  with lenght > 2 call multiple post requests
                            
                            for i in range(len(tempList)):
                                json = {'sensor_id':k,'value1':tempList[i],'unit1':uart_connections[k]['units'][i-1]}
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
        #check for any timeouts that exceed the set timeoutDuration
        for k,v in uart_connections.items():
            if time.time() - uart_connections[k]['timeoutStart'] > uart_connections[k]['timeoutDuration']:
                uart_connections[k]['notTimeout'] = True
    
        while any([uart_connections[k]['notTimeout'] for k,v in uart_connections.items()]) and not all([uart_connections[k]['connection'].connected for k,v in uart_connections.items()]):
            #BUG infinity loop in case of no connection
            for k,v in uart_connections.items():
                if not uart_connections[k]['connection'].connected:
                    print("We found a disconnected device {}".format(k))
                    uart_connections[k]['service'],uart_connections[k]['connection'] = connection(None,k)
                    uart_connections[k]['notTimeout'] = False
                    uart_connections[k]['timeoutStart'] = time.time()
                    #set next timeoutDuration
                    if uart_connections[k]['timeoutDuration'] == 0:
                        uart_connections[k]['timeoutDuration'] = timeoutDurationSteps[0]
                    else:
                        #find index of current timeoutDuration
                        index = timeoutDurationSteps.index(uart_connections[k]['timeoutDuration'])
                        #if index is not the last index, set next timeoutDuration
                        if index < len(timeoutDurationSteps)-1:
                            uart_connections[k]['timeoutDuration'] = timeoutDurationSteps[index+1]
                    #Reset the timeoutDuration for reconnected Devices
                    if uart_connections[k]['connection'].connected:
                        uart_connections[k]['timeoutDuration'] = 0
                else:
                    #for connected devices set not Timeout to false to exit the while loop
                    uart_connections[k]['notTimeout'] = False
