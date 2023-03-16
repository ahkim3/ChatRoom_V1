# Name: Andrew Kim
# Pawprint: AHKYQX
# Date: 3/14/2023
# Description: Implements server side of a chatroom. Facilitates communication between multiple clients, including login, newuser, send, and logout functions.


import socket
import sys
import os.path

bufsize = 1024  # Max amount of data to be received at once
users_file = "users.txt"  # File to store user credentials

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

clients = []  # List of connected clients
logged_in_users = {}  # Dictionary of logged in users, with their usernames as keys


# Check if user is logged in
def is_logged_in(client):
    return client in clients and client in logged_in_users.values()


# Check if user credentials are valid
def is_valid_credentials(username, password):
    # Grab user credentials from file
    with open(users_file, "r") as f:
        data = [tuple(line.strip().replace(
            "(", "").replace(")", "").split(", ")) for line in f]

    # Check for a match
    for user, passwd in data:
        if user == username and passwd == password:
            return True
    return False


# Create a new user account
def create_new_user(username, password):
    with open(users_file, "a") as f:
        f.write(f"\n({username}, {password})")

    print("New user account created.")


try:
    print("My chat room server. Version One.\n")
    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)

        while True:
            data = conn.recv(bufsize).decode().strip()
            if not data:
                continue

            # Parse command and parameters
            parts = data.split()
            command = parts[0].lower()
            params = parts[1:]

            # Handle login command
            if command == "login":
                username, password = params

                try:
                    if is_valid_credentials(username, password):
                        logged_in_users[conn] = username
                        conn.send(b"login confirmed")
                        print(username, "login.")
                    else:
                        conn.send(
                            b"Denied. User name or password incorrect.")
                except FileNotFoundError:
                    conn.send(
                        b"The users.txt file does not exist. Please create a newuser.")

            # Handle newuser command
            elif command == "newuser":
                username, password = params

                # Create file if it does not exist
                if not os.path.exists(users_file):
                    with open(users_file, "w") as f:
                        pass

                # Check if user already exists
                if is_valid_credentials(username, password):
                    conn.send(
                        b"Denied. User account already exists.")
                else:
                    create_new_user(username, password)
                    conn.send(b"New user account created. Please login.")

            # Handle logout command
            elif command == "logout":
                username = logged_in_users[conn]
                del logged_in_users[conn]
                print(username, "logout.")
                conn.close()
                clients.remove(conn)
                break

            # Handle send command
            elif command == "send":
                username = logged_in_users[conn]
                message = " ".join(params)
                conn.send(f"{username}: {message}".encode())
                print(username, ": ", message, sep="")

            # Handle invalid command
            else:
                conn.send(b"Invalid command.")

except KeyboardInterrupt:
    print("\nClosing server...")
    server_socket.close()
    sys.exit()
