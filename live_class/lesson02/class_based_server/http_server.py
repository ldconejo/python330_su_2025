import sys
import os
import socket
import mimetypes

class HttpServer:
    def __init__(self, port=10000):
        self.port = port

    def get_path(self, request):
        try:
            first_line = request.splitlines()[0]
            path = first_line.split()[1] # [GET, /cat.jpeg, HTTP/1.1], path="/cat.jpeg"
            return path
        except IndexError:
            return '/'
        
    def get_content(self, path):
        if path == '/':
            return b"<html><body><h1>Welcome to the HTTP Server!</h1></body></html>", 'text/html'
        
        safe_path = os.path.normpath(path.lstrip('/')) # /cat.jpeg -> cat.jpeg
        file_path = os.path.join(os.getcwd(), safe_path)

        if os.path.isfile(file_path):
            with open (file_path, 'rb') as file:
                content = file.read()
            content_type, _ = mimetypes.guess_type(file_path)
            return content, content_type
        else:
            return b"<html><body><h1>404 Not Found</h1></body></html>", 'text/html'

    def make_response(self, status_code, status_message, body, mymetype):
        response = f"HTTP/1.1 {status_code} {status_message}\r\n"
        response += f"Content-Type: {mymetype}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n\r\n"
        binary_response = response.encode('utf-8') + body
        return binary_response
   
    def serve(self):
        address = ('0.0.0.0', self.port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)
        sock.listen(10)

        try:
            while True:
                print("Waiting for a connection...")
                client_connection, client_address = sock.accept()
                try:
                    print(f"Connection from {client_address}")
                    request = ''
                    while True:
                        line = client_connection.recv(1024).decode('utf-8')
                        request += line
                        if '\r\n\r\n' in request:
                            break
                        print(f"Received data: {line.strip()}")
                        path = self.get_path(request)
                        body, mimetype = self.get_content(path)
                        response = self.make_response(200, "OK", body, mimetype)
                        client_connection.sendall(response)
                except KeyboardInterrupt:
                    client_connection.close()
                except Exception as exception_details:
                    print(f"Error receiving request: {exception_details}")
                    client_connection.close()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            sock.close()
            print("Socket closed.")

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 10000
        print(f"Using default port: {port}")
    else:
        print(f"Using specified port: {port}")
    server = HttpServer(port)
    server.serve()
    print("Server has stopped.")
    sys.exit(0)