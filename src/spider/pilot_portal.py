"""Local HTTP/HTML task bank for a real Chromium + LLM-agent pilot.

Two task families and unseen identifiers. Serves exclusively on loopback.
Intentionally toy-sized: never claim it represents arbitrary websites.
"""
from __future__ import annotations

import json
import threading
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlsplit

DATA = {
    "invoices": {"A-101": "CHF 138.45", "A-202": "CHF 251.30"},
    "shipments": {"S-501": "Delivered", "S-902": "In transit"},
}


def truth(family: str, identifier: str) -> str | None:
    return DATA.get(family, {}).get(identifier)


class PortalHandler(BaseHTTPRequestHandler):
    def respond(self, status: int, content: str | bytes, content_type: str = "text/html; charset=utf-8"):
        payload = content.encode("utf-8") if isinstance(content, str) else content
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urlsplit(self.path)
        parts = parsed.path.strip("/").split("/")
        if parsed.path == "/":
            return self.respond(200, '<h1>Operations portal</h1><a href="/portal/invoices">Invoices</a> <a href="/portal/shipments">Shipments</a>')
        if len(parts) == 2 and parts[0] == "portal" and parts[1] in DATA:
            family = parts[1]
            return self.respond(200,
                f'<h1>{escape(family.title())}</h1><form method="GET" action="/portal/{family}/search">'
                '<label>Reference ID <input aria-label="Reference ID" name="id"></label>'
                '<button type="submit">Find record</button></form>')
        if len(parts) == 3 and parts[0] == "portal" and parts[1] in DATA and parts[2] == "search":
            family = parts[1]
            identifier = parse_qs(parsed.query).get("id", [""])[0]
            if truth(family, identifier) is None:
                return self.respond(404, "<h1>Record not found</h1>")
            return self.respond(200, '<h1>Search result</h1><a href="/portal/'
                +family+'/view?id='+quote(identifier)+'">Open matching record</a>')
        if len(parts) == 3 and parts[0] == "portal" and parts[1] in DATA and parts[2] == "view":
            family, identifier = parts[1], parse_qs(parsed.query).get("id", [""])[0]
            value = truth(family, identifier)
            if value is None:
                return self.respond(404, "<h1>Not found</h1>")
            return self.respond(200, '<h1>Record details</h1><p>Reference: '+escape(identifier)
                +'</p><p>Answer: <strong id="answer">'+escape(value)+'</strong></p>')
        if len(parts) == 3 and parts[0] == "api" and parts[1] in DATA:
            family, identifier = parts[1], parts[2]
            value = truth(family, identifier)
            if value is None:
                return self.respond(404, json.dumps({"ok": False}), "application/json")
            return self.respond(200,
                json.dumps({"ok": True, "family": family, "id": identifier, "answer": value}),
                "application/json")
        return self.respond(404, "<h1>Not found</h1>")

    def log_message(self, *_args):
        pass


def start_portal() -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), PortalHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, thread, f"http://{host}:{port}"
