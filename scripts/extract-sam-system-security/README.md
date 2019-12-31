# Extract SAM, SYSTEM, SECURITY for P4wnP1-A.L.O.A

Author: NightRanger

Firmware: v0.1.0-alpha2

## Description

Steal windows sam, system and security to retrive hashes

Based on: https://github.com/PingDucKY/payloads-P4wnP1-A.L.O.A/tree/master/steal-windows-hash

Saves creds to the loot folder ```/usr/local/P4wnP1/www/loot/sam```

## Requirements

* Install **Impacket**: ```sudo apt-get install python-impacket``` or download and install from https://github.com/SecureAuthCorp/impacket
* **secretsdump.py** from the Impacket examples folder should be located in: ```/usr/local/bin/secretsdump.py``` (should already be there in kali linux)
* 7z

## Configuration

* Copy the **extract-sam-system-security.sh** script to ```/usr/local/P4wnP1/scripts/extract-sam-system-security.sh```
* Create disk using genimg: ```/usr/local/P4wnP1/helper/genimg -i -s 50 -o 50mb -l sam```
* You need to setup P4wnP1 USB Gadget Settings as Keyboard and Mass Storage and mount the disk you created
* Create a trigger action that starts the bash script **"extract-sam-system-security.sh"**  when USB gadget connected to host
