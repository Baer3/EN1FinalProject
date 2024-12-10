from s2pico_oled import OLED
from machine import Pin, I2C, PWM
import ssd1306
from time import sleep
import time
import onewire
from ds18x20 import DS18X20
import math

servo_bob = PWM(Pin(2), freq=50)
servo_drop = PWM(Pin(3), freq=50)
pin = Pin(1, Pin.IN)
button1 = Pin(21, Pin.IN)
button2 = Pin(33, Pin.IN)
button3 = Pin(34, Pin.IN)
button4 = Pin(35, Pin.IN)
button5 = Pin(36, Pin.IN)
degreesC = 0
degreesF = 0
start = 0
t = 0 #in seconds
BLACK_TEMP = 100
GREEN_TEMP = 82
OOLONG_TEMP = 90
HERBAL_TEMP = 100
menuX = 120
MENU1a = "Tea Type:"
MENU1b = "(1) Black, (2) Green, (3) Oolong, (4) Herbal, (5) Other/Custom"
MENU_BLACKa = "Black Tea:"
MENU_BLACKb = "100C, 3-5 mins"
MENU_BLACKc = "Use Recomended Settings? (1) Yes, (2) No, (5) Back"
MENU_GREENa = "Green Tea:"
MENU_GREENb = "82C, 1-2 mins"
MENU_GREENc = "Use Recomended Settings? (1) Yes, (2) No, (5) Back"
MENU_OOLONGa = "Oolong Tea:"
MENU_OOLONGb = "90C, 2-3 mins"
MENU_OOLONGc = "Use Recomended Settings? (1) Yes, (2) No, (5) Back"
MENU_HERBALa = "Herbal Tea:"
MENU_HERBALb = "100C, 5-10 mins"
MENU_HERBALc = "Use Recomended Settings? (1) Yes, (2) No, (5) Back"
MENU_TEMPa = "Put temperature"
MENU_TEMPb = "probe in water."
MENU_TEMPc = "(1) Continue, (2) Skip, (5) Back"
MENU_TEMP2a = "Reading"
MENU_TEMP2b = "Temperature..."
MENU_COLDa = "Water is cold."
MENU_COLDb = "Heat the water."
MENU_COLDc = "(1) Again, (5) Back"
MENU_CUSTOM = "Input time:"
stage = '0'
teaType = '0'
idealTemp = 0

i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = OLED(i2c, Pin(18))

oled.fill(0)

#create the onewire object
tempSensor = DS18X20(onewire.OneWire(pin))

#scan for device addresses
roms = tempSensor.scan()

#print temperatures
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

def menuSwitch(x):
    x = 120
    sleep(.5)
    return x

