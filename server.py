import json
import socket
import threading
import os
from dotenv import load

load()

CLIENTS = []


def check_client_list(address):
    return list(filter(lambda client: client[0] == address, CLIENTS))


def handle_client(conn, address):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        files = json.loads(data)['files']
        if not files:
            break
        if len(check_client_list(address)) == 0:
            CLIENTS.append((address, files))
        else:
            for i, (client, _) in enumerate(CLIENTS):
                if address == client:
                    CLIENTS[i] = (address, files)
                    break
        filtered = list(filter(lambda clientF: clientF[0] != address, CLIENTS))
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
