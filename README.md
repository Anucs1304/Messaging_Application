# 💬 Real-Time Python Messaging App

A TCP-based multi-client chatroom with real-time messaging, file sharing, user authentication, and contact management — built from scratch in Python using sockets and threading.

---

## Features

- **Authentication**  
  Users can securely register and log in using username/password (hashed using SHA-256)

-  **Real-Time Messaging**  
  Multiple clients can join and chat simultaneously via a threaded server

- **File Transfer**  
  Seamlessly send any file via `/file <filepath>` command

- **Contact Management**  
  Add, view, and remove contacts with simple commands

- **Modular Structure**  
  Code organized into separate files for auth, file handling, and contacts

---

## Setup Instruction

- python server.py  - Start the server
- python client.py  - Login or register to join the chatroom

## File Structure

```bash
├── server.py               # Multithreaded server
├── client.py               # Client application
├── authentication.py       # User login/registration (with password hashing)
├── fileTransfer.py        # Send/receive file utility
├── contact_manager.py      # Contact book for each user
├── users.json              # Stores credentials securely (hashed)
├── received_<filename>     # Received files saved by server



