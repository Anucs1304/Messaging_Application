# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *
from threading import Lock


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
    try:
        conn.send("Welcome to this chatroom!".encode())
        print(f"[>] Sent welcome message to {addr[0]}")

    except Exception as e:
        print(f"Failed to send welcome message to {addr[0]}: {e}")
        conn.close()
        remove(conn)
        return
    while True: 
            try: 
                message = conn.recv(2048).decode()
                if message: 

                    
                    print ("<" + addr[0] + "> " + message) 

                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 

                else: 
                    remove(conn) 

            except: 
                continue

def broadcast(message, connection): 
    with client_lock:
        for clients in list_of_clients: 
            if clients!=connection: 
                try: 
                    clients.send(message.encode())
                except Exception as e:
                    print(f"Error sending to client: {e}") 
                    clients.close() 
                    remove(clients) 

def remove(connection): 
    with client_lock:
        if connection in list_of_clients: 
            list_of_clients.remove(connection) 

while True: 

    conn, addr = server.accept() 
    print(f"[+] {addr[0]} connected")

    with client_lock:
        list_of_clients.append(conn)
         
    start_new_thread(clientthread, (conn, addr))


    # prints the address of the user that just connected 
    print (addr[0] + " connected")
    print(f"[+] New connection from {addr}")

    # creates and individual thread for every user 
    # that connects 
    start_new_thread(clientthread,(conn,addr))     


    remove(conn)
    conn.close()
    break