"""Lightweight web server to serve Mission Control UI on port 3000."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = 3000
DIRECTORY = os.path.join(os.path.dirname(__file__), "public")


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def run():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"[*] Mission Control UI server listening on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run()
