# SMBrute for P4wnP1-A.L.O.A

Author: NightRanger

Firmware: v0.1.0-alpha2

## Description

Brute force a locked windows machine login  via SMB , Tested on Win10.

Based on the P4wnP1 lockpicker and Bash Bunny Jackalope :

https://pentestit.de/smb-brute-force-mit-p4wnp1-a-l-o-a/ 

https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/Jackalope



Saves creds to the loot folder ```/usr/local/P4wnP1/www/loot/smbrute```



## Requirements

* nmap

* metasploit - ```apt-get install metasploit-framework```

* Copy the **wordlists** directory from this repository to ```/usr/local/P4wnP1/scripts/wordlists/```

  *Both should be installed on kali linux*

## Configuration

* Copy the **smbrute.sh** script to ```/usr/local/P4wnP1/scripts/smbrute.sh```
* You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET and HID Keyboard
* Create a trigger action that starts the bash script **"smbrute.sh"** when DHCP lease issued
