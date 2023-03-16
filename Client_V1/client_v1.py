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

# User is not logged in by default
logged_in = False


# Receive data from the server
def receive():
    try:
        data = client_socket.recv(bufsize).decode()
        if not data:
            print("Server disconnected.")
            client_socket.close()
            sys.exit()

        if data == b"login confirmed" or data == "login confirmed":
            global logged_in
            logged_in = True

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
    try:
        # Get user input
        data = input()

        # Parse command and parameters
        parts = data.split()
        params = parts[1:]

        # If user is not logged in, only allow login and newuser commands
        if not logged_in:
            if data.startswith("login") or data.startswith("newuser"):
                # Check if login command is used correctly
                if data.startswith("login"):
                    if len(params) != 2:
                        print("Invalid usage. Usage: login <username> <password>")
                        return

                # Check if newuser command is used correctly
                elif data.startswith("newuser"):
                    username, password = params

                    if len(params) != 2:
                        print("Invalid usage. Usage: newuser <username> <password>")
                        return

                    if len(username) < 3 or len(username) > 32:
                        print(
                            "Invalid username length (must be between 3 and 32 characters).")
                        return

                    if len(password) < 4 or len(password) > 8:
                        print(
                            "Invalid password length (must be between 4 and 8 characters).")
                        return

                    if any(c.isspace() for c in username) or any(c.isspace() for c in password):
                        print("Username and password cannot contain spaces.")
                        return

                # Valid input; send command to server
                client_socket.send(data.encode())
            else:
                if data.startswith("send") or data.startswith("logout"):
                    print("Denied. Please login first.")
                else:
                    print("Invalid command.")
        else:
            if data.startswith("send") or data.startswith("logout"):
                # Check if send command is used correctly
                if data.startswith("send"):
                    message = ' '.join(params)

                    if len(params) <= 0:
                        print("Invalid usage. Usage: send <message>")
                        return

                    if len(message) > 256 or len(message) < 1:
                        print(
                            "Invalid message length (must be between 1 and 256 characters).")
                        return

                    client_socket.send(data.encode())

                # Check if logout command is used correctly
                elif data.startswith("logout"):
                    client_socket.send(data.encode())
                    client_socket.close()
                    sys.exit()
            else:
                if data.startswith("login") or data.startswith("newuser"):
                    print("Denied. Please logout first.")
                else:
                    print("Invalid command.")
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


print("My Chat room client. Version One.\n")

# Start sending and receiving data
while True:
    try:
        send()
        receive()

    except socket.timeout:
        print("Socket timeout.")
        pass
    except KeyboardInterrupt:
        print("\nClosing client...")
        client_socket.close()
        sys.exit()
    except socket.error as err:
        print("Socket error:", err)
        client_socket.close()
        sys.exit()
