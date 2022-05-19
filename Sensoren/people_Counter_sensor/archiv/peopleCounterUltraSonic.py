import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_4_digit_display import Grove4DigitDisplay

 
def main():

    #display = Grove4DigitDisplay(12, 13, brightness=7)
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

        if len(seq) > 1 and len(seq) < 4:
            if '12' in seq or '102' in seq:
                counter+=1
                print(counter,"Personen")
                seq = ''
                time.sleep(0.5)
            if '21' in seq and  counter != 0 or '201' in seq and counter != 0:
                counter-=1
                print(counter,"Personen")
                seq = ''

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
