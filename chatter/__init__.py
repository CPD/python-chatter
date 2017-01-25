'''
Entry code for the app

@author Chris Doherty
'''

from argparse import ArgumentParser
from chatter.server import Server 
from chatter.client import Client 
from chatter.client import Controller 
from chatter.client.gui import GUI

'''
The py entry point for the application.
'''
class Application(object):    
    '''
    Creates a new server using the specified arguments.
    
    @param host The host address for the server to bind to.
    @param port The port for the server to bind to.
    '''
    def start_server(self, host = 'localhost', port = 8080):
        try:
            server = Server(host, port)
            server.run()
        except KeyboardInterrupt:
            server.stop()
    
    '''
    Creates a new client instance and connects it to a server.
    
    @param nickname The nickname for the client to use.
    @param host The host address running the server.
    @param port The port the server is listening on.
    '''
    def start_client(self, nickname, host = 'localhost', port = 8080):
        try:
            gui = GUI("Chatter")
            client = Client(host, port)
            controller = Controller(nickname, client, gui)
            controller.init()
        except KeyboardInterrupt:
            controller.stop()