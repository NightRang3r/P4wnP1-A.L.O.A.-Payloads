# P4wnP1_ALOA_OLED_MENU_V2
on the road P4wnP1 ALOA menu 

Installation instructions 
on boot partition edit config.txt to set I2C and SPI to active
in termnial you can type 
nano /boot/config.txt
find the section far away down and set : 

dtparam=i2c_arm=on
dtparam=i2c1=on

and find and set spi section 

dtparam=spi=on

note : for the waveshare hat i used (and all gui.py is set like this) the inteface is SPI and not I2C
if you have a I2C oled edit gui.py file and set on line 72
USER_I2C = 1 #set to 1 if your oled is I2C

GPIO 8 keys are default waveshare hat

you can edit to set to your hat if different
GPIO
KEY_UP_PIN     : 6, 
KEY_DOWN_PIN   : 19, 
KEY_LEFT_PIN   : 5, 
KEY_RIGHT_PIN  : 26, 
KEY_PRESS_PIN  : 13, 
KEY1_PIN       : 21, 
KEY2_PIN       : 20, 
KEY3_PIN       : 16

Remember this menu is in alpha version, not all function are ready 

then to install , run sh install.sh and script will install all the files needed

if error with luma , think about install luma core : 
pip install luma.core
pip install luma.oled

directly flashable image file available at http://dl.free.fr/j8M68z2JK (OLED and UPS module installed)
mirror on mega : https://mega.nz/#!ZEkDlSLJ!ZAIxmKVmsGwjK2ICfrWRni7kuFJyMXsg9eTDayQqe_U

new 21.02.2020 : https://mega.nz/#!YYtS2S6A!Q5OgMvLUtAM_x7jt7vBTY8Zu8lHdyyPoaLdsipVufWg P4wnP1 v0.1.1 with oled drivers and menu preinstalled

in P4wnP1 web interface , if you want to menu start at "boot" create a trigger in you default template (by default startup)
with : when service start => run script sh and choose runmenu.sh

enjoy
