import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
client_socket.connect(('127.0.0.1', 50000))
client_socket.sendall(b"Hello, Server!")
client_socket.recv(4096)  # Receive up to 4096 bytes
client_socket.close()  # Remember to close the socket when done