# Name: Andrew Kim
# Pawprint: AHKYQX
# Date: 3/14/2023
# Description: Implements server side of a chatroom. Facilitates communication between multiple clients, including login, newuser, send, and logout functions.


import socket
import sys

bufsize = 1024  # Max amount of data to be received at once

# Set server IP address and port number
host = "127.0.0.1"
port = 19347

# Create socket
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Socket creation failed:", err)
    sys.exit()

# Bind the socket
try:
    server_socket.bind((host, port))
except socket.error as err:
    print("Binding failed:", err)
    sys.exit()

server_socket.listen(1)

client = None  # Keeps track of connected clients

try:
    print("Waiting for a client to connect...\n")
    conn, addr = server_socket.accept()
    client = conn
    print("Client Connected.")
    client.send(b"Welcome to the chatroom!")

    while True:
        # Receive data
        data = client.recv(bufsize)
        if data:
            # Broadcast data to client
            client.sendall(data)
        else:
            # Client disconnected
            print("Client Disconnected.")
            client.close()
            sys.exit()

except KeyboardInterrupt:
    print("\nClosing server...")
    if client:
        client.close()
    server_socket.close()
    sys.exit()

except socket.error as err:
    print("Socket error:", err)
    sys.exit()
