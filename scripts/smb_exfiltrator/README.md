# SMB Exfiltrator for P4wnP1-A.L.O.A

Author: NightRanger

Firmware: v0.1.0-alpha2

## Description

Exfiltrate files from an unlocked windows machine using SMB

Based on: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/exfiltration/smb_exfiltrator

Saves creds to the loot folder ```/usr/local/P4wnP1/www/loot/smb_exfiltrator```

## Requirements

* Install **Impacket**: ```sudo apt-get install python-impacket``` or download and install from https://github.com/SecureAuthCorp/impacket
* **smbserver.py** from the Impacket examples folder should be located in: ```/usr/local/bin/smbserver.py``` (should already be there in kali linux)
* 7z

## Configuration

* Copy the **smb_exfiltrator.sh** script to ```/usr/local/P4wnP1/scripts/smb_exfiltrator.sh```
* Copy the "smb_exfiltrator" directory from this repository  to ```/usr/local/P4wnP1/scripts/smb_exfiltrator/```
* You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID keyboard
* Create a trigger action that starts the bash script **"smb_exfiltrator.sh"**  when  DHCP lease issued.