while True:
    oled.fill(0)
    menuX -= 1
    if menuX < - 500:
        menuX = 120
    if stage == '0':
        oled.fill(0)
        servo_bob.duty(90)
        servo_drop.duty(90)
        oled.text(MENU1a, 0, 0)
        oled.text(MENU1b, menuX, 12)
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



    if stage == '1':
        oled.fill(0)
        if teaType == 'b':
            oled.text(MENU_BLACKa, 0, 0)
            oled.text(MENU_BLACKb, 0, 12)
            oled.text(MENU_BLACKc, menuX, 24)
        elif teaType == 'g':
            oled.text(MENU_GREENa, 0, 0)
            oled.text(MENU_GREENb, 0, 12)
            oled.text(MENU_GREENc, menuX, 24)
        elif teaType == 'o':
            oled.text(MENU_OOLONGa, 0, 0)
            oled.text(MENU_OOLONGb, 0, 12)
            oled.text(MENU_OOLONGc, menuX, 24)
        elif teaType == 'h':
            oled.text(MENU_HERBALa, 0, 0)
            oled.text(MENU_HERBALb, 0, 12)
            oled.text(MENU_HERBALc, menuX, 24)
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



    if stage == '2':
        oled.fill(0)
        oled.text(MENU_TEMPa, 0, 0)
        oled.text(MENU_TEMPb, 0, 12)
        oled.text(MENU_TEMPc, menuX, 24)
        oled.show()
        if button1.value() == 1:
            stage = '3'
            menuX = menuSwitch(menuX)
        elif button2.value() == 1:
            degreesC = 0
            degreesF = 0
            t = 0
            stage = 'custom'
            menuX = menuSwitch(menuX)
        elif button5.value() == 1:
            stage = '1'
            menuX = menuSwitch(menuX)



    if stage == '3':
        oled.fill(0)
        oled.text(MENU_TEMP2a, 0, 0)
        oled.text(MENU_TEMP2b, 0, 12)
        oled.show()
        degreesC = readTemps() + 50
        degreesF = (degreesC * (9/5)) + 32
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



    if stage == '4':
        oled.text("Temp: " + str(degreesC) + "C", 0, 0)
        oled.text("Time: " + str(int(t/60)) + " minutes", 0, 12)
        oled.text("(1) Start, (5) Back", menuX, 24)
        oled.show()
        if button1.value() == 1:
            stage = 'brew'
            menuX = menuSwitch(menuX)
            endTime = time.time() + t
        elif button5.value() == 1:
            stage = '2'
            menuX = menuSwitch(menuX)



    if stage == 'cold':
        oled.fill(0)
        oled.text(MENU_COLDa, 0, 0)
        oled.text(MENU_COLDb, 0, 12)
        oled.text(MENU_COLDc, menuX, 24)
        oled.show()
        if button1.value() == 1:
            stage = '3'
            menuX = menuSwitch(menuX)
        elif button5.value() == 1:
            stage = '2'
            menuX = menuSwitch(menuX)
      
      
      
    if stage == 'custom':
        oled.fill(0)
        oled.text(MENU_CUSTOM, 0, 0)
        oled.text("Time: " + str(math.floor(t/60)), 0, 12)
        oled.text("(1) +1 Minute, (2) +2 Minutes, (3) +5 Minutes, (4) Continue, (5) Back", menuX, 24)
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
        elif button5.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)



    if stage == 'brew':
        oled.fill(0)
        servo_drop.duty(20)
        while endTime > time.time():
            menuX -= 1
            if menuX < - 500:
                menuX = 120
            remainingTime = endTime - time.time()
            oled.fill(0)
            oled.text("Time Remaining:", 0, 0)
            oled.text(str(math.floor(remainingTime / 60)) + " Min " + str(remainingTime % 60) + " Sec", 0, 12)
            oled.text("(1) Pause, (5) Cancel", menuX, 24)
            oled.show()
            if remainingTime % 2 == 0:
                servo_bob.duty(70)
            else:
                servo_bob.duty(110)
                
            if button1.value() == 1:
                stage = 'pause'
                servo_bob.duty(125)
                menuX = menuSwitch(menuX)
                break
            elif button5.value() == 1:
                stage = '0'
                servo_bob.duty(125)
                menuX = menuSwitch(menuX)
                break
        if stage == 'brew':
            stage = 'fin'
            servo_bob.duty(125)



    if stage == 'pause':
        oled.fill(0)
        oled.text("Brewing Paused.", 0, 0)
        oled.text(str(math.floor(remainingTime / 60)) + " Min " + str(remainingTime % 60) + " Sec", 0, 12)
        oled.text("(1) Resume, (5) Cancel", menuX, 24)
        oled.show()
        if button1.value() == 1:
            stage = 'brew'
            menuX = menuSwitch(menuX)
            endTime = time.time() + remainingTime
        elif button5.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)



    if stage == 'fin':
        oled.fill(0)
        oled.text("Tea Brewed!", 0, 0)
        oled.text("Press (1) to", 0, 12)
        oled.text("brew another.", 0, 24)
        oled.show()
        if button1.value() == 1:
            stage = '0'
            menuX = menuSwitch(menuX)