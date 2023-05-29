import json
import socket
import threading
import os
from dotenv import load
from ClientType import Client

load()

CLIENTS = []


def handle_client(conn, address):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        files = json.loads(data)['files']
        if not files:
            break
        CLIENTS.append((address, files))
        filtered = list(filter(lambda client: client[0] != address, CLIENTS))
        clients = json.dumps({"clients": filtered})
        conn.send(clients.encode())


def server_program():
    host = socket.gethostname()
    port = int(os.environ.get('SERVER_PORT') or 4000)

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()


if __name__ == '__main__':
    server_program()
