import socket
import threading

CLIENTS = []

def handle_client(conn, address):
    print(f"Connection from: {address}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"From connected user {address}: {data}")
        conn.send(str(CLIENTS).encode())

def server_program():
    host = socket.gethostname()
    port = 4000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, address = server_socket.accept()
        CLIENTS.append(address)
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()

if __name__ == '__main__':
    server_program()