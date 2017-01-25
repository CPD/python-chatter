# Python Chatter 
A live chat application for demonstrating to students, who have just started learning programming, how python can be used in a real application.

## About 
Python Chatter was developed as part of a STEM project by Chris Doherty. Its intended purpose is to aid as a fun collaborative exercise for students to participate in. Students must work as a team to figure out how to piece together functions such that their code works and they can connect to the Python Chatter server to talk with their friends across a class room network. 

## Pre-requisits 
The application was developed with the intention of being as dependent free as possible. 
1. Python 3.2.x.
1. Tkinter library (Client GUI, installed on Windows as part of 3.2.x)

## User Guide
The server and client are run from separate files, `chatter_server.py` and `chatter_client.py` respectively, to make it easy for the end user. The client launches using some command line arguments while the client requires some configuration before running.  It's not so obvious here, but we assume the `python` command points to Python 3.2

### Server
To start a server instance of Python Chatter run the following in a terminal replacing `host` and `port` with appropriate values (an example is provided). 

`python chatter_server.py host port`

`python chatter_server.py 127.0.0.1 8080`

### Client
To start a client we must alter the client configuration file `chatter_client_config.py` changing the three variables: `nickname`, `host`, and `port`. See each variables for explanations. Launching the client has been designed so it can be launched from the IDLE as used in many schools; this is because it's often students do not have command line access. Open the `chatter_client.py` file using the Python IDLE and run (F5). All debug will appear in the console window of the IDLE.

## Advice & Guidance
Any firewalls presnet on each machine must allow data to pass through the specified port. In the event there's an ambitious attempt to send data across networks the network should be set up appropriately (consult your tech team). 

Watching the console output gives a good indication of what's going on both server and client side. Typically, once you boot the client, you can type a message and see if it gets displayed. If you don't see a message pop up check the client console window to see if there was an error connecting to the server. 