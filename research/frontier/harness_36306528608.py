"""Frozen instrument substrate for EXP-FRONTIER-36306528608 (lane=frontier, EXECUTE).

Implements exactly the observation representation and HTTP substrate declared in the
frozen `prereg.md` section 8 and `spec.json.measurement_validity.cost_basis`:

  * stdlib HTTP only (urllib), no browser, no docker, no model key, no network beyond
    the selected sites themselves.
  * BODY-SENSITIVE observation: url, method, status_code, link relations, form actions,
    input names, semantic landmarks, response headers, SHA256 of the response body and
    key body-derived content fields -- tokenised with cl100k_base over the FULL
    serializable structure.
  * Token-to-latency / token-to-dollar mapping is explicitly UNKNOWN (prereg section 8).

Raw evidence is appended to JSONL files with non-self-referential SHA256 hashes: each
record's hash is computed over the record payload only, never over the file that
contains it.

This module contains no arm logic and no outcome measurement. It is the substrate
shared by the screen and the arm runner.
"""

from __future__ import annotations

import hashlib
import http.cookiejar
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any

import tiktoken

EXPERIMENT_ID = "EXP-FRONTIER-36306528608"
TOKENIZER = tiktoken.get_encoding("cl100k_base")

# Raw evidence directory inside the packet.
RAW_DIR = os.path.join("research", "experiments", EXPERIMENT_ID, "raw")
RESPONSE_CACHE_DIR = os.path.join(RAW_DIR, "responses_cache")

USER_AGENT = (
    "SPIDER-Research2-Frontier/1.0 (stdlib urllib; bounded academic substrate probe; "
    "contact: spider-research automation)"
)
MIN_INTERVAL_S = 0.35

# Headers retained in the body-sensitive observation (prereg section 8).
RETAINED_HEADERS = (
    "content-type",
    "etag",
    "cache-control",
    "set-cookie",
    "location",
    "vary",
    "allow",
    "www-authenticate",
    "content-length",
    "last-modified",
    "x-frame-options",
    "strict-transport-security",
    "server",
)

# C3 token-field name pattern, verbatim from prereg.md section 4.2 criterion C3.
TOKEN_NAME_RE = re.compile(r"csrf|token|nonce|_token", re.IGNORECASE)
NONGET_METHODS = ("POST", "PUT", "PATCH", "DELETE")

LANDMARK_TAGS = (
    "main", "nav", "article", "section", "form", "table", "header", "footer",
    "aside", "ul", "ol", "dl", "h1", "h2", "h3", "p", "div", "body", "html",
)

