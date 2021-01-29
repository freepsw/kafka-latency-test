from http.server import BaseHTTPRequestHandler, HTTPServer  # python3
import time
class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("received get request")

    def do_POST(self):
        start = time.time()
        print("START: ", start)
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length)  # Get the data
        print("Size : ", len(post_data))
        print("END: ", time.time() - start)
        #post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # print("LED is {}".format(post_data))
        message = "{size: %s}" % len(post_data)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def do_PUT(self):
        self.do_POST()

host = ''
port = 8080
HTTPServer((host, port), HandleRequests).serve_forever()