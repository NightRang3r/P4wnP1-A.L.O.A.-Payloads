# QuickCreds for P4wnP1-A.L.O.A

Author: NightRanger

Credits: 

Mubix: https://malicious.link/post/2016/snagging-creds-from-locked-machines/

Hak5Darren: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/QuickCreds
Firmware: v0.1.0-alpha2

## Description

Snags credentials from locked or unlocked machines using responder, Based on the attack by Mubix of Room362.com

Saves creds to the loot folder ```/usr/local/P4wnP1/www/loot/quickcreds```

## Requirements

You need to have responder installed: ```apt-get install responder```


## Configuration

* Copy the **"QuickCreds.sh"** script to ```/usr/local/P4wnP1/scripts/QuickCreds.sh```

* You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET for Windows or CDC ECM on Mac/*nix
* Create a **trigger action** to start the bash script **"QuickCreds.sh"** when DHCP lease issued.
* In network settings add the following DHCP option for interface "usbeth": ```Option number: 252 Option string: http://172.16.0.1/wpad.dat```

![alt text](https://raw.githubusercontent.com/NightRang3r/P4wnP1-A.L.O.A.-Payloads/master/scripts/QuickCreds/Capture.JPG)
