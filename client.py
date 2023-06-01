import json
import socket
from collections import Counter
from os import environ, walk
import sys
from dotenv import load
from typing import List, Type

from RepeatedTimer import RepeatedTimer

load()
folder = sys.argv[1]


def get_client_files_name() -> Type[List[str]]:
    return next(walk(folder), (List[str], None, []))[2]


def get_rarest_first(peers):
    all_files = []
    for _, files in peers:
        all_files += files
    counter = Counter(all_files)
    my_files = get_client_files_name()
    for i in my_files:
        del counter[i]
    order = sorted(counter, key=counter.get)
    while len(order) > 0:
        rarest = order.pop(0)
        for peer, files in peers:
            if rarest in files:
                print(peer, rarest)
                break


def client_server_connection(**kwargs):
    c_socket = kwargs.get("socket")

    filenames = get_client_files_name()
    jsondump = json.dumps({"files": filenames})
    c_socket.send(jsondump.encode())
    data = c_socket.recv(1024).decode()
    clients = json.loads(data)["clients"]
    get_rarest_first(clients)


def client_program():
    host = "192.168.100.6"
    port = int(environ.get("SERVER_PORT") or 4000)

    client_socket = socket.socket()
    client_socket.connect((host, port))
    client_server_connection(socket=client_socket)
    RepeatedTimer(10, client_server_connection, socket=client_socket)  # connection server
    # message = input(" -> ")  # take input
    #
    # client_socket.close()  # close the connection


if __name__ == "__main__":
    client_program()
