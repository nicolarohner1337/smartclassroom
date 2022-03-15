import board
import digitalio
import neopixel

motion_sensor = digitalio.DigitalInOut(board.A0) # nRF52840, Grove D2
motion_sensor.direction = digitalio.Direction.INPUT

led = neopixel.NeoPixel(board.NEOPIXEL, 1)

print(motion_sensor.value)

while True:
    if motion_sensor.value:
        led[0] = (0,255,0)
    else:
        led[0] = (255,0,0)