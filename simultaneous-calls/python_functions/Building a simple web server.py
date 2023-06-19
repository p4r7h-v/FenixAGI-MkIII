import http.server
import socketserver

def start_simple_web_server(port=8080, directory="."):
    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = directory

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_simple_web_server(port=8080, directory=".")