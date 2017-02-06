'''
Created on 6 Feb 2017

@author Chris Doherty
'''

'''
This is called when the connection to the server has been established. When we connect, it would 
be good to let everyone else in the chat room know we have joined; we can do that here.

@param client The client object used to send new messages to the server. Can also be used to get
    some information such as your configured nickname
@param nickname The nickname we configured in our chatter_client_config.py module.
'''
def on_connect(client):
    print("[on_connect] You haven't completed me")

'''
When the user types a new message to send and hits the "enter" key we can manipulate the message
before it goes to the server. Use the "client" object to send the message

@param client The client object used to send new messages to the server. Can also be used to get
    some information such as your configured nickname.
@param message The message that was typed into the chat window. 
'''
def on_send_message(client, message):
    print("[on_send_message] You haven't completed me")

'''
When a new message is received we need to stamp it with a time and push it on to our screen. 
This function is called when a new message is received. 

Try using the "time" library to prepend a time to the received message.

@param client The client object used to send new messages to the server. Can also be used to get
    some information such as your configured nickname.
@param received_message The received message - sent by another user in the chat room.
'''
def on_received_message(client, received_message):
    print("[on_received_message] You haven't completed me")

'''
This is calle when we disconnect from the server. We should probably let everyone know we're
disconnecting by sending a message

@param client The client object used to send new messages to the server. Can also be used to get
    some information such as your configured nickname 
'''
def on_disconnect(client):
    print("[on_disconnect] You haven't completed me")