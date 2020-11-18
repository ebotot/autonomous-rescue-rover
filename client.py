# The client program is designed to be run on the Raspberry Pi on the rover
# It will send messages back to the base station running on a laptop/PC
# Written with Python 3.9.0

import socket


# IP and port the program will be connecting to
# TODO: instead of hard-coding let user select
host = "127.0.0.1"
port = 62522


# This function will be used to initially connect to the socket
# Returns the 'connection' tuple
def connect():
    client = socket.socket() # create socket object
    client.connect((host,port))

    print("Client socket connected")
    writer = client.makefile('w') # create write file object for output
    return (client, writer) # return tuple of both socket and file object


# This function will be used to disconnect from both socket and file object
# Takes in the 'connection' tuple
def disconnect(connection: 'connection'):
    # separate the tuple for ease of use
    client = connection[0]
    writer = connection[1]
    
    client.close()
    writer.close()
    print("Client socket disconnected")

    
# This function will be used to send a message to the socket
# Done by writing to the file object returned in connect()
def write(writer: 'file object', message: str):
    writer.write(message + "\r\n")
    writer.flush()


# TODO: refactor so that UI is in a separate function instead of main body!
if __name__ == '__main__':
    connection = connect()
    # separate the tuple for ease of use
    client = connection[0]
    writer = connection[1]

    # TODO: maybe take user input instead of predefined message, could be useful later
    print("Sending message:")
    write(writer, "SAMPLE MESSAGE")
    print("Sending exit message:")
    write(writer, "exit")
        
    disconnect(connection)
    
