from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from urllib.parse import urlparse, parse_qs
from websocket import create_connection

class WebSocketHandler:
    def __init__(self, ws_url, payload_template):
        self.ws_url = ws_url
        self.payload_template = payload_template

    def run_sqlmap_middleware(self):
        class MiddlewareHTTPHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_path = urlparse(self.path)
                query = parse_qs(parsed_path.query)
                # Assuming the injection point key is known and consistent, e.g., 'id'
                injection_point = query.get('id', [''])[0]

                formatted_payload = self.server.payload_template.replace('%s', injection_point)
                response = self.forward_payload_to_ws(formatted_payload)
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(response.encode())

            def forward_payload_to_ws(self, payload):
                ws = create_connection(self.server.ws_url)
                ws.send(payload)
                received = ws.recv()
                ws.close()
                return received

        server = HTTPServer(('localhost', 8081), MiddlewareHTTPHandler)
        server.payload_template = self.payload_template
        server.ws_url = self.ws_url
        print("Middleware server running on http://localhost:8081/")
        server.serve_forever()
