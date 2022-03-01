from operator import countOf
from datetime import datetime
import os
import sys
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from grove.gpio import GPIO
import certifi
 
usleep = lambda x: time.sleep(x / 1000000.0)
 
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000
 
class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio =GPIO(pin)
 
    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)
 
        self.dio.dir(GPIO.IN)
 
        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None
 
        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None
 
        t2 = time.time()
 
        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None
 
        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm
 
        return distance
 
    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist

Grove = GroveUltrasonicRanger
 
def main():
    sensor1Pin = 16
    sensor2Pin = 5
   
    sonar1 = GroveUltrasonicRanger(int(sensor1Pin))
    sonar2 = GroveUltrasonicRanger(int(sensor2Pin))
    
    counter = 0
    initDist = []
    initDist.append(int(sonar1.get_distance()))

    initDist.append(int(sonar2.get_distance()))

    seq = ''
    lastSeq = ''
    skip = False
    timeOut=0
    print('Detecting distance...')
    print("initital distance:",initDist)

    token = "JqkM8xndU1lIiRkO76gt-YZLf1FWVu-1knan1Zaek8E-Hr1E59x7wPk9UuzOLCHJVv99OpZvfYjunvP9Fn6kgw=="
    org = "nicola.rohner@students.fhnw.ch"
    bucket = "smartclassroom"
    while True:
        
        if int(sonar1.get_distance()) < initDist[0] - 30 and int(sonar2.get_distance()) < initDist[1] - 30:
            if '0' not in seq:
                seq+= '0'
            skip = True
        
        if int(sonar1.get_distance()) < initDist[0] - 30 and '1' not in seq and not skip:
            #counter += 1
            #print(counter)
            seq+= '1'

        if int(sonar2.get_distance()) < initDist[1] - 30 and '2' not in seq and not skip:
            #counter += -1
            #print(counter)
            seq+= '2'
        #TODO: handle situation where both sensors are triggered
        if len(seq) > 1 and len(seq) < 4:
            if '12' in seq or '102' in seq:
                counter+=1
                print(counter,"Personen")
                seq = ''
                with InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token, org=org,ssl_CA_cert=certifi.where()) as client:
                    write_api = client.write_api(write_options=SYNCHRONOUS)
                    data = "personCounter,sensor=ultrasonice persons={}".format(counter)
                    write_api.write(bucket, org, data)
                time.sleep(0.5)
            if '21' in seq and  counter != 0 or '201' in seq and counter != 0:
                counter-=1
                print(counter,"Personen")
                seq = ''
                with InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token, org=org,ssl_CA_cert=certifi.where()) as client:
                    write_api = client.write_api(write_options=SYNCHRONOUS)
                    data = "personCounter,sensor=ultrasonice persons={}".format(counter)
                    write_api.write(bucket, org, data)
                time.sleep(0.5)
        
        if len(seq) > 2 and '0' not in seq or len(seq) > 0 and seq[0] == '0':
            seq = ''
        
        if len(seq) > 0:
            timeOut+=1

        if timeOut > 150 and len(seq) > 0:
            print("Timeout")
            seq = ''
            timeOut = 0

        if seq != lastSeq:
            print(seq)
            lastSeq = seq
        skip = False
        time.sleep(0.01)
    
 
if __name__ == '__main__':
    main()
