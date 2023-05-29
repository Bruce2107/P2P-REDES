import json
import socket
from os import environ, walk
import sys
from dotenv import load

from RepeatedTimer import RepeatedTimer

load()


def client_server_connection(**kwargs):
    c_socket = kwargs.get('socket')
    folder = sys.argv[1]

    filenames = (next(walk(folder), (None, None, []))[2])
    jsondump = json.dumps({"files": filenames})
    c_socket.send(jsondump.encode())
    data = c_socket.recv(1024).decode()
    clients = json.loads(data)['clients']
    for i in clients:
        ip, files = i
        print(ip)


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = int(environ.get('SERVER_PORT') or 4000)

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_server_connection(socket=client_socket)
    RepeatedTimer(10, client_server_connection, socket=client_socket)
    # message = input(" -> ")  # take input
    #
    # client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
