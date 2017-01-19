'''
Contains all the client GUI classes

@author Chris Doherty
'''

import tkinter as tk

''' 
Represents the input field specifically for the Chatter app
'''       
class Input(tk.Frame):
    ''' Makes the internal data available.'''
    text = None
    
    ''' The entry widget '''
    entry_ = None
    
    ''' 
    Creates the entry widget and fills the frame with it.
    '''
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)
        
        # Colour same colour as an entry.
        super().configure(background = "white", bd = 0, padx = 5, pady = 5)
        
        # Configure rows and columsn weight
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        
        # StrinVar object to hold the input.
        self.text = tk.StringVar()
        
        # Create outselves an entry object and fille the entire frame
        self.entry_ = tk.Entry(self, bd = 0, textvariable = self.text)
        self.entry_.grid(column = 0, row = 0, sticky = (tk.W, tk.E))
    
    ''' 
    Provides interface to configure underlying entry field
    '''
    def configure_entry(self, **kw):
        self.entry_.configure(kw)

''' 
Represents the received messages window
'''
class ReceivedMessagesWindow(tk.Text):
    ''' 
    Sets up the look and feel of the text box. 
    '''
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        
        self.configure(
            width = 100, 
            height = 20,
            bg = '#EEE',
            bd = 0,
            padx = 5,
            pady = 5,
            relief = tk.FLAT,
            spacing2 = 2,
            state = tk.DISABLED,
            wrap = tk.WORD)
    
    ''' 
    Appends a new message to the received messages window
    '''
    def append_message(self, message, raw = False):
        message = message if raw else "\n%s" % message
        
        self.configure(state = tk.NORMAL)
        self.insert(tk.END, message)
        self.configure(state = tk.DISABLED)
        self.see(tk.END)
        
''' 
The client GUI object
'''
class GUI(tk.Tk):
    ''' Main frame object/widget '''
    window_frame_ = None
    
    ''' Input received from the text box '''
    input = None
    
    ''' The received messages window holding all received messages '''
    received_messages = None
    
    ''' 
    Creates the GUI app 
    '''
    def __init__(self, title):
        tk.Tk.__init__(self)
        
        # Setup title and stop resizing of the window
        self.title(title)
        self.resizable(0, 0)
            
        # Create the main frame. 
        self.window_frame_ = tk.Frame(self)
        self.window_frame_.grid(column = 0, row = 0, sticky = (tk.N, tk.S, tk.E, tk.W))
        
        self.received_messages = ReceivedMessagesWindow(self.window_frame_)
        
        # Add entry for user to send new messages.
        self.input = Input(self.window_frame_)
        self.input.configure_entry(font = self.received_messages.cget("font"))
        
        # Position everything.
        self.received_messages.grid(column = 0, row = 0, sticky = (tk.N, tk.S, tk.E, tk.W))
        self.input.grid(column = 0, row = 1, sticky = (tk.W, tk.E))
        
        self.update()
        
        # Position window in centre of screen.
        w = self.winfo_width() # Window width after widgets added
        h = self.winfo_height() # Window height after widgets added.
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight()

        self.geometry('%dx%d+%d+%d' % (w, h, ((ws/2) - (w/2)), ((hs/2) - (h/2))))
    
    '''
    Displays a new message on screen. 
    
    @param message A string message to be displayed.
    '''
    def display_message(self, message):
        print("[GUI] Displaying new message")
        self.received_messages.append_message(message)
    
    ''' 
    Starts the GUI 
    '''
    def run(self):
        self.mainloop()
        