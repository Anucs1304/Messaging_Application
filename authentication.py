import hashlib
import json
import os

USERS_DB = "users.json"

def load_users():
    if not os.path.exists(USERS_DB):
        return {}
    with open(USERS_DB, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_DB, "w") as file:
        json.dump(users, file)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return True, "Registered successfully."

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found."
    if users[username] != hash_password(password):
        return False, "Incorrect password."
    return True, "Login successful."
