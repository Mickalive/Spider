"""P-EXTRACT-A : HTMLPARSER extraction path (producer code for EXP-GRAPH-37978902447;
adapted from EXP-GRAPH-37950584469 / EXP-GRAPH-37964565784).

Independently written stdlib ``html.parser`` based extraction of ACTION-GATING
STATE ITEMS (AGSI) from raw HTTP response bytes.  This module is intentionally
self-contained: it imports only the Python standard library and does not import
``path_b_regexlex`` or any shared extraction helper (frozen requirement
``NC-PATH-INDEPENDENCE`` / ``V03-EXTRACTION-PATH-INDEPENDENCE``).

The frozen capability-token name list is duplicated as a literal here (and in
path B) rather than imported from a shared module, so that an AST import-graph
attestation cannot find a shared extraction dependency.

Entity decoding: ``html.parser`` performs standard-library HTML entity decoding
of attribute values itself; applying ``html.unescape`` again would double-decode
(verified: ``a&amp;lt;b&amp;`` -> ``a&lt;b&`` already at parser output).  The
stdlib entity decoder is therefore used exactly once, by the parser.  This is
the single disclosed operationalization choice versus the spec's wording
("entity decoding via stdlib html.unescape"); see validity_notes.
"""
from __future__ import annotations

from html.parser import HTMLParser

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


class _Agsiparser(HTMLParser):
    def __init__(self) -> None:
        # convert_charrefs only affects text data; attribute values are decoded
        # by the parser in either mode (verified on CPython 3.12).
        super().__init__(convert_charrefs=True)
        self.open_forms: list[dict] = []
        self.closed_forms: list[dict] = []
        self.metas: list[dict] = []

    def _handle(self, tag: str, attrs) -> None:
        a = {k: v for k, v in attrs}
        t = tag.lower()
        if t == "form":
            self.open_forms.append(
                {"action": a.get("action"), "method": a.get("method"), "fields": []}
            )
        elif t in _FORM_TAGS:
            if self.open_forms:
                typ = a.get("type")
                if typ is None:
                    typ = _FORM_TAGS[t]
                self.open_forms[-1]["fields"].append(
                    {
                        "name": a.get("name"),
                        "type_class": str(typ).lower(),
                        "value_present": "value" in a,
                        "value": a.get("value"),
                    }
                )
        elif t == "meta":
            self.metas.append(
                {
                    "name": a.get("name"),
                    "content_present": "content" in a,
                    "content": a.get("content"),
                }
            )

    def handle_starttag(self, tag, attrs):  # noqa: D401
        self._handle(tag, attrs)

    def handle_startendtag(self, tag, attrs):  # noqa: D401
        self._handle(tag, attrs)

    def handle_endtag(self, tag):
        if tag.lower() == "form" and self.open_forms:
            self.closed_forms.append(self.open_forms.pop())


def _state_and_value(value_present: bool, value):
    """Return (state, exact_value_or_None).

    A discovered in-list field with no non-empty value is PRESENT_EMPTY (this is
    the frozen NC-EXTRACT-EMPTY-VALUE operationalization: field found but no
    non-empty exact value).  A field name that is not present at all is simply
    absent from the output (reported as ABSENT by the aggregation layer).
    """
    if value is None or value == "":
        return ("PRESENT_EMPTY", None)
    return ("VALUE", value)


def extract(body: bytes):
    """Parse raw bytes and return a list of AGSI records."""
    text = body.decode("utf-8", errors="replace")
    parser = _Agsiparser()
    parser.feed(text)
    parser.close()
    while parser.open_forms:
        parser.closed_forms.append(parser.open_forms.pop())

    out = []
    for form in parser.closed_forms:
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
            state, value = _state_and_value(field["value_present"], field["value"])
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
    for meta in parser.metas:
        name = meta["name"]
        if name not in TOKEN_NAME_SET:
            continue
        state, value = _state_and_value(meta["content_present"], meta["content"])
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
