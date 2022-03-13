import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_4_digit_display import Grove4DigitDisplay

""" from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS """


 
 
def main():
    """  count = 0
        t = time.strftime("%H%M", time.localtime(time.time()))
        display.show(t)
        display.set_colon(count & 1)
        count += 1
    """

    display = Grove4DigitDisplay(12, 13, brightness=7)
    sonar1 = GroveUltrasonicRanger(16)
    sonar2 = GroveUltrasonicRanger(5)
    
    counter = 0
    initDist = []
    initDist.append(int(sonar1.get_distance()))

    initDist.append(int(sonar2.get_distance()))
    noise = 20
    seq = ''
    lastSeq = ''
    skip = False
    timeOut=0
    print('Detecting distance...')
    print("initital distance:",initDist)

    #Show initial distance
    display.show(initDist[0])
    time.sleep(1)
    display.show('----')
    time.sleep(1)
    display.show(initDist[1])
    time.sleep(1)
    display.show(counter)

    """ token = "JqkM8xndU1lIiRkO76gt-YZLf1FWVu-1knan1Zaek8E-Hr1E59x7wPk9UuzOLCHJVv99OpZvfYjunvP9Fn6kgw=="
    org = "nicola.rohner@students.fhnw.ch"
    bucket = "smartclassroom" """
    while True:
        
        if int(sonar1.get_distance()) < initDist[0] - noise and int(sonar2.get_distance()) < initDist[1] - 30:
            if '0' not in seq:
                seq+= '0'
            skip = True
        
        if int(sonar1.get_distance()) < initDist[0] - noise and '1' not in seq and not skip:
            seq+= '1'
            skip =True

        if int(sonar2.get_distance()) < initDist[1] - noise and '2' not in seq and not skip:
            seq+= '2'
        #TODO: handle situation where both sensors are triggered
        if len(seq) > 1 and len(seq) < 4:
            if '12' in seq or '102' in seq:
                counter+=1
                print(counter,"Personen")
                seq = ''
                display.show(counter)
                """ with InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token, org=org,ssl_CA_cert=certifi.where()) as client:
                    write_api = client.write_api(write_options=SYNCHRONOUS)
                    data = "personCounter,sensor=ultrasonice persons={}".format(counter)
                    write_api.write(bucket, org, data) """
                time.sleep(0.5)
            if '21' in seq and  counter != 0 or '201' in seq and counter != 0:
                counter-=1
                print(counter,"Personen")
                seq = ''
                display.show(counter)
                """ with InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token, org=org,ssl_CA_cert=certifi.where()) as client:
                    write_api = client.write_api(write_options=SYNCHRONOUS)
                    data = "personCounter,sensor=ultrasonice persons={}".format(counter)
                    write_api.write(bucket, org, data) """
                time.sleep(0.5)
        
        if len(seq) > 2 and '0' not in seq or len(seq) > 0 and seq[0] == '0':
            seq = ''
        
        if len(seq) > 0:
            timeOut+=1

        if timeOut > 100 and len(seq) > 0:
            print("Timeout")
            seq = ''
            timeOut = 0

        if seq != lastSeq:
            print(seq)
            lastSeq = seq
        skip = False
        time.sleep(0.05)
    
if __name__ == '__main__':
    main()
