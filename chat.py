'''
Main execution file.

@author Chris Doherty
'''

from chatter import Application as ChatterApp

if __name__ == "__main__":
    # Boot the application
    app = ChatterApp()
    app.run()
    