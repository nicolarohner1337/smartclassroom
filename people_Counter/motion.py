#flank detection on ultra sonic sensor
#save in ring buffer
#check for flank

from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time

sonarLeft = GroveUltrasonicRanger(16)
sonarRight = GroveUltrasonicRanger(5)

def detectFlank(sonarLeft, sonarRight):
   