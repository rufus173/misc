import socket
#class for connection
#class for gui (maybe if i get round to it)
class remote_connection:
    def __init__(self) -> None:
        self.socket_server = socket.socket()
        self.socket_server.bind(("192.168.1.141",8017))
        self.socket_server.listen(1)
        connection, address = self.socket_server.accept()
        self.server = connection
        self.handshake(["based"])
    def handshake(self,buffer):
        self.server.sendall(b"_")
        self.server.recv(1024)
        send_buffer = buffer
        for i in send_buffer:
            self.server.sendall(i.encode())
            self.server.recv(1024)
        self.server.sendall(b"&end")
remote_connection()