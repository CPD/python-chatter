'''
Created on 13 Jan 2017

@author Chris Doherty 
'''

from threading import Thread
from select import select
from time import sleep
import socket

''' 
ServerClient represents a connection from a client and monitors for incoming messages.
When new messages are received it requests the server broadcastst hem to all ServerClients.

The maximum message size is RECV_BUFF_SIZE so any messages longer than this may have undefined 
side affects.
'''
class ServerClient(Thread):    
    ''' The receive buffer size, we read this number of bytes in at most per read '''
    RECV_BUFF_SIZE = 1024
    
    ''' The socket we're sending/receiving data from. '''
    socket_ = None 
    
    ''' The clients address the socket is connected to '''
    client_address_ = None
    
    ''' A reference to the server object so we can broadcast messages. '''
    server_ = None
    
    ''' Flag indicating the status of the thread (running/not running) '''
    running_ = True
    
    '''
    Constructor
    '''
    def __init__(self, socket, client_address, server):
        Thread.__init__(self)
        
        self.socket_ = socket
        self.client_address_ = client_address
        self.server_ = server
        
        self.debug_("Initialised")
    
    ''' 
    Thread execution function. 
    
    Looks for new messages by blocking with socket.recv function.
    '''
    def run(self):
        # We want to constantly try to read data out of the socket.
        while (self.running_):
            try: 
                # Socket still present but not being seen as a socket or its closed?
                message = self.socket_.recv(self.RECV_BUFF_SIZE)
                
                # We don't want to handle blanks 
                if message == b'':
                    continue
                elif message == b'#disconnect#':
                    self.handle_disconnect()
                    continue
                
                self.debug_("Received a new message: %s" % message.decode('UTF-8'))
                
                self.handle_message(message)
            except Exception as e:
                print(e)
                self.debug_("Error... closing socket (%s, %d)" % self.client_address_)
                self.handle_disconnect()
    '''
    Handles clean disconnect of this server client
    '''
    def handle_disconnect(self):
        self.running_ = False
        self.server_.kill_and_remove_connection(self)
    
    ''' 
    Handles a new message. Generally it only needs to pass the message to the Server object for 
    broadcasting.
    
    @param message The message to be handled in bytes.
    '''
    def handle_message(self, message):
        self.server_.broadcast(message)
    
    ''' 
    Sends a message down the socket to the client. It is assumed the message is no longer than 
    1024 bytes as the clients don't attempt to receive anything larger (same on the server). 
    Messages longer than 1024 bytes will create buffering problems at the client end.
    
    @param message The message in bytes to be sent. 
    '''
    def send(self, message):
        self.debug_("Sending new message")
        self.socket_.sendall(message)
    
    '''
    Closes down the internal socket
    '''
    def close(self):
        self.debug_("Closing connection")
        self.running_ = False
        
        if self.socket_ != None:
            try:
                self.socket_.shutdown(socket.SHUT_RDWR)
                self.socket_.close()
            except Exception:
                pass
        
    ''' 
    Prints a debug message with client specific information
    
    @param message The debug message to be printed
    '''
    def debug_(self, message):
        print("[ServerClient %s:%d] %s" % (self.client_address_[0], self.client_address_[1], message))
        

''' 
ServerConnectionListener listens for new client connections in an independent thread. 
This allows us to braodcast any messages received by clients simaltaneously.

Every time we stop listening for new connections and want to start again, we must create a new 
instance of this class as threads SHOULDN'T be reused.
'''
class ServerConnectionListener(Thread):
    ''' The server socket '''
    socket_ = None
    
    ''' A reference to the server object '''
    server_ = None 
    
    ''' Flag to indicate status of listening for new connections '''
    listening_ = True
    
    ''' 
    Constructor
    
    @param socket A socket set upf or listening as a server
    '''
    def __init__(self, socket, server):
        Thread.__init__(self)
        self.socket_ = socket
        self.server_ = server
    
    ''' 
    Handles new inbound connections to the server socket
    '''
    def run(self):
        while self.listening_:
            client_socket, client_address = self.socket_.accept()
            self.server_.new_connection(client_socket, client_address)
    
    '''
    Stops us from listening for new connections. This will kill the thread and a new one must be 
    created to start listening again as you cannot reuse threads.
    '''
    def stop(self):
        self.listening_ = False

'''
Our actual server object. Opens up a socket that listens for new client connections.

We do not thread this class as we want the run method to run in the main thread keeping the 
whole application alive.
'''
class Server():
    ''' An array of clients connected to '''
    clients_ = set([])
    
    ''' Flag to listen for new connections '''
    server_listener_ = None
    
    ''' The sockett we're accepting connections on '''
    socket_ = None
    
    ''' Flag indicating running status of the server'''
    running_ = True
    
    '''
    Consrtuctor.
    Sets up parent and tells the server to serve requests until shutdown() is called.
    
    @param host IP address to use for the server
    @param port Port number to listen on.
    @param request_handler The handler that'll handle incoming messages.
    '''
    def __init__(self, host, port):
        # Setup server socket
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.bind((host, port))
        self.socket_.listen(10)
        
        print("[Server] Initialised on port '%d' using address '%s'" % (port, host))
        
    '''
    Sets the server in listening mode; i.e. accepting new client connections.
    '''
    def listen(self):
        if self.server_listener_ == None:
            print("[Server] Listening for new connections")
            self.server_listener_ = ServerConnectionListener(self.socket_, self)
            self.server_listener_.start()
    
    '''
    Stops the server from listening for new connections.
    '''
    def mute(self):
        self.server_listener_.stop()
        self.server_listener_ = None
        print("[Server] No longer lsitening for new connections")
    
    '''
    Registers a new connection internally.
    
    @param socket The newly create client socket
    @param address The clients address
    '''
    def new_connection(self, socket, address):
        print("[Server] Received a new connection")
        server_client = ServerClient(socket, address, self)
        server_client.start()
        self.clients_.add(server_client)
        
    '''
    Remvoes a connection, if it exists, from internal state.
    
    @param connection A ServerClient object to be removed.
    '''
    def remove_connection(self, connection):
        self.clients_.discard(connection)
        
    '''
    Attempts to kill a ServerClient before removing it from internal state.
    
    @param connection The client to be killed and removed
    '''
    def kill_and_remove_connection(self, connection):
        connection.close()
        self.remove_connection(connection)
        
    '''
    Broadcasts a message to all clients.
    
    @param message The message to be broadcast in bytes
    '''
    def broadcast(self, message):
        print("[Server] Broadcasing message")
        for client in self.clients_:
            client.send(message)
        
    
    ''' 
    Maintains state so we can send messages inside the main thread.
    '''
    def run(self):
        # Need to make sure we kick off listening.
        self.listen()
        
        # Loop to just hold state for the entire app.
        while self.running_:
            sleep(0.05)
        
        for client in self.clients_:
            client.close()
            
        print("[Server] Closing down")
        
    ''' 
    Stops the server from running. This will eventually ask all clients to close their connections
    before the program terminates. 
    '''
    def stop(self):
        self.mute()
        self.running_ = False
        