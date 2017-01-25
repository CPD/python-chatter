'''
Contains all classes for the client logic code.

@author Chris Doherty
'''

import tkinter as tk
from datetime import datetime

'''
This object patches the client socket manager with the client GUI. It's sort of like a man-in-the-
middle.

We do this to separate out logic in the GUI from managing the socket. 
'''
class Controller(object):
    ''' Reference to teh gui object '''
    gui_ = None
    
    ''' Reference to the client logic logic '''
    client_ = None
    
    ''' Nickname of the user '''
    nickname_ = None
    
    ''' Initialises internal values '''
    def __init__(self, nickname, client, gui):
        self.nickname_ = nickname
        self.client_ = client
        self.gui_ = gui
        
        self.client_.closing_callback = self.handle_close
        self.client_.received_message_callback = self.handle_received_message
        
        self.gui_.input.entry_.bind('<Return>', lambda event: self.handle_input(
            self.gui_.input.text))
        
        self.gui_.protocol("WM_DELETE_WINDOW", self.handle_close)
        
        self.client_.connect()
        self.client_.send_message(bytes("%s has connected" % (self.nickname_), 'UTF-8'))
    
    ''' 
    Everything is technically initialised - we just want to run the GUI up and start listening for
    incoming messages.
    '''
    def init(self):
        print("[Controller] Init - starting GUI and Client")
        self.client_.start()
        
        self.gui_.received_messages.append_message("Welcome to Chatter App", True)
        self.gui_.received_messages.append_message("======================")
        self.gui_.run()
    
    ''' 
    Kills the client all together.
    '''
    def stop(self):
        self.handle_close()
    
    ''' 
    Handler for window closing
    '''
    def handle_close(self):
        self.client_.send_message(bytes("%s has disconnected" % (self.nickname_), 'UTF-8'))
        self.client_.disconnect()
        
        # Stop exceptions spamming the console when we close
        try:
            self.gui_.destroy()
        except Exception:
            pass
    
    ''' 
    Handles input into the Entry widget in the GUI
    
    @param message The StringVar object from the GUI
    '''
    def handle_input(self, message):
        print("[Controller] Handling input")
        self.client_.send_message(bytes("%s: %s" % (self.nickname_, message.get()), 'UTF-8'))
        message.set("")
        
    '''
    Handles a new message. This class expects the message parameter to be a string - not bytes. 
    It will pass the message to the GUI for presentation.
    
    @param message The message to be displayed
    '''
    def handle_received_message(self, message):
        print("[Controller] Handling new message")
        time = datetime.now()
        self.gui_.display_message("[%d:%d] %s" % (time.hour, time.minute, message.decode('UTF-8')))


import socket
from chatter.client.gui import GUI
from threading import Thread

'''
Represents the client connection to a server. This object will listen for new messages coming in
on the socket as well as send any messages we need it to, to the server
'''
class Client(Thread):
    ''' The receive buffer size, we read this number of bytes in at most per read '''
    RECV_BUFF_SIZE = 1024
    
    ''' Host address to connect to '''
    host_ = None
    
    ''' Port number to connect on '''
    port_ = None
    
    ''' The socket used to send and receive messages '''
    socket_ = None
    
    ''' Flag indicating running of thread status '''
    running_ = True
    
    ''' Callback for when a new message is received '''
    received_message_callback = None
    
    ''' Callback for when we're closing down '''
    closing_callback = None
    
    '''
    Initialises the socket class.
    
    @param host IP address to connect to
    @param port Port number to connect to
    @param timeout Timeout for connection to establish
    '''
    def __init__(self, host, port):
        Thread.__init__(self)
        
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ = host
        self.port_ = port
        
    '''
    Connects the socket to the server
    '''
    def connect(self):
        try:
            self.socket_.connect((self.host_, self.port_))
        except Exception as e:
            print("[Client] Couldn't connect")
            print("[Client] Error: %s" % e.strerror)
       
    ''' 
    Disconnects the socket from the server
    ''' 
    def disconnect(self):
        try:
            self.running_ = False
            
            if self.socket_ != None:
                print("[Client] Disconnecting")
                self.socket_.shutdown(socket.SHUT_RDWR)
                self.socket_.close()
                self.socket_ = None
        except socket.error:
            pass

    '''
    Sends a message down the socket. This attempts to send all data. Should it fail - an error is 
    printed to the console
    
    @param message The message to be sent in bytes
    '''
    def send_message(self, message):
        if self.socket_ != None: 
            try:
                print("[Client] Sending message")
                self.socket_.sendall(message)
            except socket.error:
                print("[Client] Error when sending message")
            
    '''
    Listens for new messages coming in. Should not be called directly as this operates in a 
    separate thread. Use the Client.start() method to start the client.
    '''    
    def run(self):
        print("[Client] Listening for incoming messages")
        # We want to constantly try to read data out of the socket.
        while self.running_:
            try: 
                # Socket still present but not being seen as a socket or its closed?
                message = self.socket_.recv(self.RECV_BUFF_SIZE)
                
                # We don't want to handle blanks 
                if message == b'':
                    continue
                
                print("[Client] Received new message")
                
                self.received_message_callback(message)
            except Exception:
                print("[Client] Uh oh... something went wrong receiving a message")
                self.running_ = False
                
                if self.closing_callback != None:
                    self.closing_callback()
        