_TAG_RE = re.compile(r"<\s*([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>", re.IGNORECASE)
_ATTR_RE = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""",
    re.IGNORECASE,
)
_FORM_RE = re.compile(r"<form\b.*?</form\s*>", re.IGNORECASE | re.DOTALL)
_FORM_OPEN_RE = re.compile(r"<form\b([^>]*)>", re.IGNORECASE)
_INPUT_RE = re.compile(r"<(input|textarea|select|button)\b([^>]*)>", re.IGNORECASE)
_LINK_RE = re.compile(r"<a\b([^>]*)>", re.IGNORECASE)
_SCRIPT_FORM_HINT_RE = re.compile(
    r"""(fetch|axios|XMLHttpRequest|\.post\(|\.put\(|\.delete\(|method\s*:\s*['"](post|put|patch|delete)['"])""",
    re.IGNORECASE,
)
_CSRF_HINT_RE = re.compile(
    r"""(csrf|xsrf|__requestverificationtoken|authenticity_token|nonce|_token|apitoken)""",
    re.IGNORECASE,
)
_VISIBILITY_RE = re.compile(
    r"""(type\s*=\s*["']?(hidden)["']?|display\s*:\s*none|visibility\s*:\s*hidden)""",
    re.IGNORECASE,
)


def sha256_hex(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8", "replace")
    return hashlib.sha256(data).hexdigest()


def _attrs(fragment: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in _ATTR_RE.finditer(fragment or ""):
        key = m.group(1).lower()
        val = m.group(2) or m.group(3) or m.group(4) or ""
        out[key] = val
    return out


@dataclass
class RawResponse:
    """One real HTTP transaction, retained verbatim."""

    url: str
    final_url: str
    method: str
    status_code: int | None
    headers: dict[str, str]
    body: bytes
    elapsed_ms: float
    t_start: float
    error: str | None = None
    request_body: str | None = None

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", "replace")

    @property
    def body_sha256(self) -> str:
        return sha256_hex(self.body)

    @property
    def content_type(self) -> str:
        return (self.headers.get("Content-Type") or self.headers.get("content-type") or "").lower()

    def evidence(self) -> dict[str, Any]:
        """Non-self-referential raw record (hash is over the payload, not the file)."""
        return {
            "experiment_id": EXPERIMENT_ID,
            "ts": round(self.t_start, 3),
            "url": self.url,
            "final_url": self.final_url,
            "method": self.method,
            "status_code": self.status_code,
            "elapsed_ms": round(self.elapsed_ms, 2),
            "request_body": self.request_body,
            "headers": self.headers,
            "body_bytes": len(self.body),
            "body_sha256": self.body_sha256,
            "body_excerpt": self.text[:600],
            "error": self.error,
        }


class HttpSubstrate:
    """Credential-free stdlib HTTP substrate with a per-instance cookie jar.

    One instance == one browser-like session. `HttpSubstrate(cookies=True)` models a
    state-carrying client; `cookies=False` models a stateless unconditional client.
    No Authorization header is ever sent: screen criterion C7 is about credential-free
    reachability, so sending credentials would destroy the thing being measured.
    """

    def __init__(self, timeout: int = 20, cookies: bool = True, label: str = "anon",
                 cache: "ResponseCache | None" = None, cache_key_prefix: str = ""):
        self.timeout = timeout
        self.label = label
        self.cache = cache
        self.cache_key_prefix = cache_key_prefix
        self.cache_hits = 0
        self._last_request_at = 0.0
        self.requests = 0
        self.errors = 0
        self.total_bytes = 0
        handlers: list[Any] = []
        self.jar = None
        if cookies:
            self.jar = http.cookiejar.CookieJar()
            handlers.append(urllib.request.HTTPCookieProcessor(self.jar))
        self._opener = urllib.request.build_opener(*handlers)
        # A stock UA would make some hosts 403; a descriptive UA is standard practice.
        self._opener.addheaders = []

    def _throttle(self) -> None:
        gap = time.time() - self._last_request_at
        if gap < MIN_INTERVAL_S:
            time.sleep(MIN_INTERVAL_S - gap)
        self._last_request_at = time.time()

    def fetch(
        self,
        url: str,
        method: str = "GET",
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        allow_redirects: bool = True,
        cacheable: bool = True,
    ) -> RawResponse:
        if self.cache is not None and cacheable:
            key = f"{self.cache_key_prefix}|{method}|{url}|{(data or b'').hex()[:64]}"
            hit = self.cache.get_by_key(key)
            if hit is not None:
                self.cache_hits += 1
                self.requests += 1
                return hit
        self._throttle()
        hdrs = {"User-Agent": USER_AGENT, "Accept": "*/*"}
        hdrs.update(headers or {})
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        t0 = time.time()
        self.requests += 1
        try:
            resp = self._opener.open(req, timeout=self.timeout)
            body = resp.read()
            final_url = resp.geturl()
            out = RawResponse(
                url=url, final_url=final_url, method=method, status_code=resp.status,
                headers={k: v for k, v in resp.headers.items()}, body=body,
                elapsed_ms=(time.time() - t0) * 1000.0, t_start=t0,
                request_body=data.decode("utf-8", "replace") if data else None,
            )
        except urllib.error.HTTPError as exc:  # 4xx/5xx are substrate facts, not crashes
            try:
                body = exc.read()
            except Exception:  # pragma: no cover - defensive
                body = b""
            self.errors += 1
            out = RawResponse(
                url=url, final_url=url, method=method, status_code=exc.code,
                headers={k: v for k, v in (exc.headers or {}).items()}, body=body,
                elapsed_ms=(time.time() - t0) * 1000.0, t_start=t0,
                error=f"HTTPError:{exc.code}", request_body=data.decode("utf-8", "replace") if data else None,
            )
        except Exception as exc:  # URLError, socket.timeout, ssl, ...
            self.errors += 1
            out = RawResponse(
                url=url, final_url=url, method=method, status_code=None, headers={},
                body=b"", elapsed_ms=(time.time() - t0) * 1000.0, t_start=t0,
                error=f"{type(exc).__name__}:{exc}",
                request_body=data.decode("utf-8", "replace") if data else None,
            )
        self.total_bytes += len(out.body)
        if self.cache is not None and cacheable:
            self.cache.put_by_key(
                f"{self.cache_key_prefix}|{method}|{url}|{(data or b'').hex()[:64]}", out
            )
        return out

    def cookie_names(self) -> list[str]:
        if self.jar is None:
            return []
        return sorted({c.name for c in self.jar})

    def cookie_fingerprint(self) -> str:
        if self.jar is None:
            return "nojar"
        return sha256_hex(json.dumps(sorted(
            f"{c.domain}|{c.name}" for c in self.jar
        )))[:16]


# --------------------------------------------------------------------------- #
# HTML structural parsing (regex, stdlib only -- prereg section 4.2 requires regex)
# --------------------------------------------------------------------------- #

def parse_links(html: str, base_url: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for m in _LINK_RE.finditer(html):
        a = _attrs(m.group(1))
        href = (a.get("href") or "").strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        try:
            absolute = urllib.parse.urljoin(base_url, href)
        except Exception:
            continue
        if absolute in seen:
            continue
        seen.add(absolute)
        out.append({"rel": a.get("rel", ""), "href": absolute, "raw_href": href[:200]})
    return out


def parse_forms(html: str, base_url: str) -> list[dict[str, Any]]:
    forms: list[dict[str, Any]] = []
    for idx, m in enumerate(_FORM_RE.finditer(html)):
        frag = m.group(0)
        open_m = _FORM_OPEN_RE.search(frag)
        f_attrs = _attrs(open_m.group(1) if open_m else "")
        method = (f_attrs.get("method") or "GET").upper()
        action_raw = f_attrs.get("action", "")
        try:
            action = urllib.parse.urljoin(base_url, action_raw) if action_raw else base_url
        except Exception:
            action = base_url
        inputs: list[dict[str, Any]] = []
        for im in _INPUT_RE.finditer(frag):
            tag = im.group(1).lower()
            ia = _attrs(im.group(2))
            inputs.append({
                "tag": tag,
                "name": ia.get("name", ""),
                "type": (ia.get("type") or ("text" if tag in ("input",) else tag)).lower(),
                "value": (ia.get("value") or "")[:200],
                "hidden": bool(_VISIBILITY_RE.search(im.group(2))),
            })
        inputs.sort(key=lambda d: (d["name"], d["tag"]))
        forms.append({
            "form_index": idx,
            "action_raw": action_raw[:200],
            "action": action,
            "method": method,
            "enctype": f_attrs.get("enctype", ""),
            "id": f_attrs.get("id", ""),
            "inputs": inputs,
            "input_names": sorted({i["name"] for i in inputs if i["name"]}),
            "has_token_field": any(TOKEN_NAME_RE.search(i["name"] or "") for i in inputs),
            "token_fields": sorted({i["name"] for i in inputs if TOKEN_NAME_RE.search(i["name"] or "")}),
            "html_sha256": sha256_hex(frag),
            "html_len": len(frag),
        })
    return forms


def parse_landmarks(html: str) -> list[str]:
    counts: dict[str, int] = {}
    for m in _TAG_RE.finditer(html):
        tag = m.group(1).lower()
        if tag in LANDMARK_TAGS:
            counts[tag] = counts.get(tag, 0) + 1
    return [f"{k}:{v}" for k, v in sorted(counts.items())]


def extract_key_body_fields(body_text: str, content_type: str) -> dict[str, Any]:
    """Body-derived content fields, truncated to 500 chars (prereg section 8)."""
    out: dict[str, Any] = {}
    ct = content_type or ""
    stripped = body_text.lstrip()
    if "json" in ct or stripped[:1] in "{[":
        try:
            parsed = json.loads(body_text)
        except Exception:
            parsed = None
        if parsed is not None:
            def walk(node: Any, prefix: str, depth: int) -> None:
                if depth > 3 or len(out) > 60:
                    return
                if isinstance(node, dict):
                    for k in list(node)[:40]:
                        walk(node[k], f"{prefix}.{k}" if prefix else str(k), depth + 1)
                elif isinstance(node, list):
                    out[f"{prefix}[len]"] = str(len(node))
                else:
                    out[prefix] = str(node)[:500]
            walk(parsed, "", 0)
            return out
    # Form values / token values for HTML bodies.
    vals: dict[str, str] = {}
    for im in _INPUT_RE.finditer(body_text):
        ia = _attrs(im.group(2))
        name = ia.get("name") or ""
        if not name or len(vals) > 60:
            continue
        vals[name] = ((ia.get("value") or "")[:500])
    if vals:
        out.update({f"input:{k}": v for k, v in sorted(vals.items())})
    # Token-like literal values anywhere in the body.
    tok: list[str] = []
    for m in _CSRF_HINT_RE.finditer(body_text):
        window = body_text[max(0, m.start() - 120): m.end() + 120]
        tok.append(re.sub(r"\s+", " ", window)[:500])
        if len(tok) >= 10:
            break
    if tok:
        out["_token_windows"] = tok
    return out


def script_form_hints(html: str) -> dict[str, Any]:
    """Non-GET verb / CSRF evidence that lives only in scripts, not in <form> markup.

    Reported as a diagnostic. The frozen C3 criterion counts declared forms only, so
    this never promotes a site to qualifying on its own; it only records that a
    scripted gate may exist that stdlib HTTP cannot reach.
    """
    scripts = re.findall(r"<script\b[^>]*>(.*?)</script\s*>", html, re.IGNORECASE | re.DOTALL)
    blob = "\n".join(scripts)
    return {
        "script_bytes": len(blob),
        "has_nonget_verb_hint": bool(_SCRIPT_FORM_HINT_RE.search(blob)),
        "has_csrf_hint": bool(_CSRF_HINT_RE.search(blob)),
        "csrf_hints": sorted({m.group(0).lower() for m in _CSRF_HINT_RE.finditer(blob)})[:10],
    }


# --------------------------------------------------------------------------- #
# Body-sensitive observation (prereg section 8)
# --------------------------------------------------------------------------- #

@dataclass
class BodySensitiveObservation:
    url: str
    method: str
    status_code: int | None
    link_relations: list[dict[str, str]]
    form_actions: list[dict[str, Any]]
    input_names: list[str]
    semantic_landmarks: list[str]
    response_headers: dict[str, str]
    body_sha256: str
    key_body_fields: dict[str, Any]
    body_bytes: int
    tokens: int = 0

    def serializable(self) -> dict[str, Any]:
        """FULL structure the frozen cost basis is defined over."""
        return {
            "url": self.url,
            "method": self.method,
            "status": self.status_code,
            "links": self.link_relations,
            "forms": self.form_actions,
            "inputs": self.input_names,
            "landmarks": self.semantic_landmarks,
            "headers": self.response_headers,
            "body_sha256": self.body_sha256,
            "key_body_fields": self.key_body_fields,
            "body_bytes": self.body_bytes,
        }

    def to_tokens(self) -> int:
        text = json.dumps(self.serializable(), sort_keys=True, separators=(",", ":"))
        return len(TOKENIZER.encode(text))

    def to_dict(self) -> dict[str, Any]:
        d = self.serializable()
        d["tokens"] = self.tokens
        return d


def observe(resp: RawResponse) -> BodySensitiveObservation:
    """Build the frozen body-sensitive observation from a real response."""
    ct = resp.content_type
    is_html = "html" in ct or (not ct and resp.text.lstrip()[:1] == "<")
    if is_html and resp.status_code is not None and resp.status_code < 400:
        html = resp.text
        links = parse_links(html, resp.final_url)
        forms = parse_forms(html, resp.final_url)
        landmarks = parse_landmarks(html)
    else:
        html = ""
        links, forms, landmarks = [], [], []
    obs = BodySensitiveObservation(
        url=resp.final_url or resp.url,
        method=resp.method,
        status_code=resp.status_code,
        link_relations=links[:80],
        form_actions=forms[:20],
        input_names=sorted({n for f in forms for n in f["input_names"]})[:120],
        semantic_landmarks=landmarks[:40],
        response_headers={k: v for k, v in resp.headers.items() if k.lower() in RETAINED_HEADERS},
        body_sha256=resp.body_sha256,
        key_body_fields=extract_key_body_fields(resp.text, ct) if resp.status_code is not None and resp.status_code < 400 else {},
        body_bytes=len(resp.body),
    )
    obs.tokens = obs.to_tokens()
    return obs


# --------------------------------------------------------------------------- #
# Raw evidence writers (non-self-referential hashes)
# --------------------------------------------------------------------------- #

class JsonlWriter:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._fh = open(path, "a", encoding="utf-8")
        self.n = 0

    def write(self, record: dict[str, Any]) -> dict[str, Any]:
        payload = dict(record)
        payload["seq"] = self.n
        # Hash over the payload only: never over the containing file.
        payload["record_sha256"] = sha256_hex(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self._fh.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        self._fh.flush()
        self.n += 1
        return payload

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:  # pragma: no cover
            pass


class ResponseCache:
    """Durable response cache: SHA256-named files, referenced from raw evidence."""

    def __init__(self, root: str = RESPONSE_CACHE_DIR):
        self.root = root
        os.makedirs(root, exist_ok=True)
        self.index: list[dict[str, Any]] = []
        self.key_index_path = os.path.join(root, "key_index.json")
        self.key_index: dict[str, Any] = {}
        if os.path.exists(self.key_index_path):
            try:
                with open(self.key_index_path, "r", encoding="utf-8") as fh:
                    self.key_index = json.load(fh)
            except Exception:
                self.key_index = {}
        self._dirty = 0

    def put_by_key(self, key: str, resp: RawResponse) -> None:
        if key in self.key_index:
            return
        entry = self.put(resp, "keyed")
        rec = {
            "url": resp.final_url or resp.url, "method": resp.method,
            "status_code": resp.status_code, "error": resp.error,
            "elapsed_ms": round(resp.elapsed_ms, 2),
            "body_sha256": resp.body_sha256, "path": entry["path"],
            "headers": resp.headers, "request_body": resp.request_body,
        }
        self.key_index[key] = rec
        self._dirty += 1
        if self._dirty >= 25:
            self.flush_keys()

    def flush_keys(self) -> None:
        tmp = self.key_index_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.key_index, fh, sort_keys=True)
        os.replace(tmp, self.key_index_path)
        self._dirty = 0

    def get_by_key(self, key: str) -> RawResponse | None:
        rec = self.key_index.get(key)
        if rec is None:
            return None
        try:
            with open(rec["path"], "rb") as fh:
                body = fh.read()
        except OSError:
            return None
        return RawResponse(
            url=rec["url"], final_url=rec["url"], method=rec["method"],
            status_code=rec["status_code"], headers=rec.get("headers") or {}, body=body,
            elapsed_ms=rec.get("elapsed_ms", 0.0), t_start=time.time(),
            error=rec.get("error"), request_body=rec.get("request_body"),
        )

    def put(self, resp: RawResponse, tag: str) -> dict[str, Any]:
        digest = resp.body_sha256
        name = f"{digest[:2]}/{digest}.txt"
        full = os.path.join(self.root, name)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if not os.path.exists(full):
            with open(full, "wb") as fh:
                fh.write(resp.body)
        entry = {
            "tag": tag,
            "url": resp.final_url or resp.url,
            "method": resp.method,
            "status_code": resp.status_code,
            "body_sha256": digest,
            "body_bytes": len(resp.body),
            "path": full,
        }
        self.index.append(entry)
        return entry

    def flush_index(self) -> str:
        path = os.path.join(self.root, "index.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"experiment_id": EXPERIMENT_ID, "entries": self.index}, fh, indent=1, sort_keys=True)
        return path


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def same_site(a: str, b: str) -> bool:
    try:
        pa, pb = urllib.parse.urlparse(a), urllib.parse.urlparse(b)
        return (pa.netloc.lower().lstrip("www.") == pb.netloc.lower().lstrip("www.")
                and pa.scheme in ("http", "https"))
    except Exception:
        return False


def registrable(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        return ""
