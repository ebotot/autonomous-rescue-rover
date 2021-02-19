# The client program is designed to be run on the Raspberry Pi on the rover
# It will send messages back to the base station running on a laptop/PC
# Written with Python 3.9.0

import socket
import gps

# IP and port the program will be connecting to
# TODO: instead of hard-coding let user select
host = "DESKTOP-PHEPU7Q"
port = 62522


# This function will be used to initially connect to the socket
# Returns the client object
def connect():
    client = socket.socket() # create socket object
    client.connect((host,port))

    print("Client socket connected")
    return client # return tuple of socket object


# This function will be used to disconnect from both socket and file object
# Takes in the 'connection' tuple
def disconnect(client: 'connection'):
    client.close()
    print("Client socket disconnected")

    
# This function will be used to send a message to the socket
# Done by writing to the file object returned in connect()
def write(client: 'file object', message: str):
    client.send(message.encode())
    ack = client.recv(1024).decode() # to receive the ACK
    print(ack)


# TODO: refactor so that UI is in a separate function instead of main body!
if __name__ == '__main__':
    client = connect()

    # Listen on port 2947 (gpsd) of localhost
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    while True:
        try:
            report = session.next()
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print(report)
            if report['class'] == 'TPV':
                if hasattr(report, 'time'):
                    write(client, report.time)
                    print(report.time)
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print("GPS collection terminated")
        
    disconnect(connection)
    
