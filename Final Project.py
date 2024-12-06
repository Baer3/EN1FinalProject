from s2pico_oled import OLED
from machine import Pin, I2C
import ssd1306
from time import sleep
import onewire
from ds18x20 import DS18X20

pin = Pin(1, Pin.IN())
button1 = Pin(33, Pin.IN())
button2 = Pin(34, Pin.IN())
button3 = Pin(35, Pin.IN())
button4 = Pin(36, Pin.IN())
button5 = Pin(37, Pin.IN())
go = Pin(38, Pin.IN())
degreesC = 0
degreesF = 0
start = 0
time = 0 #in seconds
BLACK_TEMP = 100
GREEN_TEMP = 82
OOLONG_TEMP = 90
HERBAL_TEMP = 100
MENU1 = "Tea Type:\n(1) Black, (2) Green, (3) Oolong, (4) Herbal, (5) Other/Custom"
MENU_BLACK = "Black Tea:\nRecomended Temperature: 212F/100C, Recomended Time: 3-5 minutes\n"
             + "Use Recomended Settings? (1) Yes, (2) No, (5) Back"
MENU_TEMP = "Please place temperature probe in the water.\n(1) Continue, (2) Skip, (5) Back"
MENU_TEMP2 = "Reading Temperature..."
MENU_COLD = "Water is cold. Please heat the water.\n(1) Continue, (5) Back"
MENU_CUSTOM = "Please input desired brew time:\n"
stage = '0'
teaType = '0'
idealTemp = 0

i2c_ext = I2C(1, sda=Pin(38), scl=Pin(37))

oled_ext = ssd1306.SSD1306_I2C(128, 64, i2c_ext)

oled_ext.fill(0)

#create the onewire object
tempSensor = DS18X20(onewire.OneWire(pin))

#scan for device addresses
roms = tempSensor.scan()

def menu():
    if stage == '0':
        oled_ext.fill(0)
        oled_ext.text(MENU1, 40, 30)
        oled_ext.show()
        sleep(.5)
        if button1.value() == 1:
            teaType = 'b'
            stage = '1'
            idealTemp = BLACK_TEMP
        if button2.value() == 1:
            teaType = 'g'
            stage = '1'
            idealTemp = GREEN_TEMP
        if button3.value() == 1:
            teaType = 'o'
            stage = '1'
            idealTemp = OOLONG_TEMP
        if button4.value() == 1:
            teaType = 'h'
            stage = '1'
            idealTemp = HERBAL_TEMP
        elif button5.value() == 1:
            stage = 'custom'
            
            
            
    if stage == '1'
        if teaType == 'b':
            oled_ext.text(MENU_BLACK, 40, 30)
        elif teaType == 'g':
            oled_ext.text(MENU_GREEN, 40, 30)
        elif teaType == 'o':
            oled_ext.text(MENU_OOLONG, 40, 30)
        elif teaType == 'h':
            oled_ext.text(MENU_HERBAL, 40, 30)
        oled_ext.show()
        sleep(.5)
        if button1.value() == 1:
            stage = '2'
        elif button2.value() == 1:
            stage = 'custom'
        elif button5.value() == 1:
            stage = '0'
            
            
            
    if stage == '2'
        oled_ext.text(MENU_TEMP, 40, 30)
        oled_ext.show()
        sleep(.5)
        if button1.value() == 1:
            stage = '3'
        elif button2.value() == 1:
            degreesC = 0
            degreesF = 0
            stage = 'custom'
        elif button5.value() == 1:
            stage = '1'
            
            
            
    if stage == '3'
        oled_ext.text(MENU_TEMP2, 40, 30)
        oled_ext.show()
        sleep(.5)
        degreesC = readTemps()
        degreesF = (degreesC * (9/5)) + 32
        if degreesC < 50:
            stage = 'cold'
            break
        elif teaType == 'b':
            if degreesC - 50 > (idealTemp - 50) * (2/3):
                time = 180
            elif degreeC - 50 > (idealTemp - 50) * (1/3):
                time = 240
            else
                time = 300
        elif teaType == 'g':
            if degreesC - 50 > (idealTemp - 50) * (1/2):
                time = 60
            else
                time = 120
        elif teaType == 'o':
            if degreesC - 50 > (idealTemp - 50) * (1/2):
                time = 120
            else
                time = 180
        elif teaType == 'h':
            if degreesC - 50 > (idealTemp - 50) * (5/6):
                time = 300
            elif degreesC - 50 > (idealTemp - 50) * (4/6):
                time = 360
            elif degreesC - 50 > (idealTemp - 50) * (3/6):
                time = 420
            elif degreesC - 50 > (idealTemp - 50) * (2/6):
                time = 480
            elif degreesC - 50 > (idealTemp - 50) * (1/6):
                time = 540
            else
                time = 600
        oled_ext.text("Temperature: " + str(degreesC) + "C/" + str(degreesF) + "F\n"
                      + "Recomended Time: " + str(time/60) + " minutes\n(1) Start, (2) Back", 40, 30)
        oled_ext.show()
        sleep(.5)
        if button1.value() == 1:
            stage = 'brew'
        elif button5.value == 1:
            stage = '2'
            
            
            
    if stage == 'cold'
        oled_ext.text(MENU_COLD, 40, 30)
        oled_ext.show()
        sleep(.5)
        if button1.value() == 1:
            stage = '3'
        elif button5.value() == 1:
            stage = '2'
            
            
            
    if stage == 'custom'
        oled_ext.text(MENU_CUSTOM + "Time: " + str(time/60) + "\n"
                      + "(1) +1 Minute, (2) +2 Minutes, (3) +5 Minutes, (4) Continue, (5) Back", 40, 30)
        oled_ext.show()
        sleep(.5)
        if button1.value() == 1:
            time += 60
        elif button2.value() == 1:
            time += 120
        elif button3.value() == 1:
            time += 300
        elif button4.value() == 1:
            stage = 'brew'
        elif button5.value() == 1:
            stage = '0'


                
def brew(time):

#print temperatures
def readTemps():
    temps = 0
    sleep(5)
    for i in range(10):
        tempSensor.convert_temp()
        sleep(.5)
        for rom in roms:
            temps += int(tempSensor.read_temp(rom))
        temps /= 10
        return temps
    
while True:
    menu()