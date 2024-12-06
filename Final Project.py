from machine import Pin
from time import sleep

# You'll need to make sure the thermocouple.py library is copied to your ESP32
from thermocouple import MAX31855 

# Now initialize the thermocouple object with the correct pins
# Change the pin numbers to match your setup
therm = MAX31855(cs=Pin(37), sck=Pin(38), so=Pin(36))