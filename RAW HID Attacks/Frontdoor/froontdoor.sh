#!/bin/bash

if ! ps -aux | grep hidserver.py | grep -q -v grep; then
        echo "[*] Start hidserver..."
        touch /tmp/device_hid_mouse
        screen -dmS hidsrv bash -c "python2 /usr/local/P4wnP1/legacy/frondoor/hidserver.py"

        echo "[+] Type \"screen -d -r hidsrv\" to switch to backdoor cli"
else
        echo "[!] HID covert channel server already running"
fi

