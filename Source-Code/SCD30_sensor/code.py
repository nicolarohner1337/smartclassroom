
import time
import board
import busio
import adafruit_scd30

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import neopixel

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

uart_connection = None
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.1

while True:
    led[0] = (255, 0, 0)
    ble.start_advertising(advertisement)
    
    while not ble.connected:
        pass
   
    led[0] = (0, 255, 0)
    while ble.connected:
        if scd.data_available:
            start_timer = time.monotonic()
            co2 = []
            temperature = []
            humidity = []
            while (time.monotonic()-start_timer) < 60:
                co2.append(float(scd.CO2))
                temperature.append(float(scd.temperature))
                humidity.append(float(scd.relative_humidity))
                time.sleep(10)
            co2 = sum(co2)/len(co2)
            temperature = sum(temperature)/len(temperature)
            humidity = sum(humidity)/(len(humidity))
            uart.write("{},{},{}\n".format(round(float(co2), 1), round(float(temperature), 1), round(float(humidity), 1)))
            




