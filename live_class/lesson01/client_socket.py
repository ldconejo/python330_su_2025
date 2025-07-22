import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
client_socket.connect(('127.0.0.1', 50000))
data = client_socket.recv(1024)
print('Received from server:', data.decode())
client_socket.sendall(b'Hello, server!')
client_socket.close()