# Name: Andrew Kim
# Pawprint: AHKYQX
# Date: 3/14/2023
# Description: Implements client side of a chatroom. Facilitates communication between multiple clients, including login, newuser, send, and logout functions.


import socket
import sys

bufsize = 1024  # Max amount of data to be received at once

# Set server IP address and port number
host = "127.0.0.1"
port = 19347

# Create socket
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Socket creation failed.")
    sys.exit()

# Connect to server
try:
    client_socket.connect((host, port))
except:
    print("Unable to connect to server.")
    sys.exit()

client_socket.settimeout(1)


# Receive data from the server
def receive():
    while True:
        try:
            data = client_socket.recv(bufsize).decode()
            if not data:
                print("Server disconnected.")
                break
            print(data)
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print("\nClosing client...")
            client_socket.close()
            sys.exit()
        except socket.error as err:
            print("Socket error:", err)
            client_socket.close()
            sys.exit()


# Send data to the server
def send():
    while True:
        try:
            data = input()
            client_socket.send(data.encode())
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print("\nClosing client...")
            client_socket.close()
            sys.exit()
        except socket.error as err:
            print("Socket error:", err)
            client_socket.close()
            sys.exit()


# Start sending and receiving data
while True:
    try:
        receive()
        send()
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        print("\nClosing client...")
        client_socket.close()
        sys.exit()
    except socket.error as err:
        print("Socket error:", err)
        client_socket.close()
        sys.exit()
