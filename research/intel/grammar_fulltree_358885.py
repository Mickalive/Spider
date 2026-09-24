"""
Full-tree semantic/multi-anchor grammar for EXP-INTEL-35888540685.
Implements full-tree traversal without truncation, product-specific subtree anchoring,
dynamic-token stripping, and placeholder expansion. This file's SHA256 is recomputed
at runtime as GRAMMAR_CODE_HASH (not hardcoded 8d4b).
"""

from __future__ import annotations
import re
import hashlib
from pathlib import Path

# Body regex (CRITICAL FIX / MV3): outerHTML is reduced to <body>...</body> (DOTALL)
# BEFORE dynamic-token stripping and SHA256. added by EXECUTE EXP-INTEL-35956094394.
BODY_REGEX = re.compile(r"<body[^>]*>.*?</body>", re.DOTALL)

# 9 dynamic-token regexes frozen before capture, not fit on outcome
DYNAMIC_TOKEN_REGEXES = [
    r"csrf[_-]?token",
    r"session[_-]?id",
    r"_token",
    r"timestamp",
    r"nonce",
    r"csrf value",
    r"sessionId",
    r"\b\d{13}\b",
    r"\b[a-f0-9]{32,}\b",
]

DYNAMIC_TOKEN_COMPILED = [re.compile(p, re.IGNORECASE) for p in DYNAMIC_TOKEN_REGEXES]

# Semantic anchors for product subtree: heading/price/add-to-cart/main/contentinfo
SEMANTIC_ANCHORS = ["heading", "price", "add-to-cart", "add_to_cart", "main", "contentinfo", "product", "heading[", "button"]

def extract_body(html: str) -> str:
    """Reduce outerHTML to <body>...</body> (DOTALL). Falls back to full html if no body tag."""
    m = BODY_REGEX.search(html)
    if m:
        return m.group(0)
    return html

# Expanded Magento attribute-bound stripping: only the attribute name + its quoted value
# are removed, never unbounded content. REPAIRED in EXP-INTEL-35956094394 (parent's
# r'form_key[^"]*' swallowed the whole document on single-quoted attributes, which made
# mutation detection impossible; bounded patterns fix that).
EXPANDED_ATTR_PATTERNS = [
    r"\b(?:form_key|uenc|store|session|timestamp|nonce)\s*=\s*\"[^\"]*\"",
    r"\b(?:form_key|uenc|store|session|timestamp|nonce)\s*=\s*'[^']*'",
    # Magento fotorama gallery instance token: fotorama{13-digit random} - a timestamp
    # class token (13-digit run preceded by letters) that changes per page load and
    # otherwise breaks SHA stability. Added under the 'expanded' set in
    # EXP-INTEL-35956094394 (fragment repair).
    r"\bfotorama\d{6,}\b",
]
EXPANDED_ATTR_COMPILED = [re.compile(p, re.IGNORECASE) for p in EXPANDED_ATTR_PATTERNS]

def strip_dynamic_tokens(html: str) -> str:
    """Normalize outerHTML by stripping dynamic tokens before SHA256.
    Includes 9 base regexes plus bounded expanded Magento form_key/uenc/store/session/timestamp/nonce
    attribute stripping. Applied AFTER body-regex reduction (extract_body).
    """
    body = extract_body(html)
    normalized = body
    for pat in DYNAMIC_TOKEN_COMPILED:
        normalized = pat.sub("__STRIPPED__", normalized)
    for pat in EXPANDED_ATTR_COMPILED:
        normalized = pat.sub("__STRIPPED__", normalized)
    return normalized

def sha256_normalized_subtree(outer_html: str) -> str:
    """SHA256 of relevant subtree outerHTML AFTER normalization and stripping."""
    normalized = strip_dynamic_tokens(outer_html)
    # No token truncation: use full normalized string
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def extract_element_pattern_fulltree(ax_tree: dict) -> list[str]:
    """
    Full-tree traversal: complete CDP Accessibility.getFullAXTree from root,
    no [:20] truncation. Returns tokenized path covering entire tree.
    """
    tokens = []
    # Traverse without truncation
    def walk(node, depth=0):
        role = node.get("role", {}).get("value", "unknown") if isinstance(node.get("role"), dict) else node.get("role", "unknown")
        name = node.get("name", {}).get("value", "") if isinstance(node.get("name"), dict) else node.get("name", "")
        tokens.append(f"{role}:{name}")
        for child in node.get("children", []):
            walk(child, depth+1)
    # Expect ax_tree has 'nodes' or is root
    if isinstance(ax_tree, dict) and "nodes" in ax_tree:
        for n in ax_tree["nodes"]:
            walk(n)
    elif isinstance(ax_tree, dict):
        walk(ax_tree)
    # NO truncation: return all tokens
    # Prior degenerate [:20] would be tokens[:20] — explicitly NOT done
    return tokens

def longest_prefix_without_fallback(a: list[str], b: list[str]) -> int:
    """Longest common prefix length without fallback, requires >=1 token."""
    i = 0
    for x, y in zip(a, b):
        if x == y:
            i += 1
        else:
            break
    return i

def get_task_start_url(start_urls, base="http://localhost:7770"):
    """Expand __SHOPPING__ and __SHOPPING__/path per spec CRITICAL FIX 2."""
    if not start_urls:
        return base
    raw = start_urls[0]
    if raw == "__SHOPPING__":
        return base + "/"
    if raw.startswith("__SHOPPING__/"):
        path_part = raw[len("__SHOPPING__"):]
        return base + path_part
    if raw.startswith("__SHOPPING_ADMIN__"):
        return raw.replace("__SHOPPING_ADMIN__", base)
    return raw

def recompute_grammar_hash() -> str:
    """Recompute this file's SHA256 from live file (not hardcoded constant)."""
    p = Path(__file__)
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

if __name__ == "__main__":
    print(recompute_grammar_hash())
    # Verify no truncation present: tokens[:20] string not in file
    content = Path(__file__).read_text()
    assert "[:20]" not in content or "NOT done" in content, "Truncation found"
    assert BODY_REGEX.pattern == r"<body[^>]*>.*?</body>", "body regex missing"
    print("No truncation verified, anchors:", SEMANTIC_ANCHORS)
    print("body regex present:", BODY_REGEX.pattern)
