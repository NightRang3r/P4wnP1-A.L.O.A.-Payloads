#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
L.O.R.D - P4wnP1 A.L.O.A Enhanced Menu System
Developed by 4r4m
Enhanced UI with animations and better UX
"""

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
import RPi.GPIO as GPIO
import datetime
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
import socket
import sys
import os
import struct
import smbus
import random
import shutil

# ==================== CONFIGURATION ====================
UPS = 0  # 1 = UPS Lite connected / 0 = No UPS Lite hat
SCNTYPE = 1  # 1 = OLED / 2 = TERMINAL MODE
USER_I2C = 0  # 0 = SPI, 1 = I2C

# ==================== GPIO PIN DEFINITIONS ====================
RST_PIN = 25
CS_PIN = 8
DC_PIN = 24
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16

# ==================== DISPLAY CONSTANTS ====================
WIDTH = 128
HEIGHT = 64
PADDING = 2
LINE_HEIGHT = 10

# ==================== P4WNP1 PATHS ====================
HIDPATH = "/usr/local/P4wnP1/HIDScripts/"
SSHPATH = "/usr/local/P4wnP1/scripts/"

# ==================== GPIO SETUP ====================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ==================== DISPLAY INITIALIZATION ====================
if SCNTYPE == 1:
    if USER_I2C == 1:
        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.output(RST_PIN, GPIO.HIGH)
        serial = i2c(port=1, address=0x3c)
    else:
        serial = spi(device=0, port=0, bus_speed_hz=8000000, 
                    transfer_size=4096, gpio_DC=24, gpio_RST=25)
    device = sh1106(serial, rotate=2)

# ==================== FONT LOADING ====================
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_title = ImageFont.load_default()

# ==================== MENU ICONS (8x8 PIXEL ART) ====================
ICONS = {
    'system': [[0,0,1,1,1,1,0,0],[0,1,1,1,1,1,1,0],[1,1,0,1,1,0,1,1],[1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1],[0,1,0,0,0,0,1,0],[0,0,1,1,1,1,0,0],[0,0,0,0,0,0,0,0]],
    'hid': [[0,1,1,1,1,1,1,0],[1,1,0,0,0,0,1,1],[1,0,1,0,0,1,0,1],[1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1],[1,0,0,0,0,0,0,1],[1,1,0,0,0,0,1,1],[0,1,1,1,1,1,1,0]],
    'wifi': [[0,0,0,1,1,0,0,0],[0,1,1,1,1,1,1,0],[1,1,0,1,1,0,1,1],[0,0,1,1,1,1,0,0],
             [0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,1,0,0,0],[0,0,0,1,1,0,0,0]],
    'trigger': [[0,0,0,1,0,0,0,0],[0,0,1,1,1,0,0,0],[0,1,1,1,1,1,0,0],[1,1,0,1,0,1,1,0],
                [0,0,0,1,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,1,1,1,0,0,0]],
    'template': [[1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,1],[1,0,1,1,1,1,0,1],[1,0,1,0,0,0,0,1],
                 [1,0,1,0,1,1,1,1],[1,0,1,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1]],
    'tools': [[0,0,0,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,1,1,1,1,0,0,0],[1,1,1,1,0,0,0,0],
              [0,1,1,0,1,1,0,0],[0,0,0,0,1,1,1,0],[0,0,0,0,0,1,1,1],[0,0,0,0,0,0,1,1]],
    'bettercap': [[0,1,1,1,1,1,1,0],[1,0,0,0,0,0,0,1],[1,0,1,1,0,0,0,1],[1,0,1,1,0,1,0,1],
                  [1,0,0,0,0,1,0,1],[1,0,0,1,1,1,0,1],[1,0,0,0,0,0,0,1],[0,1,1,1,1,1,1,0]]
}

# ==================== MENU STRUCTURE ====================
MENU_ITEMS = {
    0: {'text': 'L.O.R.D  P4wnP1', 'icon': None, 'action': 'about'},
    1: {'text': 'SYSTEM', 'icon': 'system', 'submenu': 7},
    2: {'text': 'HID ATTACKS', 'icon': 'hid', 'submenu': 14},
    3: {'text': 'WIRELESS', 'icon': 'wifi', 'submenu': 21},
    4: {'text': 'TRIGGERS', 'icon': 'trigger', 'submenu': 28},
    5: {'text': 'TEMPLATES', 'icon': 'template', 'submenu': 35},
    6: {'text': 'INFOSEC TOOLS', 'icon': 'tools', 'submenu': 42},
    7: {'text': 'System Info', 'icon': 'system', 'action': 'sysinfo'},
    8: {'text': 'OLED Brightness', 'icon': 'system', 'action': 'brightness'},
    9: {'text': 'OS Detection', 'icon': 'system', 'action': 'osdetect'},
    10: {'text': 'Display OFF', 'icon': 'system', 'action': 'screenoff'},
    11: {'text': 'Keys Test', 'icon': 'system', 'action': 'keytest'},
    12: {'text': 'Reboot GUI', 'icon': 'system', 'action': 'restart'},
    13: {'text': 'Shutdown', 'icon': 'system', 'action': 'shutdown'},
    14: {'text': 'RUN HID Script', 'icon': 'hid', 'action': 'runhid'},
    15: {'text': 'Gamepad Mode', 'icon': 'hid', 'action': 'gamepad'},
    16: {'text': 'Mouse Mode', 'icon': 'hid', 'action': 'mouse'},
    17: {'text': 'Typing Speed', 'icon': 'hid', 'action': 'typespeed'},
    18: {'text': 'Key Layout', 'icon': 'hid', 'action': 'keylayout'},
    21: {'text': 'Scan WiFi AP', 'icon': 'wifi', 'action': 'scanwifi'},
    22: {'text': 'Bettercap WebUI', 'icon': 'bettercap', 'action': 'bettercap'},
    23: {'text': 'BC MassDeauth', 'icon': 'wifi', 'action': 'bettercap_massdeauth'},
    24: {'text': 'BC NetMon', 'icon': 'bettercap', 'action': 'bettercap_netmon'},
    25: {'text': 'BC MANA AP', 'icon': 'bettercap', 'action': 'bettercap_mana'},
    28: {'text': 'Send Trigger', 'icon': 'trigger', 'action': 'trigger1'},
    35: {'text': 'Full Settings', 'icon': 'template', 'action': 'template_full'},
    36: {'text': 'Bluetooth', 'icon': 'template', 'action': 'template_bt'},
    37: {'text': 'USB', 'icon': 'template', 'action': 'template_usb'},
    38: {'text': 'WiFi', 'icon': 'template', 'action': 'template_wifi'},
    39: {'text': 'Trigger Actions', 'icon': 'template', 'action': 'template_trigger'},
    40: {'text': 'Network', 'icon': 'template', 'action': 'template_net'},
    42: {'text': 'Inject RShell ADM', 'icon': 'tools', 'action': 'rshell_admin'},
    43: {'text': 'Inject RShell USR', 'icon': 'tools', 'action': 'rshell_user'},
    44: {'text': 'Exploit RShell', 'icon': 'tools', 'action': 'rshell_exploit'},
}

# ==================== HELPER FUNCTIONS ====================
def shell(cmd):
    """Execute shell command and return output"""
    try:
        return subprocess.check_output(cmd, shell=True).decode('utf-8')
    except:
        return ""

def draw_icon(draw, x, y, icon_name):
    """Draw 8x8 icon at position"""
    if icon_name and icon_name in ICONS:
        icon = ICONS[icon_name]
        for row in range(8):
            for col in range(8):
                if icon[row][col]:
                    draw.point((x + col, y + row), fill=255)

def draw_animated_border(draw, frame):
    """Draw animated border effect"""
    offset = frame % 4
    for i in range(0, WIDTH, 4):
        if (i + offset) % 8 < 4:
            draw.point((i, 0), fill=255)
            draw.point((i, HEIGHT-1), fill=255)
    for i in range(0, HEIGHT, 4):
        if (i + offset) % 8 < 4:
            draw.point((0, i), fill=255)
            draw.point((WIDTH-1, i), fill=255)

def DisplayText(l1, l2, l3, l4, l5, l6, l7):
    """Simple text display function"""
    if SCNTYPE == 1:
        with canvas(device) as draw:
            draw.text((0, 0), l1, font=font_small, fill=255)
            draw.text((0, 9), l2, font=font_small, fill=255)
            draw.text((0, 18), l3, font=font_small, fill=255)
            draw.text((0, 27), l4, font=font_small, fill=255)
            draw.text((0, 36), l5, font=font_small, fill=255)
            draw.text((0, 45), l6, font=font_small, fill=255)
            draw.text((0, 54), l7, font=font_small, fill=255)
    elif SCNTYPE == 2:
        os.system('clear')
        print(l1, l2, l3, l4, l5, l6, l7, sep='\n')

# ==================== BOOT ANIMATION ====================
def boot_animation():
    """Enhanced boot animation with dithering and icon effects"""
    if SCNTYPE != 1:
        return

    # Dithered background shimmer + title fade
    for frame in range(12):
        with canvas(device) as draw:
            # dither background noise
            for y in range(0, HEIGHT, 2):
                for x in range(0, WIDTH, 2):
                    if (x + y + frame) % 6 == 0:
                        draw.point((x, y), fill=255)
            text = "L.O.R.D"
            bbox = draw.textbbox((0, 0), text, font=font_title)
            text_width = bbox[2] - bbox[0]
            x = (WIDTH - text_width) // 2
            draw.text((x, 8), text, font=font_title, fill=255)

            subtitle = "P4wnP1 A.L.O.A"
            bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            text_width = bbox[2] - bbox[0]
            x = (WIDTH - text_width) // 2
            draw.text((x, 30), subtitle, font=font_small, fill=255)

            credit = "by 4r4m"
            bbox = draw.textbbox((0, 0), credit, font=font_small)
            text_width = bbox[2] - bbox[0]
            x = (WIDTH - text_width) // 2
            draw.text((x, 48), credit, font=font_small, fill=255)
        time.sleep(0.08)

    # Animated icon parade with progressive brightness
    icons_list = ['system', 'hid', 'wifi', 'trigger', 'template', 'tools', 'bettercap']
    for step in range(len(icons_list) + 4):
        with canvas(device) as draw:
            draw.text((6, 2), "Initializing...", font=font_small, fill=255)
            for i, icon_name in enumerate(icons_list):
                x_pos = 8 + (i * 16)
                y_pos = 18 + (1 if (step + i) % 3 == 0 else 0)
                if i <= step:
                    draw_icon(draw, x_pos, y_pos, icon_name)
                else:
                    # draw faint placeholder
                    for r in range(8):
                        for c in range(8):
                            if ICONS[icon_name][r][c] and ((r + c + step) % 4 == 0):
                                draw.point((x_pos + c, y_pos + r), fill=255)
            # progress bar
            draw.rectangle((2, 56, WIDTH-2, 62), outline=255, fill=0)
            progress_width = int(min(step / (len(icons_list)-1 if len(icons_list)>1 else 1), 1.0)*(WIDTH-6))
            draw.rectangle((4, 58, 4 + progress_width, 60), fill=255)
        time.sleep(0.22)

    # brief flash to show ready
    for _ in range(2):
        device.hide()
        time.sleep(0.06)
        device.show()
        time.sleep(0.06)

# ==================== MENU RENDERING ====================
def render_menu(page, cursor, frame=0):
    """Render menu with icons and animations"""
    if SCNTYPE != 1:
        return
    
    with canvas(device) as draw:
        draw_animated_border(draw, frame)
        
        header = "[ L.O.R.D MAIN ]" if page == 0 else "[ MENU ]"
        bbox = draw.textbbox((0, 0), header, font=font_medium)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, 2), header, font=font_medium, fill=255)
        draw.line((2, 12, WIDTH-2, 12), fill=255)
        
        y_pos = 16
        items_per_page = 5
        start_idx = page
        
        for i in range(items_per_page):
            idx = start_idx + i
            if idx in MENU_ITEMS:
                item = MENU_ITEMS[idx]
                is_selected = (i == cursor - 1) if page == 0 else (idx == page + cursor - 1)
                
                if is_selected:
                    draw.rectangle((2, y_pos-1, WIDTH-2, y_pos + LINE_HEIGHT), 
                                 outline=255, fill=0)
                    draw.text((5, y_pos), ">", font=font_medium, fill=255)
                
                if item['icon']:
                    draw_icon(draw, 15, y_pos + 1, item['icon'])
                
                text_x = 26 if item['icon'] else 15
                draw.text((text_x, y_pos), item['text'][:15], 
                         font=font_small, fill=255)
                
                y_pos += LINE_HEIGHT

# ==================== UPS BATTERY FUNCTIONS ====================
def readVoltage(bus):
    """Read voltage from UPS HAT"""
    try:
        address = 0x36
        read = bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 / 1000 / 16
        return voltage
    except:
        return 0.0

def readCapacity(bus):
    """Read battery capacity from UPS HAT"""
    try:
        address = 0x36
        read = bus.read_word_data(address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped / 256
        return min(capacity, 100)
    except:
        return 0.0

# ==================== SYSTEM INFO ====================
def sysinfos():
    """Display system information"""
    if UPS == 1:
        try:
            bus = smbus.SMBus(1)
        except:
            bus = None
    else:
        bus = None
    
    while GPIO.input(KEY_LEFT_PIN):
        now = datetime.datetime.now()
        today_time = now.strftime("%H:%M:%S")
        today_date = now.strftime("%d %b %y")
        
        try:
            IP = shell("hostname -I | cut -d' ' -f1").strip()
            IP2 = shell("hostname -I").split()[1] if len(shell("hostname -I").split()) > 1 else "N/A"
            IP3 = shell("hostname -I").split()[2] if len(shell("hostname -I").split()) > 2 else "N/A"
        except:
            IP, IP2, IP3 = "N/A", "N/A", "N/A"
        
        CPU = shell("top -bn1 | grep %Cpu | awk '{printf \"%.0f\",$2}'").strip()
        
        try:
            temp = int(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000
        except:
            temp = 0
        
        MemUsage = shell("free -m | awk 'NR==2{printf \"MEM:%.0f%%\", $3*100/$2}'").strip()
        Disk = shell("df -h | awk '$NF==\"/\"{printf \"Disk:%dG/%dG %s\", $3,$2,$5}'").strip()
        
        if UPS == 1 and bus:
            volt = readVoltage(bus)
            batt = int(readCapacity(bus))
            bat_str = f"BAT:{volt:.2f}V {batt}%"
        else:
            bat_str = "BAT: N/C"
        
        DisplayText(
            f"WIFI: {IP}",
            f"USB : {IP2}",
            f"BTH : {IP3}",
            f"{MemUsage} CPU:{CPU}% {temp}C",
            Disk,
            bat_str,
            f"{today_date} {today_time}"
        )
        time.sleep(0.5)

# ==================== CONTRAST/BRIGHTNESS ====================
def OLEDContrast(contrast):
    """Adjust OLED contrast with visual feedback"""
    if SCNTYPE != 1:
        return contrast
    
    time.sleep(0.3)
    while GPIO.input(KEY_LEFT_PIN):
        with canvas(device) as draw:
            draw.text((25, 5), "BRIGHTNESS", font=font_medium, fill=255)
            
            if not GPIO.input(KEY_UP_PIN):
                draw.polygon([(60, 20), (64, 15), (68, 20)], outline=255, fill=255)
                contrast = min(contrast + 5, 255)
            else:
                draw.polygon([(60, 20), (64, 15), (68, 20)], outline=255, fill=0)
            
            if not GPIO.input(KEY_DOWN_PIN):
                draw.polygon([(60, 45), (64, 50), (68, 45)], outline=255, fill=255)
                contrast = max(contrast - 5, 0)
            else:
                draw.polygon([(60, 45), (64, 50), (68, 45)], outline=255, fill=0)
            
            draw.text((40, 30), f"{contrast}", font=font_large, fill=255)
            draw.rectangle((10, 55, 118, 60), outline=255, fill=0)
            bar_width = int((contrast / 255) * 106)
            draw.rectangle((11, 56, 11 + bar_width, 59), fill=255)
            
            device.contrast(contrast)
        
        time.sleep(0.05)
    
    time.sleep(0.3)
    return contrast

# ==================== SCREEN OFF ====================
def SreenOFF():
    """Turn screen off until button press"""
    if SCNTYPE == 1:
        device.hide()
        while GPIO.input(KEY_LEFT_PIN):
            time.sleep(0.1)
        device.show()

# ==================== KEY TEST ====================
def KeyTest():
    """Visual key tester"""
    if SCNTYPE != 1:
        return
    
    time.sleep(0.3)
    while GPIO.input(KEY_LEFT_PIN):
        with canvas(device) as draw:
            draw.text((35, 2), "KEY TEST", font=font_small, fill=255)
            
            draw.polygon([(20, 20), (30, 10), (40, 20)], 
                        outline=255, fill=255 if not GPIO.input(KEY_UP_PIN) else 0)
            draw.polygon([(0, 30), (10, 20), (10, 40)], 
                        outline=255, fill=255 if not GPIO.input(KEY_LEFT_PIN) else 0)
            draw.polygon([(50, 30), (40, 20), (40, 40)], 
                        outline=255, fill=255 if not GPIO.input(KEY_RIGHT_PIN) else 0)
            draw.polygon([(20, 50), (30, 60), (40, 50)], 
                        outline=255, fill=255 if not GPIO.input(KEY_DOWN_PIN) else 0)
            draw.rectangle((22, 24, 38, 36), 
                          outline=255, fill=255 if not GPIO.input(KEY_PRESS_PIN) else 0)
            
            draw.ellipse((70, 15, 85, 30), 
                        outline=255, fill=255 if not GPIO.input(KEY1_PIN) else 0)
            draw.text((75, 19), "1", font=font_small, 
                     fill=0 if not GPIO.input(KEY1_PIN) else 255)
            
            draw.ellipse((95, 25, 110, 40), 
                        outline=255, fill=255 if not GPIO.input(KEY2_PIN) else 0)
            draw.text((100, 29), "2", font=font_small, 
                     fill=0 if not GPIO.input(KEY2_PIN) else 255)
            
            draw.ellipse((70, 35, 85, 50), 
                        outline=255, fill=255 if not GPIO.input(KEY3_PIN) else 0)
            draw.text((75, 39), "3", font=font_small, 
                     fill=0 if not GPIO.input(KEY3_PIN) else 255)
        
        time.sleep(0.05)
    
    time.sleep(0.3)

# ==================== CONFIRMATION DIALOG ====================
def confirm_dialog(title, message):
    """Show confirmation dialog"""
    time.sleep(0.3)
    answer = 0
    
    while answer == 0:
        with canvas(device) as draw:
            draw.rectangle((5, 5, WIDTH-5, HEIGHT-5), outline=255, fill=0)
            draw.text((10, 10), title[:16], font=font_small, fill=255)
            draw.line((8, 19, WIDTH-8, 19), fill=255)
            
            words = message.split()
            line1 = ' '.join(words[:2])
            line2 = ' '.join(words[2:4]) if len(words) > 2 else ''
            draw.text((10, 25), line1, font=font_small, fill=255)
            if line2:
                draw.text((10, 34), line2, font=font_small, fill=255)
            
            draw.text((15, 50), "YES", font=font_small, fill=255)
            draw.text((WIDTH-35, 50), "NO", font=font_small, fill=255)
        
        if not GPIO.input(KEY_UP_PIN) or not GPIO.input(KEY1_PIN):
            answer = 1
            time.sleep(0.2)
        elif not GPIO.input(KEY_DOWN_PIN) or not GPIO.input(KEY3_PIN):
            answer = 2
            time.sleep(0.2)
        
        time.sleep(0.05)
    
    time.sleep(0.3)
    return answer == 1

# ==================== FILE SELECTOR ====================
def FileSelect(path, ext):
    """Enhanced file selector"""
    cmd = f"ls -F --format=single-column {path}*{ext}"
    try:
        listattack = shell(cmd).replace(ext, "").replace(path, "").replace("*", "").split("\n")
        listattack = [f for f in listattack if f]
    except:
        return ""
    
    if not listattack:
        DisplayText("", "", "  No files found", "", "", "", "")
        time.sleep(2)
        return ""
    
    maxi = len(listattack)
    cur = 0
    time.sleep(0.3)
    
    while GPIO.input(KEY_LEFT_PIN):
        with canvas(device) as draw:
            draw.text((2, 2), f"SELECT FILE [{cur+1}/{maxi}]", font=font_small, fill=255)
            draw.line((0, 11, WIDTH, 11), fill=255)
            
            y_pos = 14
            start = max(0, cur - 2)
            end = min(maxi, start + 5)
            
            for i in range(start, end):
                is_selected = (i == cur)
                if is_selected:
                    draw.rectangle((2, y_pos-1, WIDTH-2, y_pos+9), outline=255, fill=0)
                    draw.text((5, y_pos), ">", font=font_small, fill=255)
                
                filename = listattack[i][:18]
                draw.text((15, y_pos), filename, font=font_small, fill=255)
                y_pos += 10
        
        if not GPIO.input(KEY_UP_PIN):
            cur = max(0, cur - 1)
            time.sleep(0.15)
        elif not GPIO.input(KEY_DOWN_PIN):
            cur = min(maxi - 1, cur + 1)
            time.sleep(0.15)
        elif not GPIO.input(KEY_RIGHT_PIN):
            time.sleep(0.3)
            return listattack[cur] + ext
        
        time.sleep(0.05)
    
    return ""

# ==================== TEMPLATE FUNCTIONS ====================
def GetTemplateList(template_type):
    """Get list of templates by type"""
    cmd = "P4wnP1_cli template list"
    list_data = shell(cmd)
    list_data = list_data.replace("Templates of type ", "")
    list_data = list_data.replace(" :", "")
    list_data = list_data.replace("-" * 36 + "\n", "")
    lines = list_data.split("\n")
    
    result = ""
    found = 0
    for line in lines:
        if line == template_type:
            found = 1
        elif line == "":
            found = 0
        elif found == 1:
            result += line + "\n"
    
    return result

def templateSelect(liste):
    """Select a template from P4wnP1_cli template list output"""
    data = GetTemplateList(liste)
    items = [l.strip() for l in data.split('\n') if l.strip()]
    if not items:
        DisplayText("", "", "No templates found", "", "", "", "")
        time.sleep(1.5)
        return ""

    cur = 0
    maxi = len(items)
    time.sleep(0.2)
    while GPIO.input(KEY_LEFT_PIN):
        with canvas(device) as draw:
            draw.text((2, 2), f"TEMPLATE [{cur+1}/{maxi}]", font=font_small, fill=255)
            draw.line((0, 11, WIDTH, 11), fill=255)
            y = 14
            start = max(0, cur - 2)
            end = min(maxi, start + 5)
            for i in range(start, end):
                is_sel = (i == cur)
                if is_sel:
                    draw.rectangle((2, y-1, WIDTH-2, y+9), outline=255, fill=0)
                    draw.text((5, y), ">", font=font_small, fill=255)
                draw.text((15, y), items[i][:18], font=font_small, fill=255)
                y += 10

        if not GPIO.input(KEY_UP_PIN):
            cur = max(0, cur - 1)
            time.sleep(0.12)
        elif not GPIO.input(KEY_DOWN_PIN):
            cur = min(maxi - 1, cur + 1)
            time.sleep(0.12)
        elif not GPIO.input(KEY_RIGHT_PIN):
            time.sleep(0.2)
            return items[cur]

        time.sleep(0.05)

    return ""


# ------------------ Action dispatcher & helpers ------------------
OLED_CONTRAST = 128

def is_port_in_use(port, host='127.0.0.1'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((host, int(port)))
        s.close()
        return True
    except:
        return False

def start_bettercap_wrapper(port=8081):
    """Start Bettercap Web UI safely (wrapper script if present). Returns URL or error."""
    # prefer packaged script if available
    local_script = os.path.join(os.path.dirname(__file__), 'scripts', 'start_bettercap.sh')
    global_script = '/usr/local/P4wnP1/scripts/start_bettercap.sh'
    DisplayText("Starting Bettercap", "Checking port...", "", "", "", "", "")
    time.sleep(0.3)

    if is_port_in_use(port):
        url = f"http://{socket.gethostbyname(socket.gethostname())}:{port}"
        DisplayText("Bettercap already", f"running on port {port}", url, "", "", "", "")
        time.sleep(2)
        return url

    script_to_call = None
    if os.path.exists(global_script):
        script_to_call = global_script
    elif os.path.exists(local_script):
        script_to_call = local_script

    try:
        if script_to_call:
            subprocess.Popen(['sh', script_to_call, str(port)])
        else:
            # fallback: try launching bettercap directly
            subprocess.Popen(['bettercap', '--http-ui', '--http-ui-port', str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # give it a moment to start
        for _ in range(12):
            if is_port_in_use(port):
                url = f"http://{socket.gethostbyname(socket.gethostname())}:{port}"
                DisplayText("Bettercap started", url, "", "", "", "", "")
                time.sleep(2)
                return url
            time.sleep(0.5)

        DisplayText("Failed to start", f"Bettercap port {port}", "", "", "", "", "")
        time.sleep(2)
        return ""
    except Exception as e:
        DisplayText("Error launching", str(e)[:18], "", "", "", "", "")
        time.sleep(2)
        return ""

def action_dispatcher(action):
    """Map action strings from MENU_ITEMS to callable functions."""
    if not action:
        return

    if action == 'about':
        DisplayText("L.O.R.D - P4wnP1", "Enhanced Menu", "by 4r4m", "", "", "", "")
        time.sleep(2)
    elif action == 'sysinfo':
        sysinfos()
    elif action == 'brightness' or action == 'oledcontrast':
        global OLED_CONTRAST
        OLED_CONTRAST = OLEDContrast(OLED_CONTRAST)
    elif action == 'screenoff' or action == 'screenoff':
        SreenOFF()
    elif action == 'keytest':
        KeyTest()
    elif action == 'bettercap':
        start_bettercap_wrapper(8081)
    elif action == 'bettercap_massdeauth':
        # Confirm before running disruptive wireless attack
        if confirm_dialog("Mass Deauth", "Run mass deauth?"):
            run_bettercap_caplet('massdeauth')
    elif action == 'bettercap_netmon':
        if confirm_dialog("Net Monitor", "Start netmon caplet?"):
            run_bettercap_caplet('netmon')
    elif action == 'bettercap_mana':
        if confirm_dialog("MANA AP", "Start MANA rogue AP?"):
            run_bettercap_caplet('mana')
    else:
        # generic: try calling a function by name if it exists
        func = globals().get(action)
        if callable(func):
            try:
                func()
            except TypeError:
                # if function expects args, ignore
                pass
        else:
            # fallback: try shell command with P4wnP1_cli
            try:
                shell(action)
            except:
                DisplayText("Unknown action", action, "", "", "", "", "")
                time.sleep(1)

def find_bettercap_bin():
    """Return path to bettercap binary or None"""
    paths = ['/usr/bin/bettercap', '/usr/local/bin/bettercap']
    for p in paths:
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
    p = shutil.which('bettercap')
    return p

def run_bettercap_caplet(caplet_name, iface=None):
    """Run a bettercap caplet in background; returns True if launched."""
    bcmd = find_bettercap_bin()
    if not bcmd:
        DisplayText("bettercap not found", "Install first", "", "", "", "", "")
        time.sleep(1.5)
        return False

    args = [bcmd, '-caplet', caplet_name]
    # if iface provided, attempt to pass via -eval
    if iface:
        args = [bcmd, '-eval', f"set iface {iface}; caplets.run {caplet_name}"]

    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        DisplayText(f"Launched {caplet_name}", "See logs for details", "", "", "", "", "")
        time.sleep(1.5)
        return True
    except Exception as e:
        DisplayText("Failed to launch", str(e)[:18], "", "", "", "", "")
        time.sleep(1.5)
        return False

