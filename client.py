import json
import socket
from socket import SocketType as ST
import threading
from collections import Counter
from os import environ, walk
import os
import sys
from dotenv import load
from typing import List, Type
from enum import Enum
import keyboard

from RepeatedTimer import RepeatedTimer


class SocketType(Enum):
    CLIENT, SERVER = range(1, 3)


load()
folder = sys.argv[1]
user = sys.argv[2]
client_ip = socket.gethostbyname(socket.gethostname())
client_port = 9999
tracker_ip = "192.168.100.4"
tracker_port = int(environ.get("SERVER_PORT") or 4000)
MIN_PEER_REQUIRED = 1


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
                peer_socket = create_socket((peer[0], client_port), SocketType.CLIENT)
                peer_socket.send(rarest.encode())
                print(f"Requesting {rarest} from {name}")
                with open(f"{folder}/{rarest}", "wb") as f:
                    while True:
                        bytes_read = peer_socket.recv(1024)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                        peer_socket.close()
                        f.close()
                        break


def connect_to_tracker(**kwargs):
    tracker = kwargs.get("tracker")

    filenames = get_client_files_name()
    jsondump = json.dumps({"files": filenames, "name": user})
    tracker.send(jsondump.encode())
    data = tracker.recv(1024).decode()
    clients = json.loads(data)["clients"]
    if len(clients) >= MIN_PEER_REQUIRED:
        get_rarest_first(clients)
    else:
        print(f"Aguardando {MIN_PEER_REQUIRED - len(clients)} peers entrarem")


def create_socket(address: tuple, socket_type: SocketType) -> ST:
    new_socket = socket.socket()
    if socket_type == SocketType.CLIENT:
        new_socket.connect(address)
    else:
        new_socket.bind(address)
    return new_socket


def tracker_program():
    print('Tracker rodando')
    tracker = create_socket((tracker_ip, tracker_port), SocketType.CLIENT)
    connect_to_tracker(tracker=tracker)
    timer = RepeatedTimer(10, connect_to_tracker, tracker=tracker)
    keyboard.add_hotkey("esc", exit_tracker, args=[timer])


def exit_tracker(*args):
    timer = args[0]
    timer.stop()
    keyboard.remove_hotkey("esc")
    # raise SystemExit(1)
    os._exit(0)


def handle_request(conn, address):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        with open(f"{folder}/{data}", "rb") as f:
            print(f"Sending {data}")
            conn.sendfile(f)
            f.close()


def server_program():
    print('Server rodando')
    server_socket = create_socket((client_ip, client_port), SocketType.SERVER)
    server_socket.listen(5)
    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_request, args=(conn, address))
        client_thread.start()


if __name__ == "__main__":
    tracker = threading.Thread(target=tracker_program)
    server = threading.Thread(target=server_program)
    tracker.start()
    server.start()
