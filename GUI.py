#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from tkinter import messagebox
import pickle


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        
    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 600,
                             height = 500)
        self.login.configure(bg="#EEB4B4")
        
        
        # create a Label
        self.pls = Label(self.login, 
                       text = "PLEASE LOGIN TO CONTINUE",
                
                       justify = CENTER, 
                       font = "Helvetica 16 bold",
                       fg='#8B3A62')
        
          
        self.pls.place(relheight = 0.3,
                       relx = 0.35, 
                       rely = 0.001)
        self.pls.configure(bg="#EEB4B4")
        #8B0A50

        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 14 bold",
                               fg='#8B3A62')
          
        self.labelName.place(relheight = 0.3,
                             relx = 0.25, 
                             rely = 0.15)
        self.labelName.configure(bg='#EEB4B4')
       
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
        self.entryName.configure(bg="linen")
          
        # set the focus of the curser
        self.entryName.focus()
          
        #set label for password 
        self.labelPass = Label(self.login, text="Password:", font="Helvetica 14 bold", fg='#8B3A62')
        self.labelPass.place(relheight=0.3, relx=0.20, rely=0.35)

        self.labelPass.configure(bg='#EEB4B4')

        #create an entry box for typing the password 
        self.entryPass = Entry(self.login, show="*", font="Helvetica 14")
        self.entryPass.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4)
        self.entryPass.configure(bg="#FAF0E6")
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold",
                         command =self.goAhead,
                          bg = "#ABB2B9",
                           fg='#8B3A62' )
        #8B3A62
          
        self.go.place(relwidth=0.3, relheight=0.1, relx = 0.4,
                      rely = 0.6)
        #self.go.configure(bg="#FAF0E6")

        self.signup_button = Button(self.login, text="SIGN UP", font="Helvetica 14 bold", command=self.signup, bg='#FFC1C1',fg='#8B3A62')
        self.signup_button.place(relwidth=0.3, relheight=0.1, relx=0.4, rely=0.7)

      
        self.Window.mainloop()

    def authenticate_user(self, name, password):
        try:
            # Open the user credentials file and check if the provided username and password match any entry
            with open('user_credentials.txt', 'r') as file:
                for line in file:
                    username, stored_password = line.strip().split(':')
                    if username == name and stored_password == password:
                        return True  # Authentication successful
        
            # If no matching entry found, return False
            return False

        except FileNotFoundError:
            messagebox.showerror("Error", "User credentials file not found.")
            return False  # File not found
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return False  # Other error occurred
        
    def signup(self):
    # sign-up window
        self.signup_window = Toplevel()
        self.signup_window.title("SIGN UP")
        self.signup_window.resizable(width=False, height=False)
        self.signup_window.configure(width=400, height=300)

        # create labels and entry boxes for new username and password
        Label(self.signup_window, text="New Username:", font="Helvetica 12").place(relheight=0.2, relx=0.1, rely=0.2)
        self.new_username_entry = Entry(self.signup_window, font="Helvetica 14")
        self.new_username_entry.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.25)
        Label(self.signup_window, text="New Password:", font="Helvetica 12").place(relheight=0.2, relx=0.1, rely=0.4)
        self.new_password_entry = Entry(self.signup_window, show="*", font="Helvetica 14")
        self.new_password_entry.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.45)

        # create sign-up button
        Button(self.signup_window, text="SIGN UP", font="Helvetica 14 bold", command=self.register_new_user).place(relx=0.4, rely=0.7)

    def register_new_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        # check if the username already exists
        if self.check_username_exists(new_username):
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        # save new username and password to the text file
        with open("user_credentials.txt", "a") as file:
            file.write(f"{new_username}:{new_password}\n")

        messagebox.showinfo("Success", "User created successfully. You can now login with your new credentials.")
        self.signup_window.destroy()

        self.user[new_username] = new_password

    def check_username_exists(self, username):
        try:
            with open("user_credentials.txt", "r") as file:
                for line in file:
                    if line.startswith(username):
                        return True
        except FileNotFoundError:
            # If the file does not exist, return False
            return False
        return False
             
    def goAhead(self):
        name = self.entryName.get()
        password = self.entryPass.get()
        if len(name) > 0 and len(password) > 0:
            # Check if the user authentication is successful
            if self.authenticate_user(name, password):
                msg = json.dumps({"action": "login", "name": name, "password": password})
                self.send(msg)
                response = json.loads(self.recv())
                if response["status"] == 'ok':
                    self.login.destroy()
                    self.sm.set_state(S_LOGGEDIN)
                    self.sm.set_myname(name)
                    
                    self.layout(name)
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, "hello" + "\n\n")
                    self.textCons.insert(END, menu + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                else:
                # Display error message if authentication fails
                    messagebox.showerror("Authentication Failed", "Invalid username or password. Please try again.")
                    # Start a thread to receive messages
                process = threading.Thread(target=self.proc)
                process.daemon = True
                process.start()
            

  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#CD8C95") #big background 
        
        self.labelHead = Label(self.Window,
                             bg = "#CD8C95", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5,
                               bd=3,
                               relief=SOLID)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "linen") #Upper Line
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.002)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "linen",     #whole window
                             fg = "#8B5F65",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5,
                             bd = 3,
                            relief = SOLID)
          
        self.textCons.place(relheight = 0.85,
                            relwidth = 1, 
                            rely = 0.06)
          
        self.labelBottom = Label(self.Window,
                                 bg = "linen",
                                 height = 45)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.91)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#CD8C95",
                              fg = "#EAECEE",
                              font = "Helvetica 13",
                              bd = 3,
                              relief = SOLID)
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.78,
                            relheight = 0.05,
                            rely = 0.007,
                            relx = 0.011)
          
        self.entryMsg.focus()

        self.entryMsg.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))

          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "white",
                                fg='#8B475D',
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.8,
                             rely = 0.007,
                             relheight = 0.05, 
                             relwidth = 0.18)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, term):
        self.my_msg = term
        # print(msg)
        self.searchBar.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.send(json.dumps({"action": "search", "target": term}))
        msg = json.loads(self.recv())["results"]
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
    
    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = ""
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                
                self.textCons.insert(END, self.system_msg +"\n") 

                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()

# create a GUI class object
if __name__ == "__main__": 
    g = GUI()
    