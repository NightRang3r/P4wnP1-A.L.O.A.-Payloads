# HostScan for P4wnP1-A.L.O.A

Author: NightRanger

## Description

Perform an Nmap scan of the host and save the results to the loot folder `/usr/local/P4wnP1/www/loot/scans`

## Requirements

You need to have nmap installed: `apt-get install nmap`

## Configuration

- Copy the **"hostscan.sh"** script to `/usr/local/P4wnP1/scripts/hostscan.sh`

- You need to setup P4wnP1 USB Gadget Settings as RNDIS_ETHERNET for Windows or CDC ECM on Mac/\*nix
- Create a **trigger action** to start the bash script **"hostscan.sh"** when DHCP lease issued.
