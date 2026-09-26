#!/usr/bin/env python3
"""
HTTP Application for EXP-GRAPH-36272373909
stdlib-only http.server with 5 resource types × 4 CRUD operations
"""

import json
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs


# In-memory state for each resource type
STATE: Dict[str, Dict[str, Dict[str, Any]]] = {
    "users": {},
    "posts": {},
    "comments": {},
    "albums": {},
    "photos": {},
}

# Valid auth token
VALID_TOKEN = "spider-exp-token-36272373909"

# Resource schemas
SCHEMAS = {
    "users": {"id": str, "name": str, "email": str, "created_at": str},
    "posts": {"id": str, "title": str, "body": str, "user_id": str, "created_at": str},
    "comments": {"id": str, "body": str, "post_id": str, "user_id": str, "created_at": str},
    "albums": {"id": str, "title": str, "user_id": str, "created_at": str},
    "photos": {"id": str, "title": str, "url": str, "album_id": str, "created_at": str},
}

RESOURCE_FIELDS = {
    "users": ["name", "email"],
    "posts": ["title", "body", "user_id"],
    "comments": ["body", "post_id", "user_id"],
    "albums": ["title", "user_id"],
    "photos": ["title", "url", "album_id"],
}


def validate_token(auth_header: Optional[str]) -> bool:
    if not auth_header:
        return False
    return auth_header == f"Bearer {VALID_TOKEN}"


def make_response(handler: BaseHTTPRequestHandler, status: int, data: Any = None):
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    if data is not None:
        handler.wfile.write(json.dumps(data).encode())


def parse_path(path: str) -> tuple[str, Optional[str], str]:
    """Parse /resource/id?query -> (resource, id, action)"""
    parsed = urlparse(path)
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        return "", None, ""
    resource = parts[0]
    resource_id = parts[1] if len(parts) > 1 else None
    return resource, resource_id, parsed.path


class SpiderHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        resource, resource_id, _ = parse_path(self.path)
        
        if not validate_token(self.headers.get("Authorization")):
            return make_response(self, 401, {"error": "Unauthorized"})
        
        if resource not in STATE:
            return make_response(self, 404, {"error": "Not found"})
        
        if resource_id is None:
            # List all
            return make_response(self, 200, list(STATE[resource].values()))
        
        if resource_id not in STATE[resource]:
            return make_response(self, 404, {"error": "Not found"})
        
        return make_response(self, 200, STATE[resource][resource_id])

    def do_POST(self):
        resource, _, _ = parse_path(self.path)
        
        if not validate_token(self.headers.get("Authorization")):
            return make_response(self, 401, {"error": "Unauthorized"})
        
        if resource not in STATE:
            return make_response(self, 404, {"error": "Not found"})
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length).decode()) if content_length else {}
        
        # Validate required fields
        required = RESOURCE_FIELDS.get(resource, [])
        for field in required:
            if field not in body:
                return make_response(self, 400, {"error": f"Missing required field: {field}"})
        
        # Create new resource
        new_id = str(uuid.uuid4())[:8]
        now = time.time()
        new_item = {"id": new_id, **body, "created_at": str(now)}
        STATE[resource][new_id] = new_item
        
        return make_response(self, 201, new_item)

    def do_PUT(self):
        resource, resource_id, _ = parse_path(self.path)
        
        if not validate_token(self.headers.get("Authorization")):
            return make_response(self, 401, {"error": "Unauthorized"})
        
        if resource not in STATE or resource_id not in STATE[resource]:
            return make_response(self, 404, {"error": "Not found"})
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length).decode()) if content_length else {}
        
        # Update existing resource
        STATE[resource][resource_id].update(body)
        STATE[resource][resource_id]["updated_at"] = str(time.time())
        
        return make_response(self, 200, STATE[resource][resource_id])

    def do_DELETE(self):
        resource, resource_id, _ = parse_path(self.path)
        
        if not validate_token(self.headers.get("Authorization")):
            return make_response(self, 401, {"error": "Unauthorized"})
        
        if resource not in STATE or resource_id not in STATE[resource]:
            return make_response(self, 404, {"error": "Not found"})
        
        del STATE[resource][resource_id]
        return make_response(self, 204, None)

    def log_message(self, format, *args):
        # Suppress default logging
        pass


def run_server(port: int = 8765, ready_event: threading.Event = None):
    server = HTTPServer(("localhost", port), SpiderHTTPHandler)
    if ready_event:
        ready_event.set()
    server.serve_forever()


def reset_state():
    """Reset all state to empty"""
    global STATE
    for resource in STATE:
        STATE[resource].clear()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    run_server(port)