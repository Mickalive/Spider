"""Neutral certificate detector (producer code for EXP-GRAPH-37978902447;
adapted from EXP-GRAPH-37950584469).

Deliberately minimal PRESENCE-ONLY detector used at GATE C to certify in-list
field presence and body variation.  It is a raw byte regex for ``name=``
occurrences whose captured value is in the frozen capability-token name list.
It extracts NO values and is not either extraction path, so it cannot pre-empt
the confirmatory extraction.

The frozen capability-token name list is duplicated as a literal (it is frozen
data, not extraction logic).
"""
from __future__ import annotations

import re

TOKEN_NAME_LIST = [
    "authenticity_token",
    "authenticityToken",
    "csrfmiddlewaretoken",
    "_csrf",
    "csrf_token",
    "csrf-token",
    "__RequestVerificationToken",
    "__VIEWSTATE",
    "__EVENTVALIDATION",
    "wpEditToken",
    "wpCreateaccountToken",
    "wpCreateaccounttoken",
    "wpLoginToken",
    "wpCancelToken",
    "form_token",
    "__FORM_TOKEN",
    "auth_token",
    "os_authkey",
    "bbl_",
    "requesttoken",
    "state",
    "code",
    "nonce",
    "otp",
    "user_token",
    "session_token",
    "authenticity",
]
TOKEN_NAME_SET = frozenset(TOKEN_NAME_LIST)

# Capture the value of any `name=` attribute occurrence, quoted or unquoted.
_NAME_ATTR_RE = re.compile(
    r"name\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>\"']+))", re.I
)


def find_in_list_names(body: bytes):
    """Return the sorted unique list of in-list token names appearing in `name=`."""
    text = body.decode("utf-8", errors="replace")
    found = set()
    for m in _NAME_ATTR_RE.finditer(text):
        value = m.group(1) or m.group(2) or m.group(3) or ""
        if value in TOKEN_NAME_SET:
            found.add(value)
    return sorted(found)


def count_in_list_occurrences(body: bytes):
    """Total number of `name=<in-list>` occurrences (presence only)."""
    text = body.decode("utf-8", errors="replace")
    total = 0
    for m in _NAME_ATTR_RE.finditer(text):
        value = m.group(1) or m.group(2) or m.group(3) or ""
        if value in TOKEN_NAME_SET:
            total += 1
    return total
