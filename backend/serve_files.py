import http.server
import socketserver

PORT = 8000
DIRECTORY = "."

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path.endswith('.json'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open(self.path[1:], 'rb') as file:  # Remove leading '/'
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving files from {DIRECTORY} at port {PORT}")
    httpd.serve_forever()
