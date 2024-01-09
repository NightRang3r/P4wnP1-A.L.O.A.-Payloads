# HID covert channel backdoor ("Ported" from P4wnP1 to P4wnP1 A.L.O.A)

### DEMO

![](https://raw.githubusercontent.com/NightRang3r/P4wnP1-A.L.O.A.-Payloads/master/RAW%20HID%20Attacks/Backdoor/backdoor.gif)

### HID backdoor features

- Payload to bridge an Airgap target, by relaying a shell over raw HID and provide it from P4wnP1 via WiFi
- Plug and Play install of HID device on Windows (tested on Windows 7 and Windows 10)
- Covert channel based on raw HID
- Pure **in memory, multi stage payload** - nothing is written to disk, small footprint (compared to typical PowerShell IOCs)
- RAT like control server with custom shell:

  - Auto completition for core commands

  - Trigger remote backdoor to bring up HID covert channel
  - creation of **multiple** remote processes (only with covert channel connection)
  - console interaction with managed remote processes (only with covert channel connection)
  - auto kill of remote payload on disconnect
  - `shell` command to create remote shell (only with covert channel connection)
  - server could be accessed with SSH via WiFi

## Requirements

- Copy the "**backdoor**" directory to `/usr/local/P4wnP1/scripts/`
- Copy the "**backdoor.sh**" script to `/usr/local/P4wnP1/scripts/`
- chmod "**backdoor.sh**" to allow execution: `root@kali:/usr/local/P4wnP1/scripts# chmod 755 backdoor.sh`
- Copy the "**backdoor.js**" to `/usr/local/P4wnP1/HIDScripts/backdoor.js`

## Configuration

**Create a USB setting template with the following settings:**

- Keyboard
- Custom HID device
- Vendor ID: `0x1d6b`
- Product ID: `0x1347`
- Manufacturer Name: `MaMe82`
- Product Name: `P4wnP1 by MaMe82`
- Serial Number: `deadbeef1337`

_If you want to use other VID/PID you will need to update the values in backdoor.js and Stage1.ps1 (inside the backdoor folder)_

**Store the template under the name "backdoor"**

**Create a trigger action** that starts the bash script "backdoor.sh" when USB gadget connected to host, **Store the template under the name "backdoor"**

**Create a master template** with the following settings:

- TriggerActions Template: `backdoor`
- USB Template: `backdoor`
- WiFi Template: `startup`
- Bluetooth Template: `startup`
- Networks templates: `bteth_startup, usbeth_startup, wlan0_startup_dhcp_server`

## Execution

- Connect to the P4wnP1 A.L.O.A web interface (using the access point ip "172.24.0.1") and deploy the master template "**backdoor**"
- SSH into your P4wnP1 A.L.O.A access point ip "172.24.0.1" and run the following command: `root@kali:~# screen -d -r backdoor`
- To interact with the shell simply type: `shell`

```
Starting P4wnP1 server...
=================================
P4wnP1 HID backdoor shell
Author: MaMe82
Web: https://github.com/mame82/P4wnP1
State: Experimental (maybe forever ;-))

Enter "help" for help
Enter "FireStage1" to run stage 1 against the current target.
Use "help FireStage1" to get more details.
=================================

P4wnP1 shell (client connected) > shell
```
