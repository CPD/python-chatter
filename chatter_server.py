'''
Main execution file.

@author Chris Doherty
'''

from argparse import ArgumentParser
from chatter import Application

if __name__ == "__main__":    
    # Define the argument parser and associated arguments for the application
    arg_parser_ = ArgumentParser(description = "Python Chatter -> A nifty live chat app :-)")
    
    arg_parser_.add_argument(
        'host', 
        action = 'store',
        help = 'The host IP address to [run a server|connect a client]')
    
    arg_parser_.add_argument(
        'port',
        action = 'store',
        type = int,
        help = 'The port number used by the [server|client]')
    
    args = arg_parser_.parse_args()
    
    # Run the server object
    Application().start_server(args.host, args.port)
    