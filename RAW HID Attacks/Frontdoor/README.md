# HID covert channel frontdoor ("Ported" from P4wnP1 to P4wnP1 A.L.O.A)

### Video demo

[![P4wnP1 HID demo youtube](https://img.youtube.com/vi/MI8DFlKLHBk/0.jpg)](https://www.youtube.com/watch?v=MI8DFlKLHBk&yt:cc=on)

### HID frontdoor features

- Plug and Play install of HID device on Windows (tested on Windows 7 and Windows 10)
- Covert channel based on a raw HID device
- Pure **in memory PowerShell payload** - nothing is written to disk
- Synchronous data transfer with about 32KBytes/s (fast enough for shells and small file transfers)
- Custom protocol stack to handle HID communication and deal with HID data fragmentation
- HID based file transfer from P4wnP1 to target memory
- **Stage 0:** P4wnP1 sits and waits, till the attacker triggers the payload stage 1 (frequently pressing CAPS LOCK)
- **Stage 1:** payload with "user space driver" for HID covert channel communication protocols is **typed out to the target via USB keyboard**
- **Stage 2:** Communications switches to HID channel and gives access to a custom shell on P4wnP1. This could be used to upload and run PowerShell scripts, which are hosted on P4wnP1, directly into memory of the PowerShell process running on the target. This happens without touching disk or using network communications, at any time.

## Requirements

- Copy the "**frontdoor**" directory to `/usr/local/P4wnP1/scripts/`
- Copy the "**frontdoor.sh**" script to `/usr/local/P4wnP1/scripts/`
- chmod "**frontdoor.sh**" to allow execution: `root@kali:/usr/local/P4wnP1/scripts# chmod 755 frontdoor.sh`
- Copy the "**frontdoor.js**" to `/usr/local/P4wnP1/HIDScripts/frontdoor.js`

## Configuration

**Create a USB setting template with the following settings:**

- Keyboard
- Custom HID device
- Vendor ID: `0x1d6b`
- Product ID: `0x1347`
- Manufacturer Name: `MaMe82`
- Product Name: `P4wnP1 by MaMe82`
- Serial Number: `deadbeef1337`

You can change the vendor and product ID to your needs, but you have to change the values in the `frontdoor.js` script as well.
