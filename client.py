import json
import socket
from collections import Counter
from os import environ, walk
import sys
from dotenv import load
from typing import List, Type
from enum import Enum

from RepeatedTimer import RepeatedTimer


class SocketType(Enum):
    CLIENT, SERVER = range(1, 3)


load()
folder = sys.argv[1]
user = sys.argv[2]
client_ip = socket.gethostbyname(socket.gethostname())
client_port = 9999
server_ip = "192.168.100.4"
server_port = int(environ.get("SERVER_PORT") or 4000)


def get_client_files_name() -> Type[List[str]]:
    return next(walk(folder), (List[str], None, []))[2]


def get_rarest_first(peers):
    all_files = []
    for _, files, _ in peers:
        all_files += files
    counter = Counter(all_files)
    my_files = get_client_files_name()
    for i in my_files:
        del counter[i]
    order = sorted(counter, key=counter.get)
    while len(order) > 0:
        rarest = order.pop(0)
        for peer, files, name in peers:
            if rarest in files:
                print(peer, name)
                break


def client_server_connection(**kwargs):
    c_socket = kwargs.get("socket")

    filenames = get_client_files_name()
    jsondump = json.dumps({"files": filenames, "name": user})
    c_socket.send(jsondump.encode())
    data = c_socket.recv(1024).decode()
    clients = json.loads(data)["clients"]
    get_rarest_first(clients)


def create_socket(address: tuple, socket_type: SocketType) -> socket:
    new_socket = socket.socket()
    new_socket.connect(address) if socket_type == SocketType.CLIENT else new_socket.bind(address)
    return new_socket


def client_program():
    client_socket = create_socket((server_ip, server_port), SocketType.CLIENT)
    client_server_connection(socket=client_socket)
    RepeatedTimer(
        10, client_server_connection, socket=client_socket
    )


def client_as_server():
    server_socket = create_socket((client_ip, client_port), SocketType.SERVER)
    server_socket.listen(5)


if __name__ == "__main__":
    client_program()
