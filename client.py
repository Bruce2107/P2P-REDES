import json
import socket
from os import environ, walk
import sys
from dotenv import load
from ClientType import Client

load()


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = int(environ.get('SERVER_PORT') or 4000)
    folder = sys.argv[1]

    filenames = (next(walk(folder), (None, None, []))[2])
    jsondump = json.dumps({"files": filenames})

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_socket.send(jsondump.encode())
    data = client_socket.recv(1024).decode()
    clients = json.loads(data)['clients']
    for i in clients:
        ip, files = i
        print(ip)
    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        c = Client(data[0], data[1])
        print(c)
        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
