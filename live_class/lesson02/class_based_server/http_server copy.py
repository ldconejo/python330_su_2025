import sys
import os
import socket
import mimetypes

class HttpServer:
    def __init__(self, port=10000):
        self.port = port

    def get_path(self, request):
        # Extract the path from the request
        try:
            first_line = request.splitlines()[0]
            path = first_line.split()[1]
            return path
        except IndexError:
            return '/'

    def get_content(self, path):
        # Serve the requested file or a default message
        if path == '/':
            return b"<html><body><h1>Simple HTTP Server</h1></body></html>", 'text/html'
        
        # Normalize the path to prevent directory traversal attacks
        safe_path = os.path.normpath(path.lstrip('/'))
        file_path = os.path.join(os.getcwd(), safe_path)


        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            content_type, _ = mimetypes.guess_type(file_path)
            return content, content_type
        else:
            return b"<html><body><h1>Error 404: Not Found</h1></body></html>", 'text/html'
    
    def make_response(self, status_code, status_message, body, mimetype):
        # Create the HTTP response
        response = f"HTTP/1.1 {status_code} {status_message}\r\n"
        response += f"Content-Type: {mimetype}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n\r\n"
        print(response)
        response = response.encode('utf-8') + body
        return response
        
    def serve(self):
        address = ('0.0.0.0', self.port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Serving HTTP on {address}:{self.port} ...")
        print(f"Visit http://localhost:{self.port} in your browser")
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
                        # Note the use of decode to convert bytes to string
                        line = client_connection.recv(1024).decode('utf-8')
                        request += line
                        if '\r\n\r\n' in request:
                            break

                    # Parse the request
                    path = self.get_path(request)
                    body, mimetype = self.get_content(path)

                    response = self.make_response("200",
                                                  "OK",
                                                  body, 
                                                  mimetype)
                    client_connection.sendall(response)
                except KeyboardInterrupt:
                    client_connection.close()
                except Exception as exception_details:
                    print(f"Error accepting connection: {exception_details}")
        except KeyboardInterrupt:
            print("Server stopped by user")
        finally:
            sock.close()
            print("Socket closed")

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Using default port 10000")
        port = 10000  # Default port
    else:
        print(f"Using port {port}")
    server = HttpServer(port)    
    server.serve()
