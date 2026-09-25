from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('<!DOCTYPE html>\n<html><head><title><h2>Garden Bliss</h2></title></head>\n<body>\n<h2>Garden Bliss</h2>\n<div class="price"><span class="price">$55.00</span></div>\n<button class="add-to-cart">Add to Cart</button>\n<main><p>Garden tools and plants</p></main>\n<footer class="contentinfo"><p>Seasonal tips</p></footer>\n</body></html>'.encode())
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8708), Handler)
    server.serve_forever()
