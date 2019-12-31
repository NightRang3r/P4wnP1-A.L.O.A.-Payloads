# Quickdraw for P4wnP1-A.L.O.A

Author: NightRanger

Credits:  golem445

 https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Quickdraw

Firmware: v0.1.0-alpha2

## Description

Snags credentials from **unlocked machines** using responder, based on the BashBunny Quickdraw payload

Saves creds to the loot folder ```/usr/local/P4wnP1/www/loot/quickdraw```

## Requirements

You need to have responder installed: ```apt-get install responder```


## Configuration

* Copy the **"Quickdraw.sh"** script to ```/usr/local/P4wnP1/scripts/Quickdraw.sh```

* You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID Keyboard
* Create a trigger action that starts the bash script **"Quickdraw.sh"** when DHCP lease issued
