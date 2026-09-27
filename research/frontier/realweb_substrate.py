"""Real Web substrate for EXP-FRONTIER-36293269574.

Credential-free public HTTP/HTML observation substrate.
No browser, no docker, no model key, no authentication.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import tiktoken

# Frozen tokenizer from EXP-INTEL-36287179392
TOKENIZER = tiktoken.get_encoding("cl100k_base")
TARGET_TOKENS_PER_OBS = 763  # Baseline from EXP-INTEL-36287179392

# TRAIN sites (10 sites, distillation only) - frozen pre-registered
TRAIN_SITES = [
    "https://httpbin.org",
    "https://jsonplaceholder.typicode.com",
    "https://api.github.com",
    "https://developer.mozilla.org",
    "https://docs.python.org",
    "https://doc.rust-lang.org",
    "https://go.dev",
    "https://en.wikipedia.org",
    "https://example.com",
    "https://postman-echo.com",
]

# TEST sites (5 sites, execution only) - frozen pre-registered, distinct eTLD+1
# api.publicapis.org unreachable (DNS), replaced with api.ipify.org
TEST_SITES = [
    "https://api.ipify.org",
    "https://dog.ceo",
    "https://catfact.ninja",
    "https://api.chucknorris.io",
    "https://zenquotes.io",
]

ALL_SITES = TRAIN_SITES + TEST_SITES

# Task family: Read-write resource CRUD on REST-like endpoints
# Intent families matching the synthetic substrate
INTENTS = [
    "list_resources",   # GET /resources or equivalent
    "create_resource",  # POST /resources or equivalent
    "read_resource",    # GET /resources/{id}
    "update_resource",  # PATCH/PUT /resources/{id}
    "delete_resource",  # DELETE /resources/{id}
]


@dataclass
class RealHTTPResponse:
    """Raw HTTP response with metadata."""
    url: str
    method: str
    status_code: int
    headers: dict[str, str]
    body: bytes
    body_text: str
    elapsed_ms: float
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "method": self.method,
            "status_code": self.status_code,
            "headers": self.headers,
            "body_text": self.body_text[:5000],  # Truncate for storage
            "elapsed_ms": self.elapsed_ms,
            "error": self.error,
        }


@dataclass
class MinimalObservation:
    """Minimal HTTP+HTML structural representation (763 tokens baseline)."""
    url: str
    method: str
    status_code: int
    # Structural elements only
    link_relations: list[dict[str, str]]  # rel, href
    form_actions: list[dict[str, Any]]    # action, method, inputs
    input_names: list[str]
    semantic_landmarks: list[str]         # main, nav, article, section, etc.
    response_headers: dict[str, str]      # Content-Type, ETag, Cache-Control, etc.
    tokens: int
    raw_html_hash: str

    def to_tokens(self) -> int:
        """Serialize to token count using cl100k_base."""
        serializable = {
            "url": self.url,
            "method": self.method,
            "status": self.status_code,
            "links": self.link_relations,
            "forms": self.form_actions,
            "inputs": self.input_names,
            "landmarks": self.semantic_landmarks,
            "headers": self.response_headers,
        }
        text = json.dumps(serializable, sort_keys=True, separators=(",", ":"))
        return len(TOKENIZER.encode(text))

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "method": self.method,
            "status_code": self.status_code,
            "link_relations": self.link_relations,
            "form_actions": self.form_actions,
            "input_names": self.input_names,
            "semantic_landmarks": self.semantic_landmarks,
            "response_headers": self.response_headers,
            "tokens": self.tokens,
            "raw_html_hash": self.raw_html_hash,
        }


class RealWebClient:
    """HTTP client for credential-free public websites."""

    def __init__(self, timeout: int = 30, user_agent: str = "SPIDER-FRONTIER/1.0"):
        self.timeout = timeout
        self.user_agent = user_agent
        self.request_count = 0
        self.total_tokens = 0

    def request(self, method: str, url: str, body: Any = None, headers: dict[str, str] | None = None) -> RealHTTPResponse:
        """Make HTTP request and return raw response."""
        self.request_count += 1

        req_headers = {"User-Agent": self.user_agent, "Accept": "application/json, text/html, */*"}
        if headers:
            req_headers.update(headers)

        data = None
        if body is not None:
            if isinstance(body, (dict, list)):
                data = json.dumps(body).encode("utf-8")
                req_headers.setdefault("Content-Type", "application/json")
            else:
                data = str(body).encode("utf-8")

        req = Request(url, data=data, headers=req_headers, method=method.upper())

        start = time.perf_counter()
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                raw_body = resp.read()
                elapsed = (time.perf_counter() - start) * 1000
                return RealHTTPResponse(
                    url=url,
                    method=method.upper(),
                    status_code=resp.status,
                    headers=dict(resp.getheaders()),
                    body=raw_body,
                    body_text=raw_body.decode("utf-8", errors="replace"),
                    elapsed_ms=elapsed,
                    error=None,
                )
        except HTTPError as e:
            elapsed = (time.perf_counter() - start) * 1000
            raw_body = e.read()
            return RealHTTPResponse(
                url=url,
                method=method.upper(),
                status_code=e.code,
                headers=dict(e.headers) if e.headers else {},
                body=raw_body,
                body_text=raw_body.decode("utf-8", errors="replace"),
                elapsed_ms=elapsed,
                error=f"HTTP {e.code}",
            )
        except URLError as e:
            elapsed = (time.perf_counter() - start) * 1000
            return RealHTTPResponse(
                url=url,
                method=method.upper(),
                status_code=0,
                headers={},
                body=b"",
                body_text="",
                elapsed_ms=elapsed,
                error=f"URL Error: {e.reason}",
            )
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return RealHTTPResponse(
                url=url,
                method=method.upper(),
                status_code=0,
                headers={},
                body=b"",
                body_text="",
                elapsed_ms=elapsed,
                error=f"Exception: {type(e).__name__}: {e}",
            )

    def get(self, url: str) -> RealHTTPResponse:
        return self.request("GET", url)

    def post(self, url: str, body: Any = None) -> RealHTTPResponse:
        return self.request("POST", url, body)

    def put(self, url: str, body: Any = None) -> RealHTTPResponse:
        return self.request("PUT", url, body)

    def patch(self, url: str, body: Any = None) -> RealHTTPResponse:
        return self.request("PATCH", url, body)

    def delete(self, url: str) -> RealHTTPResponse:
        return self.request("DELETE", url)


def extract_minimal_observation(response: RealHTTPResponse) -> MinimalObservation:
    """Extract minimal structural observation from HTTP response (763 tokens target)."""
    html = response.body_text
    raw_hash = hashlib.sha256(response.body).hexdigest()[:16]

    # Extract link relations
    link_relations = []
    for match in re.finditer(r'<link\s+([^>]*rel=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\'][^>]*)>', html, re.IGNORECASE):
        attrs = match.group(1)
        rel = match.group(2)
        href = match.group(3)
        link_relations.append({"rel": rel, "href": href})

    # Also find <a> tags with rel
    for match in re.finditer(r'<a\s+([^>]*rel=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\'][^>]*)>', html, re.IGNORECASE):
        rel = match.group(2)
        href = match.group(3)
        link_relations.append({"rel": rel, "href": href})

    # Extract forms
    form_actions = []
    for match in re.finditer(r'<form\s+([^>]*action=["\']([^"\']*)["\'][^>]*method=["\']([^"\']*)["\'][^>]*)>', html, re.IGNORECASE):
        action = match.group(2)
        method = match.group(3).upper()
        # Extract input names from this form
        form_html = match.group(0)
        inputs = re.findall(r'<input\s+[^>]*name=["\']([^"\']+)["\']', form_html, re.IGNORECASE)
        form_actions.append({"action": action, "method": method, "inputs": inputs})

    # Extract all input names globally
    input_names = list(set(re.findall(r'<input\s+[^>]*name=["\']([^"\']+)["\']', html, re.IGNORECASE)))

    # Extract semantic landmarks
    landmarks = []
    landmark_tags = ["main", "nav", "article", "section", "aside", "header", "footer", "form", "table", "ul", "ol"]
    for tag in landmark_tags:
        if re.search(f"<{tag}\\b", html, re.IGNORECASE):
            landmarks.append(tag)

    # Key response headers
    key_headers = {}
    for h in ["content-type", "etag", "cache-control", "last-modified", "location", "set-cookie", "x-ratelimit-limit", "x-ratelimit-remaining"]:
        if h in response.headers:
            key_headers[h] = response.headers[h]

    obs = MinimalObservation(
        url=response.url,
        method=response.method,
        status_code=response.status_code,
        link_relations=link_relations,
        form_actions=form_actions,
        input_names=input_names,
        semantic_landmarks=landmarks,
        response_headers=key_headers,
        tokens=0,  # Will compute
        raw_html_hash=raw_hash,
    )
    obs.tokens = obs.to_tokens()
    return obs


# Identifier detection
IDENTIFIER_PATTERNS = {
    # Stable identifiers
    "canonical_resource_id": [
        r'"id"\s*:\s*"([^"]+)"',           # JSON "id": "value"
        r'"id"\s*:\s*(\d+)',                # JSON "id": 123
        r'/resources/([a-zA-Z0-9_-]+)',     # REST path /resources/{id}
        r'/api/[^/]+/([a-zA-Z0-9_-]+)',     # /api/resource/{id}
        r'data-id=["\']([^"\']+)["\']',     # data-id attribute
    ],
    "stable_link_relation": [
        r'rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
        r'rel=["\']self["\']\s+href=["\']([^"\']+)["\']',
    ],
    "self_describing_url": [
        r'/([a-zA-Z0-9_-]{8,})',  # Long path segments that look like IDs
    ],
    "stable_etag": [
        r'^ETag:\s*["\']?([^"\'\s]+)',  # From headers
    ],

    # Session-scoped identifiers
    "csrf_token": [
        r'name=["\']csrf_token["\']\s+value=["\']([^"\']+)["\']',
        r'name=["\']_token["\']\s+value=["\']([^"\']+)["\']',
        r'csrf[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        r'X-CSRF-Token:\s*([^\s\r\n]+)',
    ],
    "rotating_handle": [
        r'capability[_-]?handle["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        r'access[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    ],
    "session_nonce": [
        r'name=["\']nonce["\']\s+value=["\']([^"\']+)["\']',
        r'nonce["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    ],
}


def detect_identifiers(response: RealHTTPResponse, obs: MinimalObservation) -> list[dict[str, Any]]:
    """Detect and classify identifiers in response."""
    identifiers = []
    text = response.body_text
    headers_text = "\n".join(f"{k}: {v}" for k, v in response.headers.items())

    # Check stable identifiers
    for pattern in IDENTIFIER_PATTERNS["canonical_resource_id"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            val = match.group(1) if match.lastindex else match.group(0)
            identifiers.append({
                "type": "STABLE",
                "subtype": "canonical_resource_id",
                "value": val,
                "source": "body",
            })

    for pattern in IDENTIFIER_PATTERNS["stable_link_relation"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            val = match.group(1)
            identifiers.append({
                "type": "STABLE",
                "subtype": "stable_link_relation",
                "value": val,
                "source": "body",
            })

    for pattern in IDENTIFIER_PATTERNS["self_describing_url"]:
        for match in re.finditer(pattern, response.url):
            val = match.group(1)
            if len(val) >= 8:  # Filter out short segments
                identifiers.append({
                    "type": "STABLE",
                    "subtype": "self_describing_url",
                    "value": val,
                    "source": "url",
                })

    # ETag from headers
    if "etag" in response.headers:
        identifiers.append({
            "type": "STABLE",
            "subtype": "stable_etag",
            "value": response.headers["etag"],
            "source": "header",
        })

    # Check session-scoped identifiers
    for pattern in IDENTIFIER_PATTERNS["csrf_token"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            val = match.group(1) if match.lastindex else match.group(0)
            identifiers.append({
                "type": "SESSION_SCOPED",
                "subtype": "csrf_token",
                "value": val,
                "source": "body",
            })
    for pattern in IDENTIFIER_PATTERNS["csrf_token"]:
        for match in re.finditer(pattern, headers_text, re.IGNORECASE):
            val = match.group(1) if match.lastindex else match.group(0)
            identifiers.append({
                "type": "SESSION_SCOPED",
                "subtype": "csrf_token",
                "value": val,
                "source": "header",
            })

    for pattern in IDENTIFIER_PATTERNS["rotating_handle"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            val = match.group(1) if match.lastindex else match.group(0)
            identifiers.append({
                "type": "SESSION_SCOPED",
                "subtype": "rotating_handle",
                "value": val,
                "source": "body",
            })

    for pattern in IDENTIFIER_PATTERNS["session_nonce"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            val = match.group(1) if match.lastindex else match.group(0)
            identifiers.append({
                "type": "SESSION_SCOPED",
                "subtype": "session_nonce",
                "value": val,
                "source": "body",
            })

    return identifiers


def classify_identifier_stability(identifier_values: list[str], episodes: int) -> str:
    """Classify if identifier is stable across episodes."""
    if len(set(identifier_values)) == 1 and len(identifier_values) == episodes:
        return "STABLE"
    elif len(set(identifier_values)) > 1:
        return "SESSION_SCOPED"
    return "ABSENT"


@dataclass
class EpisodeResult:
    """Result of a single episode."""
    site: str
    episode: int
    arm: str
    spans: list[dict[str, Any]]
    total_tokens: int
    total_requests: int
    total_verification: int
    total_repair: int
    correct_spans: int
    total_spans: int
    abstentions: int
    false_replays: int


def check_site_reachable(client: RealWebClient, site: str) -> tuple[bool, str]:
    """Pre-flight check for site reachability."""
    try:
        resp = client.get(site)
        if resp.status_code == 200:
            return True, "OK"
        return False, f"HTTP {resp.status_code}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


if __name__ == "__main__":
    # Quick test
    client = RealWebClient()
    for site in TEST_SITES[:2]:
        reachable, msg = check_site_reachable(client, site)
        print(f"{site}: {reachable} - {msg}")
        if reachable:
            resp = client.get(site)
            obs = extract_minimal_observation(resp)
            ids = detect_identifiers(resp, obs)
            print(f"  Tokens: {obs.tokens}, Identifiers: {len(ids)}")
            for id_info in ids[:3]:
                print(f"    {id_info['type']} {id_info['subtype']}: {id_info['value'][:50]}")