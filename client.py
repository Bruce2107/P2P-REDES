import json
import socket
from collections import Counter
from os import environ, walk
import sys
from dotenv import load

from RepeatedTimer import RepeatedTimer

load()
folder = sys.argv[1]


def get_rarest_first(file_list):
    all_files = []
    for client in file_list:
        all_files += client[1]
    counter = Counter(all_files)
    my_files = next(walk(folder), (None, None, []))[2]
    for i in my_files:
        del counter[i]
    order = sorted(counter, key=counter.get)
    while len(order) > 0:
        rarest = order.pop(0)
        for client in file_list:
            if rarest in client[1]:
                print(client[0], rarest)
                break


def client_server_connection(**kwargs):
    c_socket = kwargs.get("socket")

    filenames = next(walk(folder), (None, None, []))[2]
    jsondump = json.dumps({"files": filenames})
    c_socket.send(jsondump.encode())
    data = c_socket.recv(1024).decode()
    clients = json.loads(data)["clients"]
    get_rarest_first(clients)


def client_program():
    host = "192.168.100.6"  # as both code is running on same pc
    port = int(environ.get("SERVER_PORT") or 4000)

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_server_connection(socket=client_socket)
    RepeatedTimer(10, client_server_connection, socket=client_socket)
    # message = input(" -> ")  # take input
    #
    # client_socket.close()  # close the connection


if __name__ == "__main__":
    client_program()
