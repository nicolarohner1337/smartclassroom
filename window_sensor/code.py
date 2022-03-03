import time
import board
import adafruit_hcsr04
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.SDA, echo_pin=board.SCL)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
initDistance = None

uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
while True:
    led[0] = (255, 0, 0)

    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    led[0] = (0, 255, 0)
    while ble.connected:
        while not initDistance:
            try:
                initDistance = sonar.distance
            except:
                pass
        print(initDistance)
        while True:
            try:
                if sonar.distance > initDistance + 5:
                    uart.write("1")
                    led[0] = (0, 0, 255)
                else:
                    uart.write("0")
                    led[0] = (255, 0, 0)
            except RuntimeError:
                pass
            time.sleep(0.05)
