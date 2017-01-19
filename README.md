# Python Chatter 
A live chat application for demonstrating to students, who have just started learning programming, how python can be used in a real application.

# About #
Python Chatter was developed as part of a STEM project by Chris Doherty. Its intended purpose is to aid as a fun collaborative exercise for students to participate in. Students must work as a team to figure out how to piece together functions such that their code works and they can connect to the Python Chatter server to talk with their friends across a class room network. 

# Pre-requisits 
1. Python 3.2.x. Python Chatter was written and tested using Python 3.2.x. 
1. Tkinter library must be available

# User Guide
The application boots with a few easy commands straight from the `chat.py` file. The arguments differ depending on whether you boot a client or a server. It's not so obvious here, but we assume the `python` command points to Python 3.2

To start a server instance of Python Chatter run the following:

`python chat.py --app=server --host=[HOST] --port=[PORT]`

To start a client instance of Python Chatter run the following:

`python chat.py --nickname="Chris Doherty" --host=[HOST] --port=[PORT]`


The client boots by default so the `--app` argument isn't needed; although you can explicitly use it (`--app=client`). Host and port are required for both server and client. This is PC dependent but in all cases make sure your firewall(s) let the connection through.

Watching the console output gives a good indication of what's going on both server and client side. Typically, once you boot the client, you can type a message and see if it gets displayed. If you don't see a message pop up check the client console window to see if there was an error connecting to the server. 
