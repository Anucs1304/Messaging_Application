# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import threading
from fileTransfer import send_file
from contactManager import add_contact, remove_contact, view_contacts

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) == 3: 
    print("Usage: python client.py <IP> <PORT>")
    sys.exit()


IP_address = "192.168.178.88"
Port = 12345


server.connect((IP_address, Port)) 

print(server.recv(1024).decode())  # reads: "Enter login or register"

# login/register
print("Do you want to 'login' or 'register'?")
mode = input(">> ").strip()
username = input("Username: ").strip()
password = input("Password: ").strip()

server.send(mode.encode())
server.recv(1024)  # Wait for "Username:" prompt
server.send(username.encode())
server.recv(1024)  # Wait for "Password:" prompt
server.send(password.encode())

auth_response = server.recv(1024).decode()
print(auth_response)

if "successful" not in auth_response.lower():
    print("Authentication failed. Closing connection.")
    server.close()
    sys.exit()


# Function to handle user input in a separate thread
def handle_input():
    while True:
        message = sys.stdin.readline()
        if message.strip().lower() == "/exit":
            print("Exiting chat...")
            server.close()
            sys.exit()

        elif message.startswith("/file "):
            filepath = message.split("/file ", 1)[1]
            send_file(server, filepath)

        elif message.startswith("/add "):
            parts = message.strip().split(" ", 1)
            if len(parts) < 2:
                print("Usage: /add <username>")
                continue
            username = parts[1]
            add_contact(username)

        elif message.startswith("/remove "):
            parts = message.strip().split(" ", 1)
            if len(parts) < 2:
                print("Usage: /remove <username>")
                continue
            username = parts[1]
            remove_contact(username)

        elif message == "/contacts":
            view_contacts()

        else:
            server.send(message.encode())
            sys.stdout.write("<You> " + message + "\n")
            sys.stdout.flush()
       

# Start the input thread
input_thread = threading.Thread(target=handle_input)
input_thread.daemon = True
input_thread.start()

# Main thread just receives messages
while True:
    try:
        message = server.recv(2048)
        if not message:
            print("\nDisconnected from server.")
            server.close()
            sys.exit()
        else:
            print(message.decode())
    except:
        print("\nAn error occurred while receiving.")
        server.close()
        sys.exit()

