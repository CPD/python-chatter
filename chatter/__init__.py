'''
Entry code for the app

@author Chris Doherty
'''

from argparse import ArgumentParser
from chatter.server import Server as ChatterServer
from chatter.client import Client as ChatterClient
from chatter.client import ClientController as ChatterController
from chatter.client.gui import GUI as ChatterGUI

'''
The chat entry point for the application.
'''
class Application(object):
    ''' 
    Container for the command line arguments (CLA)
    '''
    args_ = None
    
    ''' The argument parseing object '''
    arg_parser_ = None
    
    '''
    Controls the chat loop of the application.
    '''
    def run(self):
        self.parse_command_line_args_()
        
        if self.args_.app == 'client':
            if not self.args_.nickname:
                self.arg_parser_.error("You must enter a nickname when starting the client")
            else:
                self.setup_client_()
        elif self.args_.app == 'server':
            if not self.args_.host or not self.args_.port:
                self.arg_parser_.error(
                    "You must enter a --host and --port when starting the server")
            else:
                self.setup_server_()
        
        return 
    
    '''
    Sets the application up as a client
    '''
    def setup_client_(self):
        try:
            # We need a GUI, a Client object and a controller to manage them both.
            gui = ChatterGUI("Chatter")
            
            client = ChatterClient(self.args_.host, self.args_.port)
            
            controller = ChatterController(self.args_.nickname, client, gui)
            controller.init()
        except KeyboardInterrupt:
            controller.handle_close()
    
    ''' 
    Sets the application up as a server
    '''
    def setup_server_(self):
        try:
            server = ChatterServer(
                    self.args_.host,
                    self.args_.port)
            server.run()
        except KeyboardInterrupt:
            server.stop()
    
    '''
    Parses the command line arguments and puts them in the Application.CLA_ wrapper
    '''
    def parse_command_line_args_(self):
        # Define the argument parser and associated arguments for the application
        self.arg_parser_ = ArgumentParser(description = "Chatter -> A nifty chat app :-)")
        
        self.arg_parser_.add_argument(
            '--app', 
             action = 'store', 
             choices = ['client', 'server'],
             default = 'client',
             help = 'Do you want to start a server or client?')
        
        self.arg_parser_.add_argument(
            '--nickname',
            action = 'store',
            default = None,
            help = 'The nickname we want to use when connecting to the chat as a client')
        
        self.arg_parser_.add_argument(
            '--host', 
            action = 'store',
            default = 'localhost',
            help = 'The host IP address to [run a server|connect a client]')
        
        self.arg_parser_.add_argument(
            '--port',
            action = 'store',
            default = 8080,
            type = int,
            help = 'The port number used by the [server|client]')
        
        self.args_ = self.arg_parser_.parse_args()
        