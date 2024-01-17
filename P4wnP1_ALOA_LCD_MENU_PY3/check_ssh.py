import socket
import subprocess
import time

def check_ssh_service(port=22):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_script(script_path):
    subprocess.Popen(["python3", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Usage
print("Waiting for SSH service to be up...")
while not check_ssh_service():
    time.sleep(5)  # wait for 5 seconds before checking again

print("SSH service is up on the local machine. Running the script now.")
run_script("/root/BeBoXGui/runmenu.py")
