# Roaster for P4wnP1-A.L.O.A

Author: NightRanger

Credits: golem445

https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Roaster

Firmware: v0.1.0-alpha2

## Description

Snags credentials from **unlocked machines** using **smbserver.py**, based on the BashBunny roaster payload.

Saves creds to the loot folder `/usr/local/P4wnP1/www/loot/roaster`

## Requirements

- Install **Impacket**: `sudo apt-get install python-impacket` or download and install from https://github.com/SecureAuthCorp/impacket
- **smbserver.py** from the Impacket examples folder should be located in: `/usr/share/doc/python3-impacket/examples/smbserver.py`

## Configuration

- Copy the **roaster.sh** script to `/usr/local/P4wnP1/scripts/roaster.sh`
- You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID Keyboard
- Create a trigger action that starts the bash script **"roaster.sh"** when DHCP lease issued
