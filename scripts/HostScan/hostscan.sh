#!/bin/bash

LOOTDIR=/usr/local/P4wnP1/www/loot/scans
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);
TARGET_IP=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f3);
HOST_IP=$(ifconfig usbeth | awk '$1=="inet"{print $2}');

echo "[*] Checking if nmap is installed..."
if [ ! -f /usr/bin/nmap ]; then
    echo "[!] nmap not found!"
    exit 1
  fi

echo "[*] Creating loot dir..."
mkdir -p $LOOTDIR
HOST=$TARGET_HOSTNAME
[[ -z "$HOST" ]] && HOST="noname"
COUNT=$(ls -lad $LOOTDIR/$HOST* | wc -l)
COUNT=$((COUNT+1))
mkdir -p $LOOTDIR/$HOST-$COUNT
mkdir -p /usr/local/P4wnP1/www/loot/scans/$HOST-$COUNT

if [ -z "$TARGET_IP" ]; then
	exit 1
fi

echo "[*] Initiating nmap scan on: $TARGET_HOSTNAME - $TARGET_IP"

nmap -sTV -v $TARGET_IP -O -A --script discovery,version --system-dns -oN /usr/local/P4wnP1/www/loot/scans/$HOST-$COUNT/$HOST-$COUNT.txt


echo "[+] Scan completed!"
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
echo "[*] Killing nmap..."
process=$(ps aux | grep 'nmap' | grep -v 'grep')

# Check if the process was found
if [ ! -z "$process" ]; then
    # Extract the PID
    pid=$(echo $process | awk '{print $2}')

    # Kill the process
    kill $pid

    echo "Process 'nmap' with PID $pid has been terminated."
else
    echo "No 'nmap' process found."
fi