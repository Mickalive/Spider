"""
HTTP Server for EXP-GRAPH-36287167610
stdlib-only multi-endpoint multi-verb HTTP application
"""
import json
import hashlib
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List, Optional, Tuple
import random


class SpiderHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, server_state: Dict[str, Any], **kwargs):
        self.server_state = server_state
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self._handle_request("GET")

    def do_POST(self):
        self._handle_request("POST")

    def do_PUT(self):
        self._handle_request("PUT")

    def do_DELETE(self):
        self._handle_request("DELETE")

    def _handle_request(self, method: str):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Parse path: /{resource}/{id} or /{resource}
        parts = [p for p in path.split("/") if p]
        if not parts:
            self._send(404, {"error": "Not found"})
            return

        resource = parts[0]
        resource_id = parts[1] if len(parts) > 1 else None

        valid_resources = ["users", "posts", "comments", "albums", "photos"]
        if resource not in valid_resources:
            self._send(404, {"error": "Unknown resource"})
            return

        store = self.server_state[resource]

        try:
            if method == "GET":
                if resource_id is None:
                    # List all
                    self._send(200, list(store.values()))
                else:
                    if resource_id in store:
                        self._send(200, store[resource_id])
                    else:
                        self._send(404, {"error": "Not found"})

            elif method == "POST":
                content_length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(content_length).decode()) if content_length > 0 else {}
                # Generate ID if not provided
                new_id = body.get("id", str(len(store) + 1))
                body["id"] = new_id
                store[new_id] = body
                self._send(201, body)

            elif method == "PUT":
                if resource_id is None:
                    self._send(400, {"error": "ID required for update"})
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(content_length).decode()) if content_length > 0 else {}
                if resource_id in store:
                    body["id"] = resource_id
                    store[resource_id] = body
                    self._send(200, body)
                else:
                    self._send(404, {"error": "Not found"})

            elif method == "DELETE":
                if resource_id is None:
                    self._send(400, {"error": "ID required for delete"})
                    return
                if resource_id in store:
                    del store[resource_id]
                    self._send(204, {})
                else:
                    self._send(404, {"error": "Not found"})

        except json.JSONDecodeError:
            self._send(400, {"error": "Invalid JSON"})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def _send(self, status: int, data: Any):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # Suppress default logging


class SpiderHTTPServer:
    def __init__(self, port: int = 0):
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.state = self._initial_state()
        self._state_hash: Optional[str] = None

    def _initial_state(self) -> Dict[str, Dict[str, Any]]:
        return {
            "users": {},
            "posts": {},
            "comments": {},
            "albums": {},
            "photos": {}
        }

    def reset(self):
        """Reset server state to initial empty state"""
        self.state = self._initial_state()
        self._state_hash = None

    def get_state_hash(self) -> str:
        """Get SHA256 hash of current server state"""
        if self._state_hash is None:
            serialized = json.dumps(self.state, sort_keys=True)
            self._state_hash = hashlib.sha256(serialized.encode()).hexdigest()
        return self._state_hash

    def start(self):
        def handler(*args, **kwargs):
            SpiderHTTPHandler(*args, server_state=self.state, **kwargs)

        self.server = HTTPServer(("localhost", self.port), handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=2)

    def get_url(self) -> str:
        return f"http://localhost:{self.port}"


def make_handler(server_state):
    def handler(*args, **kwargs):
        return SpiderHTTPHandler(*args, server_state=server_state, **kwargs)
    return handler


if __name__ == "__main__":
    # Test server
    server = SpiderHTTPServer(8765)
    server.start()
    print(f"Server started on {server.get_url()}")
    import time
    time.sleep(10)
    server.stop()