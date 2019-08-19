import socket
import sys


host = '134.141.244.70'
port = 28888
s = socket.socket()
s.connect((host, port))
print('Connection established ')

while True:
    cmd = input()
    if cmd == 'quit':
        s.close()
        sys.exit()
    if len(cmd) > 0:
        s.send(str.encode(cmd))
        output = str(s.recv(1024),'utf-8')
        print(output, end='')
