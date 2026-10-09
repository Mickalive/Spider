"""P-EXTRACT-B : REGEXLEX extraction path (producer code, EXP-GRAPH-37950584469).

Independently written byte-level lexer that uses ``re`` only for tag/attribute
token boundaries plus a hand-written whitespace/quote/attribute state machine
and a hand-written HTML entity decoder (it does **not** use ``html.unescape``
and does not import ``path_a_htmlparser`` or any shared extraction helper).

This is structurally independent from path A: different scanning primitive
(token regex + manual state machine vs. ``html.parser`` callback API),
different entity decoder, different attribute parser.  Frozen requirement
``NC-PATH-INDEPENDENCE`` / ``V03``.

The frozen capability-token name list is duplicated as a literal (not imported
from a shared module) so an AST import-graph attestation finds no shared
extraction dependency.
"""
from __future__ import annotations

import re

# Frozen capability-token name list (spec.frozen_populations.frozen_token_name_list)
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

_FORM_TAGS = {"input": "text", "textarea": "textarea", "select": "select"}

# Hand-written entity decoder -------------------------------------------------
_ENTITY_RE = re.compile(r"&(#x[0-9A-Fa-f]+|#[0-9]+|[A-Za-z][A-Za-z0-9]*);")
_NAMED_ENTITIES = {
    "amp": "&",
    "lt": "<",
    "gt": ">",
    "quot": '"',
    "apos": "'",
    "nbsp": "\xa0",
    "copy": "\xa9",
    "reg": "\xae",
    "hellip": "\u2026",
    "mdash": "\u2014",
    "ndash": "\u2013",
    "lsquo": "\u2018",
    "rsquo": "\u2019",
    "ldquo": "\u201c",
    "rdquo": "\u201d",
    "middot": "\xb7",
    "times": "\xd7",
    "trade": "\u2122",
}


def _decode_entities(text):
    if text is None:
        return None

    def _repl(match: "re.Match[str]") -> str:
        ent = match.group(1)
        if ent[:2] in ("#x", "#X"):
            try:
                return chr(int(ent[2:], 16))
            except (ValueError, OverflowError):
                return match.group(0)
        if ent.startswith("#"):
            try:
                return chr(int(ent[1:]))
            except (ValueError, OverflowError):
                return match.group(0)
        return _NAMED_ENTITIES.get(ent, match.group(0))

    return _ENTITY_RE.sub(_repl, text)


# Lexer ----------------------------------------------------------------------
# One combined token regex: comments, CDATA, doctype/declarations, processing
# instructions, and ordinary start/end tags (quoted attribute values may contain
# '>').  re is used only for tag/attribute token boundaries.
_TOKEN_RE = re.compile(
    r"<!--.*?-->"
    r"|<!\[CDATA\[.*?\]\]>"
    r"|<![^>]*>"
    r"|<\?.*?\?>"
    r"|</?[A-Za-z][A-Za-z0-9:_-]*(?:\"[^\"]*\"|'[^']*'|[^>\"'])*?/?>",
    re.S,
)


def _parse_tag(token: str):
    """Return (tag_name_lower, attrs_string, is_closing) or (None, '', False)."""
    inner = token[1:-1]
    is_closing = False
    if inner.startswith("/"):
        is_closing = True
        inner = inner[1:]
    inner = inner.strip()
    if inner.endswith("/"):
        inner = inner[:-1]
    m = re.match(r"[A-Za-z][A-Za-z0-9:_-]*", inner)
    if not m:
        return (None, "", is_closing)
    return (m.group(0).lower(), inner[m.end():], is_closing)


