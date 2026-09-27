"""RAW EVIDENCE probe: does the frozen substrate match prereg.md section 7?

prereg.md section 7 asserts, of the reused substrate (sha256 d3fe358e...):
  * multi-step auth: Bearer token issuance -> validation
  * pagination:    ?page=N&page_size=K with Link headers
  * schema discovery: GET /api/v1/schema returns JSON Schema
  * Resource-A endpoints: /api/v1/items/*, /api/v1/collections/*
  * Resource-B endpoints: /api/v1/products/*, /api/v1/categories/*
  * bound path form /api/v1/<collection>/<slot>

This probe issues real HTTP requests and records status codes and headers.
It writes raw_evidence/substrate_surface_probe.json and never interprets.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

EXP = Path(__file__).resolve().parent
SUBSTRATE = EXP.parent / "EXP-PRODUCT-36272385776" / "substrate.py"

spec = importlib.util.spec_from_file_location("spider_substrate", SUBSTRATE)
mod = importlib.util.module_from_spec(spec)
sys.modules["spider_substrate"] = mod
spec.loader.exec_module(mod)

OUT = EXP / "raw_evidence" / "substrate_surface_probe.json"


def req(base: str, path: str, token: str | None = None, method: str = "GET"):
    """One real HTTP request. Returns status, headers, body-snippet, or error."""
    r = urllib.request.Request(base + path, method=method)
    if token:
        r.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(r, timeout=10) as resp:
            raw = resp.read()
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            return {
                "path": path,
                "method": method,
                "status": resp.status,
                "link_header": hdrs.get("link"),
                "etag": hdrs.get("etag"),
                "body_snippet": raw[:220].decode("utf-8", "replace"),
            }
    except urllib.error.HTTPError as e:
        raw = e.read()
        hdrs = {k.lower(): v for k, v in e.headers.items()}
        return {
            "path": path,
            "method": method,
            "status": e.code,
            "link_header": hdrs.get("link"),
            "etag": hdrs.get("etag"),
            "body_snippet": raw[:220].decode("utf-8", "replace"),
        }
    except Exception as e:  # pragma: no cover - diagnostic path
        return {"path": path, "method": method, "error": f"{type(e).__name__}: {e}"}


def main() -> int:
    sub = mod.Substrate()
    try:
        sub.seed_many("items", mod.RESOURCE_A_IDS[:40])
        sub.seed_many("products", list(mod.RESOURCE_B_IDS[:40]))
        base = sub.base_url

        probes = []

        # --- prereg section 7: declared endpoints, verbatim -------------------
        probes.append({"claim": "auth_issue", "expect": "Bearer token issuance step",
                       "probe": req(base, "/auth/token", method="POST")})
        probes.append({"claim": "schema_discovery", "expect": "GET /api/v1/schema returns JSON Schema",
                       "probe": req(base, "/api/v1/schema", token="tok-owner-a")})
        probes.append({"claim": "pagination", "expect": "?page=N&page_size=K with Link headers",
                       "probe": req(base, "/items?page=1&page_size=10", token="tok-owner-a")})
        probes.append({"claim": "resource_a_read", "expect": "/api/v1/items/<id>",
                       "probe": req(base, "/api/v1/items/item-1", token="tok-owner-a")})
        probes.append({"claim": "resource_b_read", "expect": "/api/v1/products/<id>",
                       "probe": req(base, "/api/v1/products/PROD-100", token="tok-owner-a")})
        probes.append({"claim": "collections_endpoint", "expect": "/api/v1/collections/*",
                       "probe": req(base, "/api/v1/collections", token="tok-owner-a")})
        probes.append({"claim": "categories_endpoint", "expect": "/api/v1/categories/*",
                       "probe": req(base, "/api/v1/categories", token="tok-owner-a")})

        # --- what the substrate actually serves -------------------------------
        actual = []
        actual.append({"claim": "index", "probe": req(base, "/", token="tok-owner-a")})
        actual.append({"claim": "item_read_unprefixed", "probe": req(base, "/items/item-1", token="tok-owner-a")})
        actual.append({"claim": "product_read_unprefixed", "probe": req(base, "/products/PROD-100", token="tok-owner-a")})
        actual.append({"claim": "listing_limit", "probe": req(base, "/items?limit=5", token="tok-owner-a")})
        actual.append({"claim": "listing_q", "probe": req(base, "/items?q=cat1&limit=5", token="tok-owner-a")})
        actual.append({"claim": "unauthenticated", "probe": req(base, "/items/item-1")})

        # --- identifier-namespace disjointness (a real, checkable property) ----
        a, b = set(mod.RESOURCE_A_IDS), set(mod.RESOURCE_B_IDS)
        disjoint = {
            "resource_a_count": len(a),
            "resource_b_count": len(b),
            "intersection": sorted(a & b),
            "disjoint": not (a & b),
        }

        # --- token expiry is a real cost source ------------------------------
        expiry = {"TOKEN_EXPIRY": mod.TOKEN_EXPIRY}

        record = {
            "probe_kind": "raw_evidence",
            "interpretation": None,
            "substrate_path": str(SUBSTRATE.relative_to(EXP.parents[2])),
            "substrate_sha256": hashlib.sha256(SUBSTRATE.read_bytes()).hexdigest(),
            "prereg_claimed_sha256_prefix": "d3fe358e",
            "prereg_declared_endpoints": probes,
            "actual_endpoints": actual,
            "identifier_namespaces": disjoint,
            "token_expiry": expiry,
        }
        OUT.write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps(record, indent=2))
    finally:
        sub.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
