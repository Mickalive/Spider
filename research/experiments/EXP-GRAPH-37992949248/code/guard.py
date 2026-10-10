"""Frozen four-channel freshness guard for EXP-GRAPH-37992949248 (adapted from
EXP-GRAPH-37978902447; semantics unchanged per SB-06).

Decision set {REUSE, ABSTAIN}.  ABSTAIN is the product-preferred UNKNOWN /
unsafe-to-inherit outcome; REUSE inherits the recorded binding.

Channels (activation inputs and firing conditions frozen in spec.json):
- CH-STRUCT-SIG        : structure_signature = (type_class, form_action,
                         form_method, sorted form_input_names) differs.
- CH-TRANSPORT-VALIDATOR: transport_signature = (ETag, Last-Modified,
                         Cache-Control max-age, Vary) plus final_url differs.
- CH-POSTCOND-SEM      : the session in-list field-name set differs.
- CH-PRECOND-BINDING   : live exact value != recorded exact value byte-exact.

Baselines:
- B-INCUMBENT-SIGNAL-ONLY : REUSE iff none of CH-STRUCT-SIG,
  CH-TRANSPORT-VALIDATOR, CH-POSTCOND-SEM fires (value-blind incumbent).
- B-VALUE-AWARE           : REUSE iff CH-PRECOND-BINDING does not fire.
- B-FULL-GUARD            : REUSE iff none of the four channels fires.
- B-NO-GUARD-REPLAY       : always REUSE.

This module is deliberately small and importable so its firing logic can be
unit-tested by the guard-logic fixtures without touching the scored population.
"""
from __future__ import annotations

CHANNELS = [
    "CH-STRUCT-SIG",
    "CH-TRANSPORT-VALIDATOR",
    "CH-POSTCOND-SEM",
    "CH-PRECOND-BINDING",
]

REUSE = "REUSE"
ABSTAIN = "ABSTAIN"


def incumbent_reuse(fired: dict) -> bool:
    return not (
        fired.get("CH-STRUCT-SIG", False)
        or fired.get("CH-TRANSPORT-VALIDATOR", False)
        or fired.get("CH-POSTCOND-SEM", False)
    )


def valueaware_reuse(fired: dict) -> bool:
    return not fired.get("CH-PRECOND-BINDING", False)


def full_reuse(fired: dict) -> bool:
    return not any(bool(fired.get(c, False)) for c in CHANNELS)


def decide(guard_id: str, fired: dict) -> str:
    if guard_id == "B-INCUMBENT-SIGNAL-ONLY":
        return REUSE if incumbent_reuse(fired) else ABSTAIN
    if guard_id == "B-VALUE-AWARE":
        return REUSE if valueaware_reuse(fired) else ABSTAIN
    if guard_id == "B-FULL-GUARD":
        return REUSE if full_reuse(fired) else ABSTAIN
    if guard_id == "B-NO-GUARD-REPLAY":
        return REUSE
    raise ValueError(f"unknown guard id: {guard_id}")
