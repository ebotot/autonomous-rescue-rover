# The server program is designed to be run on the base station (can be a laptop)
# It will wait and receive messages coming from the rover's Raspberry Pi
# Written with Python 3.9.0

import socket

# IP and port the program will be connecting to
# TODO: instead of hard-coding let user select
host = "127.0.0.1"
port = 62522


# This function will be used to initially connect to the socket
# Returns the 'connection' tuple
def connect():
    server = socket.socket() # create socket object
    server.connect((host,port))

    print("Server socket connected")
    reader = server.makefile('r') # create read file object for output
    return (server, reader) # return tuple of both socket and file object


# This function will be used to disconnect from both socket and file object
# Takes in the 'connection' tuple
def disconnect(connection: 'connection'):
    # separate the tuple for ease of use
    server = connection[0]
    reader = connection[1]
    
    server.close()
    reader.close()
    print("Server socket disconnected")


# This function will be used to read a message from the socket
# Done by reading a line from the read file object returned in connect()
def read(reader: 'file object'):
    return reader.readline()


# TODO: refactor so that UI is in a separate function instead of main body!
if __name__ == '__main__':
    connection = connect()
    # separate the tuple for ease of use
    server = connection[0]
    reader = connection[1]

    while True: # waits for data indefinitely
        print("Waiting for data")
        data = read(reader)

        if data == "exit": # stops when "exit" is sent
            break
        else:
            print(data) # prints out message to standard output

    disconnect(connection)
    
