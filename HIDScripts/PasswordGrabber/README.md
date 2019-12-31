# PasswordGrabber

Author: NightRanger

Credits: 


jdebetaz: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/credentials/PasswordGrabber


# Description

Use ["LaZagne"](https://github.com/AlessandroZ/LaZagne) to retrieve lots of passwords stored on a local computer.
To avoid detection by windows defender the script will attempt to disable it using the **"Disable Security.js"** code which you can find [here](https://github.com/NightRang3r/P4wnP1-A.L.O.A.-Payloads/tree/master/HIDScripts/Disable%20Security)



## Requirements


* Create disk using genimg: ```/usr/local/P4wnP1/helper/genimg -i -s 50 -o passwords -l passwords```
* Copy the **"tools"** directory from this repository to the "passwords" disk


## Configuration

* Copy the **"PasswordGrabber.js"** script to ```/usr/local/P4wnP1/HIDScripts/PasswordGrabber.js```

* You need to setup P4wnP1 USB Gadget Settings as Keyboard and Mass Storage and mount the "passwords" disk you created
* Create a trigger action that starts the HID script "PasswordGrabber.js" when USB gadget connected to host
