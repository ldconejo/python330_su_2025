'''
Prework:

- Get information about the remote host (do this in the Python CLI)

>>> import socket
>>> socket.getaddrinfo("info.cern.ch", 'http')
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('188.184.67.127', 80)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('188.184.67.127', 80))]

We asked for information about the CERN web server.
AF_INET means we are using IPv4.
SOCK_STREAM means we are using TCP.
SOCK_DGRAM means we are using UDP.
The last tuple contains the IP address and port number of the server.
'''

import socket

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

client_socket.connect(('188.184.67.127', 80))

message = "GET / HTTP/1.1\r\n"
message += "Host: info.cern.ch\r\n\r\n"
message = message.encode('utf-8')
message
client_socket.sendall(message)
response = client_socket.recv(4096) # Receive up to 4096 bytes
print(response.decode('utf-8'))
client_socket.close() # Remember to close the socket when done