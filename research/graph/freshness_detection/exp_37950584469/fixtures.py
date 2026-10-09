"""Frozen instrument fixtures for EXP-GRAPH-37950584469.

SYNTHETIC BYTES PERMITTED ONLY FOR INSTRUMENT SELF-TEST (V08).  Fixtures are
unit tests only, are never part of the scored population, and no claim depends
on them.

- SYN-CANARY-BOTH : positive instrument fixture. Non-GET form with an in-list
  hidden input carrying a literal value, plus an in-list meta token with
  content. Both paths must recover exactly the same 2 (name, value) pairs.
- SYN-EMPTY-VALUE : empty-value instrument fixture. In-list hidden input with no
  value attribute and in-list meta token with empty content. Both paths must
  classify PRESENT-EMPTY and agree.
- SYN-JSSTRING : representation-loss instrument fixture. An in-list token name
  appearing only inside a JavaScript string literal. Both paths must recover 0
  non-empty values.
"""
from __future__ import annotations

SYN_CANARY_BOTH = (
    b"<!DOCTYPE html><html><head>"
    b'<meta name="csrf-token" content="fixture-meta-canary-91bd"/>'
    b"</head><body>"
    b'<form method="post" action="https://example.invalid/submit">'
    b'<input type="hidden" name="authenticity_token" value="fixture-canary-value-7f3a"/>'
    b"</form></body></html>"
)

SYN_EMPTY_VALUE = (
    b"<!DOCTYPE html><html><head>"
    b'<meta name="csrf-token" content=""/>'
    b"</head><body>"
    b'<form method="post" action="https://example.invalid/x">'
    b'<input type="hidden" name="authenticity_token"/>'
    b"</form></body></html>"
)

SYN_JSSTRING = (
    b"<!DOCTYPE html><html><body>"
    b"<script>"
    b'var t = "authenticity_token"; var o = {"csrf_token": "rendered-later"};'
    b"</script>"
    b'<form method="post" action="https://example.invalid/y"></form>'
    b"</body></html>"
)

FIXTURES = {
    "SYN-CANARY-BOTH": SYN_CANARY_BOTH,
    "SYN-EMPTY-VALUE": SYN_EMPTY_VALUE,
    "SYN-JSSTRING": SYN_JSSTRING,
}
