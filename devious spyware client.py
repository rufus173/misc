import socket
import tkinter
import tkinter.font
#class for connection
#class for gui (maybe if i get round to it)
class remote_connection:
    def __init__(self) -> None:
        self.socket_server = socket.socket()
        self.socket_server.bind(("192.168.1.141",8017))
        self.socket_server.listen(1)
        connection, address = self.socket_server.accept()
        self.server = connection
        self.handshake(["connected"])
    def handshake(self,buffer):
        self.server.sendall(b"_")
        self.server.recv(1024)
        send_buffer = buffer
        for i in send_buffer:
            self.server.sendall(i.encode())
            self.server.recv(1024)
        self.server.sendall(b"&end")
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
class window(remote_connection):
    def __init__(self) -> None:
        super().__init__()
        self.root = tkinter.Tk()
        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(size=18)
        self.root.title("control pannel")
        
        #terminal interaction box
        self.terminal_frame = tkinter.LabelFrame(self.root,text="terminal",fg="green",bg="grey")
        self.terminal_frame.grid(row=0,column=0,columnspan=1,sticky=tkinter.NSEW)
        self.submit_command_button = tkinter.Button(self.terminal_frame,text="submit command",fg="green",bg="black")
        self.submit_command_button.grid(row=0,column=0,columnspan=1,sticky=tkinter.NSEW)
        self.submit_command_entry = tkinter.Entry(self.terminal_frame,fg="green",bg="black")
        self.submit_command_entry.grid(row=1,column=0,columnspan=1,sticky=tkinter.NSEW)
        
        #status box
        self.status_frame = tkinter.LabelFrame(self.root,text="status",fg="green",bg="grey")
        self.status_frame.grid(row=0,column=1,sticky=tkinter.NSEW)
        self.status_label = tkinter.Label(self.status_frame,text="disconnected",fg="green",bg="black")
        self.status_label.grid(row=0,column=0,sticky=tkinter.NSEW)
        
        #the stack box (what is happening and the contents of the buffer)
        
        self.root.mainloop()
window()