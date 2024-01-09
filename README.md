# P4wnP1-A.L.O.A. Payloads

The scripts (for Windows and OSX), HIDScripts (for Windows) and RAW HID Attacks Scripts have been tested and verified. They've been adapted to integrate and work with my customized P4wnP1 Image. You'll find this repository pre-included in the root directory of the image. To ensure you have the latest version, execute a 'git pull' command once in a while.

If you plan to use this repository with a different image, be prepared to make the necessary adjustments to the scripts for compatibility.

You can get my cutom P4wnP1 Kali Linux 2023.1 image for Raspberry Pi 0W from [here](https://drive.google.com/drive/folders/14XCb1sHFjzZa7OnzNZRt5AeTbEyZlZGf?usp=sharing) or [here](https://mega.nz/folder/UWgClaID#IlDFij3ckSTR4EqTlzDh_Q)

- HID Scripts should be placed in `/usr/local/P4wnP1/HIDScripts`
- Shell scripts should be places in `/usr/local/P4wnP1/scripts`
- Loot directory will be created in: `/usr/local/P4wnP1/www/loot` and is accessible via browser at: `http://172.XX.0.1:8000/loot/`

**You can find the usage and requirements information in the comments inside each file**

# P4wnP1 A.L.O.A - Kali Linux 2023.1 Image for Raspberry Pi 0W

## Key Features

- **Boot Configuration**: Updated `boot.txt` and `config.txt` for to support P4wnP1 functionality.
- **Included Tools**:
  - Responder
  - Metasploit Framework
  - Impacket
  - Nmap
  - Aircrack-ng
  - MDK4
  - MSFPC
  - Python3-pymetasploit3
  - kali windows-binaries
  - `raspi-config` for easy filesystem expansion
  - python2
  - python3

## Pre-installed Python3 Libraries

- spidev
- Pillow
- luma.lcd
- luma.core
- luma.oled
- RPi.GPIO

## LCD/OLED Hat Support

- **LCD Menu**: [`P4wnP1_ALOA_LCD_MENU`](https://github.com/NightRang3r/P4wnP1_ALOA_LCD_MENU.git) - a modified version of this repository is included in the image in the root folder.
- **OLED Menu V2**: [`P4wnP1_ALOA_OLED_MENU_V2`](https://github.com/beboxos/P4wnP1_ALOA_OLED_MENU_V2.git) - a modified version of this repository is included in the image in the root folder, Adjustments may be needed for Python3.

You will need to initiate the `install.sh` script in the corresponding directory to install the lcd support.

## Exclusive Payloads

- [`P4wnP1-A.L.O.A.-Payloads`](https://github.com/NightRang3r/P4wnP1-A.L.O.A.-Payloads.git) - A collection of Payloads for P4wnP1 already included in the image in the root folder.

### Installation Guide

1. **Download**: Grab the image file from [https://drive.google.com/drive/folders/14XCb1sHFjzZa7OnzNZRt5AeTbEyZlZGf?usp=sharing](https://drive.google.com/drive/folders/14XCb1sHFjzZa7OnzNZRt5AeTbEyZlZGf?usp=sharing) or [https://mega.nz/folder/UWgClaID#IlDFij3ckSTR4EqTlzDh_Q](https://mega.nz/folder/UWgClaID#IlDFij3ckSTR4EqTlzDh_Q)
2. **Flash**: Use your preferred method to flash the image onto your Raspberry Pi 0W.
3. **Connect**: Access the Pi via SSH in USB Gadget Mode or Wifi AP Mode.
   - **USB Gadget Mode**:
     - SSH: `172.16.0.1`, Port: `22`
     - Web UI: `http://172.16.0.1:8000`
   - **Wifi AP Mode**:
     - SSID: 💥🖥💥 Ⓟ➃ⓌⓃ🅟❶
     - SSH: `172.24.0.1`, Port: `22`
     - Web UI: `http://172.24.0.1:8000`
   - **Credentials**: `root:toor`, WiFi Key: `MaMe82-P4wnP1`
4. **Expand Filesystem**: Run `raspi-config --expand-rootfs` and reboot to use the full SD card size.
5. **LCD/OLED Setup**: If you have a hat, navigate to the corresponding directory (in `/root`) and run `./install.sh`.
6. **Final Touch**: Create a new trigger action when service starts to run a bash script and select: `/usr/local/P4wnP1/scripts/runmenu.sh`, save it to the `startup` template in the P4wnP1 UI.
