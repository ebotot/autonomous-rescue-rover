# The server program is designed to be run on the base station (can be a laptop)
# It will wait and receive messages coming from the rover's Raspberry Pi
# Written with Python 3.9.0

import socket

# IP and port of the server
# TODO: instead of hard-coding let user select
host = "0.0.0.0"
port = 62522


# This function will be used to initially connect to the socket
# Returns the 'connection' tuple
def connect():
    server = socket.socket() # create socket object
    server.bind((host,port)) # bind the tcp socket to an IP and port

    print("Server socket connected")
    return server # return tuple of socket object


# This function will be used to disconnect from both socket and file object
# Takes in the 'connection' tuple
def disconnect(connection: 'connection'):
    # separate the tuple for ease of use
    server = connection[0]
    client = connection[1]
    
    server.close()
    client.close()
    print("Server socket disconnected")


# This function will be used to read a message from the socket
# Takes the clientConnection object
def read(client: 'file object'):
    return client.recv(1024).decode()


# TODO: refactor so that UI is in a separate function instead of main body!
if __name__ == '__main__':
    server = connect()

    server.listen(); # listening for connection from client
    
    while True: # waits for data indefinitely
        print("Waiting for data")
        (clientConnection, clientAddress) = server.accept(); # accepting from all clients
        print (str(clientAddress) + " connected!")
        data = read(clientConnection)
        if data == "exit": # stops when "exit" is sent
            break
        elif not data:
            break
        else:
            print("data: " + data) # prints out message to standard output
            clientConnection.send("Received!") # sends ACK 

    disconnect((server, clientConnection))
    
