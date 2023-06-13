import json
import socket
import threading
import os
from dotenv import load

load()

CLIENTS = []


def check_client_list(address, name):
    return list(
        filter(lambda client: client[0] == address or client[2] == name, CLIENTS)
    )


def disconnect_client(address):
    for i, (ip, _, _) in enumerate(CLIENTS):
        if address == ip:
            del CLIENTS[i]
            break


def handle_client(conn, address):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                disconnect_client(address)
                break
            jdata = json.loads(data)
            files = jdata["files"]
            name = jdata["name"]

            if len(check_client_list(address, name)) == 0:
                CLIENTS.append((address, files, name))
            else:
                for i, (client, _, cname) in enumerate(CLIENTS):
                    if address == client or name == cname:
                        CLIENTS[i] = (address, files, name)
                        break
            filtered = list(
                filter(
                    lambda clientF: clientF[0] != address and clientF[2] != name,
                    CLIENTS,
                )
            )
            clients = json.dumps({"clients": filtered})
            conn.send(clients.encode())
        except ConnectionResetError as e:
            disconnect_client(address)
            break


def server_program():
    host = "192.168.100.4"
    port = int(os.environ.get("SERVER_PORT") or 4000)

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()


if __name__ == "__main__":
    server_program()
