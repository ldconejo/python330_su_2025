import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server_socket.bind(('127.0.0.1', 50000))  # Bind to localhost on port 50000
server_socket.listen(1)  # Listen for incoming connections
connection, client_address = server_socket.accept()  # Accept a connection
connection.recv(4096)  # Receive up to 4096 bytes
connection.sendall(b"Hello, Client!")  # Send a response to the client
connection.close()  # Close the connection
server_socket.close()  # Close the server socket when done