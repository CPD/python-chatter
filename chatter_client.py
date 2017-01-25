'''
Main execution file.

@author Chris Doherty
'''

from chatter import Application as ChatterApp
import chatter_client_config

if __name__ == "__main__":
    # Run a client based on the configuration.
    ChatterApp().start_client(chatter_client_config.nickname, 
                              chatter_client_config.host, 
                              chatter_client_config.port)
    