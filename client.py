# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
#import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) == 3: 
   IP_address = "192.168.178.88"
   Port = 12345

else:
    # Fallback for testing
    IP_address = "192.168.178.88"
    Port = 12345

server.connect((IP_address, Port)) 

import threading

# Function to handle user input in a separate thread
def handle_input():
    while True:
        message = sys.stdin.readline()
        if message.strip().lower() == "/exit":
            print("Exiting chat...")
            server.close()
            sys.exit()
        server.send(message.encode())
        sys.stdout.write("<You> ")
        sys.stdout.write(message)
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


