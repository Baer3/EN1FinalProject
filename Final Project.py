#import libraries
from s2pico_oled import OLED
from machine import Pin, I2C, PWM
import ssd1306
from time import sleep
import time
import onewire
from ds18x20 import DS18X20
import math

#assign pins to devices
thermocouplePin = Pin(1, Pin.IN, Pin.PULL_UP)
servo_bob = PWM(Pin(2), freq=50)
servo_drop = PWM(Pin(3), freq=50)
button1 = Pin(34, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(35, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(36, Pin.IN, Pin.PULL_DOWN)
button4 = Pin(37, Pin.IN, Pin.PULL_DOWN)
button5 = Pin(38, Pin.IN, Pin.PULL_DOWN)

#define variables and constants
degreesC = 0
t = 0 #in seconds
BLACK_TEMP = 100
GREEN_TEMP = 82
OOLONG_TEMP = 90
HERBAL_TEMP = 100
menuX = 120
stage = '0'
teaType = ''
idealTemp = 0

#set up and clear external oled
i2c = I2C(0, sda=Pin(13), scl=Pin(12))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)

#create the onewire object
tempSensor = DS18X20(onewire.OneWire(thermocouplePin))

#scan for device addresses
roms = tempSensor.scan()

#find average temperature over 5 seconds
#delay by 5 seconds to allow the thermocouple to warm up in the water
def readTemps():
    temps = 0
    sleep(5)
    for i in range(10):
        tempSensor.convert_temp()
        sleep(.5)
        for rom in roms:
            temps += round(tempSensor.read_temp(rom), 2)
    temps /= 10
    return temps

#reset scrolling menu location
#and delay menu switch to allow user time to press and release the buttons
def menuSwitch(x):
    x = 120
    sleep(.5)
    return x

while True:
    oled.fill(0)
    #constantly scroll certain menu items
    menuX -= 1
    if menuX < - 200:
        menuX = 120
    
    #display tea type selection menu
    #and take user input through buttons
    if stage == '0':
        oled.fill(0)
        servo_bob.duty(70)
        servo_drop.duty(70)
        oled.text("Tea Type:", 0, 0)
        oled.text("(1) Black", 0, 10)
        oled.text("(2) Green", 0, 20)
        oled.text("(3) Oolong", 0, 30)
        oled.text("(4) Herbal", 0, 40)
        oled.text("(5) Other/Custom", 0, 50)
        oled.show()
        if button1.value() == 1:
            teaType = 'b'
            stage = '1'
            idealTemp = BLACK_TEMP
            menuX = menuSwitch(menuX)
        elif button2.value() == 1:
            teaType = 'g'
            stage = '1'
            idealTemp = GREEN_TEMP
            menuX = menuSwitch(menuX)
        elif button3.value() == 1:
            teaType = 'o'
            stage = '1'
            idealTemp = OOLONG_TEMP
            menuX = menuSwitch(menuX)
        elif button4.value() == 1:
            teaType = 'h'
            stage = '1'
            idealTemp = HERBAL_TEMP
            menuX = menuSwitch(menuX)
        elif button5.value() == 1:
            t = 0
            stage = 'custom'
            menuX = menuSwitch(menuX)


    #display "recommended settings" menu depending on tea type
    #and take user input through buttons
    if stage == '1':
        oled.fill(0)
        if teaType == 'b':
            oled.text("Black Tea:", 0, 0)
            oled.text("100C, 3-5 mins", 0, 10)
            oled.text("Use Recommended Settings?", menuX, 20)
            oled.text("(1) Yes", 0, 30)
            oled.text("(2) No", 0, 40)
            oled.text("(5) Cancel", 0, 50)
        elif teaType == 'g':
            oled.text("Green Tea:", 0, 0)
            oled.text("82C, 1-2 mins", 0, 10)
            oled.text("Use Recommended Settings?", menuX, 20)
            oled.text("(1) Yes", 0, 30)
            oled.text("(2) No", 0, 40)
            oled.text("(5) Cancel", 0, 50)
        elif teaType == 'o':
            oled.text("Oolong Tea:", 0, 0)
            oled.text("90C, 2-3 mins", 0, 10)
            oled.text("Use Recommended Settings?", menuX, 20)
            oled.text("(1) Yes", 0, 30)
            oled.text("(2) No", 0, 40)
            oled.text("(5) Cancel", 0, 50)
        elif teaType == 'h':
            oled.text("Herbal Tea:", 0, 0)
            oled.text("100C, 5-10 mins", 0, 10)
            oled.text("Use Recommended Settings?", menuX, 20)
            oled.text("(1) Yes", 0, 30)
            oled.text("(2) No", 0, 40)
            oled.text("(5) Cancel", 0, 50)
        oled.show()
        if button1.value() == 1:
            stage = '2'
            menuX = menuSwitch(menuX)
        elif button2.value() == 1:
            t = 0
            stage = 'custom'
            menuX = menuSwitch(menuX)
        elif button5.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)


    #prompt user to put the thermocouple in the water
    #and take user input through buttons
    if stage == '2':
        oled.fill(0)
        oled.text("Put temperature", 0, 0)
        oled.text("probe in water.", 0, 10)
        oled.text("(1) Continue", 0, 20)
        oled.text("(2) Skip", 0, 30)
        oled.text("(5) Back", 0, 40)
        oled.show()
        if button1.value() == 1:
            stage = '3'
            menuX = menuSwitch(menuX)
        elif button2.value() == 1:
            degreesC = 0
            t = 0
            stage = 'custom'
            menuX = menuSwitch(menuX)
        elif button5.value() == 1:
            stage = '1'
            menuX = menuSwitch(menuX)


    #read the temperature of the water
    #and determine the ideal time based on the tea type, ideal temperature, and temperature of the water
    if stage == '3':
        oled.fill(0)
        oled.text("Reading", 0, 0)
        oled.text("Temperature...", 0, 10)
        oled.show()
        degreesC = readTemps() + 50
        if degreesC < 50:
            stage = 'cold'
        else:
            if teaType == 'b':
                if degreesC - 50 > (idealTemp - 50) * (2/3):
                    t = 180
                elif degreesC - 50 > (idealTemp - 50) * (1/3):
                    t = 240
                else:
                    t = 300
            elif teaType == 'g':
                if degreesC - 50 > (idealTemp - 50) * (1/2):
                    t = 60
                else:
                    t = 120
            elif teaType == 'o':
                if degreesC - 50 > (idealTemp - 50) * (1/2):
                    t = 120
                else:
                    t = 180
            elif teaType == 'h':
                if degreesC - 50 > (idealTemp - 50) * (5/6):
                    t = 300
                elif degreesC - 50 > (idealTemp - 50) * (4/6):
                    t = 360
                elif degreesC - 50 > (idealTemp - 50) * (3/6):
                    t = 420
                elif degreesC - 50 > (idealTemp - 50) * (2/6):
                    t = 480
                elif degreesC - 50 > (idealTemp - 50) * (1/6):
                    t = 540
                else:
                    t = 600
            stage = '4'


    #display ideal time and prompt start
    #and take user input through buttons
    if stage == '4':
        oled.text("Temp: " + str(degreesC) + "C", 0, 0)
        oled.text("Time: " + str(int(t/60)) + " minutes", 0, 10)
        oled.text("(1) Start", 0, 20)
        oled.text("(5) Back", 0, 30)
        oled.show()
        if button1.value() == 1:
            stage = 'brew'
            menuX = menuSwitch(menuX)
            endTime = time.time() + t
            servo_drop.duty(25)
        elif button5.value() == 1:
            stage = '2'
            menuX = menuSwitch(menuX)


    #prompt user to heat water if it is below 50C
    #and take user input through buttons
        #note: if the water is below 50C the machine will never progress to brewing
        #unless the temperature is manually adjusted in the code
    if stage == 'cold':
        oled.fill(0)
        oled.text("Water is cold.", 0, 0)
        oled.text("Heat the water.", 0, 10)
        oled.text("(1) Again", 0, 20)
        oled.text("(5) Back", 0, 30)
        oled.show()
        if button1.value() == 1:
            stage = '3'
            menuX = menuSwitch(menuX)
        elif button5.value() == 1:
            stage = '2'
            menuX = menuSwitch(menuX)
      
      
    #display the menu to input a custom time
    #and take user input through buttons
    if stage == 'custom':
        oled.fill(0)
        oled.text("Input time:", 0, 0)
        oled.text("Time: " + str(math.floor(t/60)), 0, 10)
        oled.text("(1) +1 Minute", 0, 20)
        oled.text("(2) +2 Minutes", 0, 30)
        oled.text("(3) +5 Minutes", 0, 40)
        oled.text("(4) Continue, (5) Back", menuX, 50)
        oled.show()
        if button1.value() == 1:
            t += 60
            menuX = menuSwitch(menuX)
        elif button2.value() == 1:
            t += 120
            menuX = menuSwitch(menuX)
        elif button3.value() == 1:
            t += 300
            menuX = menuSwitch(menuX)
        elif button4.value() == 1:
            stage = 'brew'
            menuX = menuSwitch(menuX)
            endTime = time.time() + t
            servo_drop.duty(25)
        elif button5.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)


    #display a brewing timer, drop the tea bag into the water and move it up and down
    #and take user input through buttons
    if stage == 'brew':
        oled.fill(0)
        while endTime > time.time():
            menuX -= 1
            if menuX < - 500:
                menuX = 120
            remainingTime = endTime - time.time()
            oled.fill(0)
            oled.text("Time Remaining:", 0, 0)
            oled.text(str(math.floor(remainingTime / 60)) + " Min " + str(remainingTime % 60) + " Sec", 0, 10)
            oled.text("(1) Pause", 0, 20)
            oled.text("(5) Cancel", 0, 30)
            oled.show()
            if remainingTime % 2 == 0:
                servo_bob.duty(125)
            else:
                servo_bob.duty(50)
                
            if button1.value() == 1:
                stage = 'pause'
                servo_bob.duty(50)
                menuX = menuSwitch(menuX)
                break
            elif button5.value() == 1:
                stage = '0'
                servo_bob.duty(50)
                menuX = menuSwitch(menuX)
                break
        if stage == 'brew':
            stage = 'fin'
            servo_bob.duty(50)


    #pause the tea bag movement and display the remaining brewing time
    #and take user input through buttons
        #note: the tea bag will still be in the water despite the timer being paused
    if stage == 'pause':
        oled.fill(0)
        oled.text("Brewing Paused.", 0, 0)
        oled.text(str(math.floor(remainingTime / 60)) + " Min " + str(remainingTime % 60) + " Sec", 0, 10)
        oled.text("(1) Resume", 0, 20)
        oled.text("(5) Cancel", 0, 30)
        oled.show()
        if button1.value() == 1:
            stage = 'brew'
            menuX = menuSwitch(menuX)
            endTime = time.time() + remainingTime
        elif button5.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)


    #display a finished message and prompt the user to brew another cup
    #and take user input through buttons
        #note: the tea bag will still be in the water despite the timer havinf finished
    if stage == 'fin':
        oled.fill(0)
        oled.text("Tea Brewed!", 0, 0)
        oled.text("Press (1) to", 0, 10)
        oled.text("brew another.", 0, 20)
        oled.show()
        if button1.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)