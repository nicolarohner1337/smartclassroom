
import time
import board
import adafruit_hcsr04
import neopixel

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.SDA, echo_pin=board.SCL)
led = neopixel.NeoPixel(board.NEOPIXEL,1)
led.brightness = 0.3
initDistance = None
while not initDistance:
    try:
        initDistance = sonar.distance
    except:
        pass
print(initDistance)
while True:
    try:
        if sonar.distance > initDistance + 5:
            print("Window open")
            led[0]= (0,0,255)
        else:
            print("window closed")
            led[0]= (255,0,0)
    except RuntimeError:
        pass
    time.sleep(0.05)
