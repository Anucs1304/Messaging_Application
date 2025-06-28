import os

BUFFER_SIZE = 4096

def send_file(sock, filepath):
    """Sends file metadata and content to the server or another client"""
    if not os.path.exists(filepath):
        print(f"[!] File not found: {filepath}")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    # Send file header
    header = f"__file__|{filename}|{filesize}"
    sock.send(header.encode())

    # Send file content
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)
    print(f"[📤] File sent: {filename}")

def receive_file(sock, header):
    """Parses header and saves incoming file"""
    try:
        _, filename, filesize = header.split("|")
        filesize = int(filesize)

        with open(f"received_{filename}", "wb") as f:
            remaining = filesize
            while remaining > 0:
                chunk = sock.recv(min(BUFFER_SIZE, remaining))
                if not chunk:
                    break
                f.write(chunk)
                remaining -= len(chunk)

        print(f"[📥] Received file: {filename} ({filesize} bytes)")

    except Exception as e:
        print(f"[!] Error receiving file: {e}")