def _parse_attrs(attr_text: str):
    """Hand-written attribute state machine.

    Returns dict name(lower) -> value(str|None).  Membership means the attribute
    is present; a present attribute with no value maps to None.
    """
    attrs: dict[str, str | None] = {}
    i, n = 0, len(attr_text)
    while i < n:
        while i < n and attr_text[i] in " \t\r\n/":
            i += 1
        if i >= n:
            break
        j = i
        while j < n and attr_text[j] not in " \t\r\n=/>":
            j += 1
        name = attr_text[i:j]
        while j < n and attr_text[j] in " \t\r\n":
            j += 1
        value = None
        if j < n and attr_text[j] == "=":
            j += 1
            while j < n and attr_text[j] in " \t\r\n":
                j += 1
            if j < n and attr_text[j] in "\"'":
                quote = attr_text[j]
                j += 1
                k = attr_text.find(quote, j)
                if k < 0:
                    k = n
                value = attr_text[j:k]
                j = k + 1
            else:
                k = j
                while k < n and attr_text[k] not in " \t\r\n>":
                    k += 1
                value = attr_text[j:k]
                j = k
        if name:
            attrs[name.lower()] = value
        i = max(j, i + 1)
    return attrs


def _state_and_value(value) -> tuple[str, str | None]:
    if value is None or value == "":
        return ("PRESENT_EMPTY", None)
    return ("VALUE", value)


def extract(body: bytes):
    """Parse raw bytes and return a list of AGSI records."""
    text = body.decode("utf-8", errors="replace")
    open_forms: list[dict] = []
    closed_forms: list[dict] = []
    metas: list[dict] = []

    pos = 0
    n = len(text)
    while True:
        m = _TOKEN_RE.search(text, pos)
        if not m:
            break
        token = m.group(0)
        pos = m.end()

        if token.startswith("<!--") or token.startswith("<![CDATA[") or token.startswith("<!"):
            continue
        if token.startswith("<?"):
            continue

        tag, attr_text, is_closing = _parse_tag(token)
        if tag is None:
            continue
        if tag in ("script", "style"):
            close = re.compile(r"</\s*" + re.escape(tag) + r"\s*>", re.I).search(text, pos)
            pos = close.end() if close else n
            continue

        if is_closing:
            if tag == "form" and open_forms:
                closed_forms.append(open_forms.pop())
            continue

        attrs = _parse_attrs(attr_text)
        if tag == "form":
            open_forms.append(
                {
                    "action": attrs.get("action"),
                    "method": attrs.get("method"),
                    "fields": [],
                }
            )
        elif tag in _FORM_TAGS:
            if open_forms:
                typ = attrs.get("type")
                if typ is None:
                    typ = _FORM_TAGS[tag]
                name = attrs.get("name")
                vpresent = "value" in attrs
                vraw = attrs.get("value")
                open_forms[-1]["fields"].append(
                    {
                        "name": _decode_entities(name) if name is not None else None,
                        "type_class": str(typ).lower(),
                        "value_present": vpresent,
                        "value": _decode_entities(vraw) if vraw is not None else None,
                    }
                )
        elif tag == "meta":
            name = attrs.get("name")
            cpresent = "content" in attrs
            craw = attrs.get("content")
            metas.append(
                {
                    "name": _decode_entities(name) if name is not None else None,
                    "content_present": cpresent,
                    "content": _decode_entities(craw) if craw is not None else None,
                }
            )

    while open_forms:
        closed_forms.append(open_forms.pop())

    out = []
    for form in closed_forms:
        method = form["method"]
        non_get = method is not None and str(method).strip().lower() != "get"
        if not non_get:
            continue
        input_names = sorted(
            {str(f["name"]) for f in form["fields"] if f["name"] is not None}
        )
        for field in form["fields"]:
            name = field["name"]
            if name not in TOKEN_NAME_SET:
                continue
            state, value = _state_and_value(field["value"])
            out.append(
                {
                    "field_name": name,
                    "kind": "form_field",
                    "state": state,
                    "value": value,
                    "form_action": form["action"],
                    "form_method": method,
                    "type_class": field["type_class"],
                    "form_input_names": input_names,
                }
            )
    for meta in metas:
        name = meta["name"]
        if name not in TOKEN_NAME_SET:
            continue
        state, value = _state_and_value(meta["content"])
        out.append(
            {
                "field_name": name,
                "kind": "meta",
                "state": state,
                "value": value,
                "form_action": None,
                "form_method": None,
                "type_class": "meta",
                "form_input_names": [],
            }
        )
    return out
