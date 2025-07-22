import socket
import sys

try:
    port = int(sys.argv[1])
except IndexError:
    print("Please include a port number, eg: python serve.py 50000")
    exit(-1)

try:
    host = sys.argv[2]
except IndexError:
    host = "127.0.0.1"

client_socket = socket.socket()
client_socket.connect((host, port))

while True:
    try:
        response = client_socket.recv(4096).decode()
    except ConnectionAbortedError:
        print("Connection closed by host.")
        break

    print(response)

    my_message = input("> ").encode('utf-8') + b'\n'
    client_socket.sendall(my_message)
