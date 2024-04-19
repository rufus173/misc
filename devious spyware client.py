import socket
import tkinter
import time
import tkinter.font
import threading
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
        return receive_buffer
class window(remote_connection):
    def __init__(self) -> None:
        super().__init__()
        self.outgoing_buffer = []
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
        self.stack_box = tkinter.LabelFrame(self.root,fg="green",bg="grey")
        self.stack_box.grid(row=0,column=2,rowspan=2,columnspan=1)
        self.stack_text = tkinter.Text(self.stack_box,fg="green",bg="black")
        self.stack_text.grid(row=0,column=0,sticky=tkinter.NSEW)
        
        #quick actions pannel
        self.quick_actions_frame = tkinter.LabelFrame(self.root,fg="green",bg="grey",text="quick actions")
        self.quick_actions_frame.grid(row=1,column=0,columnspan=2,sticky=tkinter.NSEW)
        self.shutdown_button = tkinter.Button(self.quick_actions_frame,
                                              fg="black",bg="grey",text="shutdown",
                                              command=lambda:self.quick_action(action="shutdown"))
        self.shutdown_button.grid(row=0,column=0,columnspan=1,sticky=tkinter.NSEW)
        self.ip_button = tkinter.Button(self.quick_actions_frame,
                                              fg="black",bg="grey",text="get ip",
                                              command=lambda:self.quick_action(action="ip address"))
        self.ip_button.grid(row=0,column=1,columnspan=1,sticky=tkinter.NSEW)
        
        #upkeep of the program
        threading.Thread(target=self.mainloop).start()
        self.root.mainloop()
    def mainloop(self):
        while True:
            time.sleep(0.5)
            self.incoming_buffer = self.handshake(self.outgoing_buffer)
            self.outgoing_buffer = []
            print(self.incoming_buffer)
            for i in self.incoming_buffer:
                self.stack_text.insert(tkinter.END,i)
            self.incoming_buffer = []
    def quick_action(self,action):
        print(action)
        self.stack_text.insert(tkinter.END,">>> "+action)
        match action:
            case "shutdown":
                self.outgoing_buffer.append("shutdown") 
            case "ip address":
                self.outgoing_buffer.append("ip address")
window()