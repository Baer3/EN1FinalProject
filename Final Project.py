from time import sleep
import onewire
from ds18x20 import DS18X20

pin = Pin(1)

#create the onewire object
tempSensor = DS18X20(onewire.OneWire(pin))

#scan for device addresses
roms = tempSensor.scan()

#print temperatures
for i in range(100):
    tempSensor.convert_temp()
    sleep(.5)
    for rom in roms:
        print("Temperature: " + str(tempSensor.read_temp(rom)))