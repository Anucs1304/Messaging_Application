# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *
from threading import Lock
import signal
from fileTransfer import receive_file
from authentication import login, register


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) == 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 

IP_address = "192.168.178.88"

Port = 12345

server.bind((IP_address, Port)) 

server.listen(100) 

list_of_clients = [] 
client_lock = Lock()

def clientthread(conn, addr):  
    conn.send("Enter 'login' or 'register': ".encode())
    mode = conn.recv(1024).decode().strip().lower()

    conn.send("Username: ".encode())
    username = conn.recv(1024).decode().strip()

    conn.send("Password: ".encode())
    password = conn.recv(1024).decode().strip()

    if mode == "register":
        success, msg = register(username, password)
    else:
        success, msg = login(username, password)

    conn.send((msg + "\n").encode())

    if not success:
        conn.close()
        return

    welcome_msg = f"Welcome {username}! You are now in the chatroom.\n"
    try:
        conn.send(welcome_msg.encode())
    except ConnectionAbortedError:
        print(f"[!] Client at {addr} disconnected before welcome message.")
        remove(conn)
        return
    broadcast(f"[+] {username} has joined the chat.", conn)
    while True: 
            try: 
                message = conn.recv(2048).decode()
                if message.startswith("__file__|"):
                    from fileTransfer import receive_file
                    receive_file(conn, message)
                    broadcast(f"{addr[0]} shared a file.", conn)
                else:
                    print(f"<{addr[0]}> {message}")
                    message_to_send = f"<{addr[0]}> {message}"
                    broadcast(message_to_send, conn)

            except Exception as e:
                print(f"Error with client {addr[0]}: {e}")
                remove(conn)
                break


def broadcast(message, connection, system=False):
    prefix = "[SYSTEM]" if system else"" 
    with client_lock:
        for clients in list_of_clients: 
            if clients!=connection: 
                try: 
                    clients.send((prefix + message).encode())
                except Exception as e:
                    print(f"Error sending to client: {e}") 
                    clients.close() 
                    remove(clients) 

def remove(connection): 
    with client_lock:
        if connection in list_of_clients: 
            list_of_clients.remove(connection) 

def signal_handler(sig, frame):
    print("Shutting down server...")
    with client_lock:
        for client in list_of_clients:
            client.close()
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True: 

    conn, addr = server.accept() 
    print(f"[+] {addr[0]} connected")

    with client_lock:
        list_of_clients.append(conn)
         
    start_new_thread(clientthread, (conn, addr))


    # prints the address of the user that just connected 
    print (addr[0] + " connected")
    print(f"[+] New connection from {addr}")
