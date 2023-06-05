import json
import socket
from collections import Counter
from os import environ, walk
import sys
from dotenv import load
from typing import List, Type

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from RepeatedTimer import RepeatedTimer

load()
folder = sys.argv[1]
user = sys.argv[2]

pnconfig = PNConfiguration()
userId = user
pnconfig.publish_key = 'demo'
pnconfig.subscribe_key = 'demo'
pnconfig.user_id = userId
pnconfig.ssl = True
pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
    if not status.is_error():
        pass


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        pass

    def message(self, pubnub, message):
        if message.publisher == userId:
            return
        print("from device " + message.publisher + ": " + message.message)


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
                pubnub.publish().channel(name).message('oi').pn_async(my_publish_callback)
                break


def client_server_connection(**kwargs):
    c_socket = kwargs.get("socket")

    filenames = get_client_files_name()
    jsondump = json.dumps({"files": filenames, "name": user})
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
    RepeatedTimer(
        10, client_server_connection, socket=client_socket
    )


if __name__ == "__main__":
    client_program()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(user).execute()
